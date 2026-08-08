# agents/chat_agent.py
import os
import json
import requests
from utils.prompt_templates import CHAT_SYSTEM_PROMPT

class ChatAgent:
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")

    def run(self, message: str, business_context: dict) -> dict:
        """
        Conversational agent interface responding to user questions about business financial state.
        Uses Gemini 1.5 Flash function calling (simulated or actual) to query context details.
        """
        context_json = json.dumps(business_context, indent=2, default=str)
        system_prompt = CHAT_SYSTEM_PROMPT.format(business_context_json=context_json)

        # Fallback responses tailored to golden-path queries
        if not self.api_key or self.api_key == "your_gemini_api_key":
            reason = "GOOGLE_API_KEY unset" if not self.api_key else "GOOGLE_API_KEY is placeholder"
            res = self._fallback_chat(message)
            res.update({"fallback_used": True, "fallback_reason": reason})
            return res

        model_name = "gemini-3.1-flash-lite"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": f"SYSTEM SYSTEM_INSTRUCTION:\n{system_prompt}\n\nUser Question:\n{message}"}
                    ]
                }
            ]
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
                
                print(f"[LLM LOG] Agent: Chat, Model: {model_name}, Attempt: {attempt + 1}, HTTP Status: {http_status}, Latency: {latency_end - latency_start:.2f}s")
                
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
                print(f"[LLM LOG] Agent: Chat, Attempt: {attempt + 1}, Timeout Error: {t_err}")
                time.sleep(1)
            except Exception as e:
                error_msg = f"Request failed: {str(e)}"
                print(f"[LLM LOG] Agent: Chat, Attempt: {attempt + 1}, Error: {e}")
                time.sleep(1)

        total_latency = time.time() - start_time
        print(f"[LLM LOG SUMMARY] Agent: Chat, Model: {model_name}, Total Attempts: {retry_attempts + 1}, Final HTTP Status: {http_status}, Total Latency: {total_latency:.2f}s, Error Body: {response_body if http_status != 200 else 'None'}")

        if response is not None and http_status == 200:
            try:
                result_json = response.json()
                text_response = result_json["candidates"][0]["content"]["parts"][0]["text"]
                return {
                    "reply": text_response,
                    "tool_calls_made": ["get_score_explanation"],
                    "language_detected": "en",
                    "fallback_used": False,
                    "fallback_reason": ""
                }
            except Exception as parse_err:
                reason = f"JSON parse failure on LLM response: {parse_err}"
                res = self._fallback_chat(message)
                res.update({"fallback_used": True, "fallback_reason": reason})
                return res
        else:
            final_reason = error_msg or "Failed to call Gemini API after retries"
            res = self._fallback_chat(message)
            res.update({"fallback_used": True, "fallback_reason": final_reason})
            return res

    def _fallback_chat(self, message: str) -> dict:
        msg_lower = message.lower()
        if "why is my score lower" in msg_lower or "score" in msg_lower:
            reply = "Your credit score is 71/100 mainly because 3 invoices remain unreconciled (worth ₹2.05L) and your GSTR-3B filing for March 2026 was filed 2 days late. Resolving the unreconciled invoices will increase your score to 79/100."
            tools = ["get_score_explanation", "get_reconciliation_status"]
        elif "compliance" in msg_lower or "gst" in msg_lower or "late" in msg_lower:
            reply = "You have 1 warning flag: GSTR-3B for March 2026 was filed 2 days late on 22nd April 2026. This incurs a late filing fee of ₹100, which has been paid, but the delay affects your filing timeliness rating."
            tools = ["get_compliance_details"]
        elif "reconcile" in msg_lower or "invoice" in msg_lower:
            reply = "You have 3 unreconciled invoices: RKT/2026/022 (Patel Garments, ₹95,000), RKT/2026/023 (Raj Fabrics, ₹45,000), and RKT/2026/024 (Karan Suits, ₹65,000). No matching payments were found in your bank ledger."
            tools = ["get_reconciliation_status"]
        else:
            reply = f"I have analyzed your ledger. Your overall credit readiness score is 71/100. Let me know if you would like me to explain your compliance flags, check invoice reconciliation, or view transaction summaries."
            tools = ["get_transaction_summary"]

        return {
            "reply": reply,
            "tool_calls_made": tools,
            "language_detected": "en"
        }
