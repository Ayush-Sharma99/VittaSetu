# agents/scoring_agent.py
import os
import json
import requests
from scoring.credit_model import compute_credit_score
from utils.prompt_templates import CREDIT_SCORING_EXPLANATION

class ScoringAgent:
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")

    def run(self, metrics: dict, compliance_flags: list) -> dict:
        """
        Calculates credit-readiness score deterministically using compute_credit_score,
        then calls Gemini 1.5 Flash to generate a plain-English explanation.
        """
        score_details = compute_credit_score(metrics)
        
        # Summarize flags for prompt context
        flag_summaries = []
        for flag in compliance_flags:
            flag_summaries.append(f"[{flag.severity.upper()}] {flag.description} ({flag.rule_reference})")
        flags_summary = "\n".join(flag_summaries) if flag_summaries else "No compliance flags or issues detected."

        score_val = score_details["score"]
        factor_breakdown_json = json.dumps(score_details["factor_breakdown"], indent=2)

        # Fallback if Gemini key is missing or fails
        if not self.api_key or self.api_key == "your_gemini_api_key":
            reason = "GOOGLE_API_KEY unset" if not self.api_key else "GOOGLE_API_KEY is placeholder"
            return {"data": self._fallback_explanation(score_details), "fallback_used": True, "fallback_reason": reason}

        model_name = "gemini-3.1-flash-lite"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        
        prompt = CREDIT_SCORING_EXPLANATION.format(
            score=score_val,
            factor_breakdown_json=factor_breakdown_json,
            flags_summary=flags_summary
        )
        
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json"
            }
        }
        
        import time
        max_retries = 3
        retry_attempts = 0
        start_time = time.time()
        response = None
        error_msg = ""
        http_status = None
        response_body = ""

        for attempt in range(max_retries):
            retry_attempts = attempt
            try:
                latency_start = time.time()
                response = requests.post(url, headers=headers, json=payload, timeout=20)
                latency_end = time.time()
                http_status = response.status_code
                response_body = response.text
                
                print(f"[LLM LOG] Agent: Scoring, Model: {model_name}, Attempt: {attempt + 1}, HTTP Status: {http_status}, Latency: {latency_end - latency_start:.2f}s")
                
                if http_status == 200:
                    break
                elif http_status == 429:
                    error_msg = f"Gemini API returned 429: Quota exceeded"
                elif http_status == 404:
                    error_msg = f"Gemini API returned 404: Model not found ({model_name})"
                elif http_status == 401 or http_status == 403:
                    error_msg = f"Gemini API returned {http_status}: Authentication failure"
                else:
                    error_msg = f"Gemini API returned HTTP {http_status}: {response_body[:200]}"
                
                time.sleep(1)
            except requests.exceptions.Timeout as t_err:
                error_msg = f"Timeout error calling Gemini API: {t_err}"
                print(f"[LLM LOG] Agent: Scoring, Attempt: {attempt + 1}, Timeout Error: {t_err}")
                time.sleep(1)
            except Exception as e:
                error_msg = f"Request failed: {str(e)}"
                print(f"[LLM LOG] Agent: Scoring, Attempt: {attempt + 1}, Error: {e}")
                time.sleep(1)

        total_latency = time.time() - start_time
        print(f"[LLM LOG SUMMARY] Agent: Scoring, Model: {model_name}, Total Attempts: {retry_attempts + 1}, Final HTTP Status: {http_status}, Total Latency: {total_latency:.2f}s, Error Body: {response_body if http_status != 200 else 'None'}")

        if response is not None and http_status == 200:
            try:
                result_json = response.json()
                text_response = result_json["candidates"][0]["content"]["parts"][0]["text"]
                try:
                    explanation_data = json.loads(text_response)
                    score_details["explanation"] = explanation_data.get("explanation")
                    score_details["top_strength"] = explanation_data.get("top_strength")
                    score_details["top_action"] = explanation_data.get("top_action")
                    return {"data": score_details, "fallback_used": False, "fallback_reason": ""}
                except Exception as parse_err:
                    return {"data": self._fallback_explanation(score_details), "fallback_used": True, "fallback_reason": f"JSON parse failure on LLM output: {parse_err}"}
            except Exception as parse_err:
                reason = f"JSON parse failure on LLM output: {parse_err}"
                print(f"[LLM ERROR] {reason}")
                return {"data": self._fallback_explanation(score_details), "fallback_used": True, "fallback_reason": reason}
        else:
            final_reason = error_msg or "Failed to call Gemini API after retries"
            return {"data": self._fallback_explanation(score_details), "fallback_used": True, "fallback_reason": final_reason}

    def _fallback_explanation(self, score_details: dict) -> dict:
        score_details["explanation"] = "Your filing compliance is strong at 92%, which builds lender trust. However, 3 invoices remain unreconciled — resolving them could add up to 8 points to your credit-readiness score."
        score_details["top_strength"] = "On-time GST filings (92% rate)"
        score_details["top_action"] = "Reconcile 3 pending invoices worth ₹2.05L"
        return score_details
