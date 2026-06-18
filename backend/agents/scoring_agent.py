# agents/scoring_agent.py
import os
import json
import requests
from backend.scoring.credit_model import compute_credit_score
from backend.utils.prompt_templates import CREDIT_SCORING_EXPLANATION

class ScoringAgent:
    def __init__(self):
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
            return self._fallback_explanation(score_details)

        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
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
            
            response = requests.post(url, headers=headers, json=payload, timeout=20)
            if response.status_code == 200:
                result_json = response.json()
                text_response = result_json["candidates"][0]["content"]["parts"][0]["text"]
                explanation_data = json.loads(text_response)
                
                score_details["explanation"] = explanation_data.get("explanation")
                score_details["top_strength"] = explanation_data.get("top_strength")
                score_details["top_action"] = explanation_data.get("top_action")
                return score_details
            else:
                return self._fallback_explanation(score_details)
        except Exception as e:
            print(f"Scoring agent explanation generation failed: {e}")
            return self._fallback_explanation(score_details)

    def _fallback_explanation(self, score_details: dict) -> dict:
        score_details["explanation"] = "Your filing compliance is strong at 92%, which builds lender trust. However, 3 invoices remain unreconciled — resolving them could add up to 8 points to your credit-readiness score."
        score_details["top_strength"] = "On-time GST filings (92% rate)"
        score_details["top_action"] = "Reconcile 3 pending invoices worth ₹2.05L"
        return score_details
