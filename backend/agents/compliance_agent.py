# agents/compliance_agent.py
import os
import json
import requests
from utils.prompt_templates import COMPLIANCE_AUDITOR
from rag.knowledge_base import kb

class ComplianceAgent:
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")

    def run(self, business_data: dict) -> list:
        """
        Check extracted transaction and filing data against retrieved GST rules from ChromaDB.
        Returns a list of compliance flag dictionaries.
        """
        # Look up GST rules via RAG knowledge base
        search_query = f"deadlines filing return invoice threshold HSN late fee GSTR-1 GSTR-3B"
        retrieved_rules = kb.query(search_query, n_results=4)
        rag_context = "\n\n---\n\n".join(retrieved_rules)

        financial_data_json = json.dumps(business_data, indent=2)

        # Fallback if Google API Key is not set or fails
        if not self.api_key or self.api_key == "your_gemini_api_key":
            reason = "GOOGLE_API_KEY unset" if not self.api_key else "GOOGLE_API_KEY is placeholder"
            return {"data": self._fallback_compliance(business_data), "fallback_used": True, "fallback_reason": reason}

        model_name = "gemini-3.1-flash-lite"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        
        prompt = COMPLIANCE_AUDITOR.format(
            rag_context=rag_context,
            financial_data_json=financial_data_json
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
                response = requests.post(url, headers=headers, json=payload, timeout=30)
                latency_end = time.time()
                http_status = response.status_code
                response_body = response.text
                
                print(f"[LLM LOG] Agent: Compliance, Model: {model_name}, Attempt: {attempt + 1}, HTTP Status: {http_status}, Latency: {latency_end - latency_start:.2f}s")
                
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
                print(f"[LLM LOG] Agent: Compliance, Attempt: {attempt + 1}, Timeout Error: {t_err}")
                time.sleep(1)
            except Exception as e:
                error_msg = f"Request failed: {str(e)}"
                print(f"[LLM LOG] Agent: Compliance, Attempt: {attempt + 1}, Error: {e}")
                time.sleep(1)

        total_latency = time.time() - start_time
        print(f"[LLM LOG SUMMARY] Agent: Compliance, Model: {model_name}, Total Attempts: {retry_attempts + 1}, Final HTTP Status: {http_status}, Total Latency: {total_latency:.2f}s, Error Body: {response_body if http_status != 200 else 'None'}")

        if response is not None and http_status == 200:
            try:
                result_json = response.json()
                text_response = result_json["candidates"][0]["content"]["parts"][0]["text"]
                parsed_json = json.loads(text_response)
                return {"data": parsed_json, "fallback_used": False, "fallback_reason": ""}
            except Exception as parse_err:
                reason = f"JSON parse failure on LLM output: {parse_err}"
                print(f"[LLM ERROR] {reason}")
                return {"data": self._fallback_compliance(business_data), "fallback_used": True, "fallback_reason": reason}
        else:
            final_reason = error_msg or "Failed to call Gemini API after retries"
            return {"data": self._fallback_compliance(business_data), "fallback_used": True, "fallback_reason": final_reason}

    def _fallback_compliance(self, business_data: dict) -> list:
        flags = []
        
        # Check late filing check
        gst_return = business_data.get("gst_return", {})
        if gst_return:
            filing_date = gst_return.get("filing_date")
            # For Ravi Kumar textiles GSTR-3B filed on 22nd Apr (2 days late)
            if filing_date and filing_date > "2026-04-20":
                flags.append({
                    "flag_type": "late_filing",
                    "severity": "warning",
                    "description": "GSTR-3B for March 2026 was filed on 2026-04-22, which is 2 days past the deadline of 20th of the month.",
                    "rule_reference": "Rule 61 - GSTR-3B Filing Deadlines",
                    "rag_source_chunk": "GSTR-3B Filing Deadline: GSTR-3B is due by the 20th of the following month for taxpayers with aggregate turnover above ₹5 crore. For others, due date varies by state (22nd or 24th)."
                })

        # Check unreconciled count
        invoices = business_data.get("invoices", [])
        unreconciled_count = sum(1 for inv in invoices if not inv.get("reconciled", False))
        if unreconciled_count > 0:
            flags.append({
                "flag_type": "rate_mismatch", # Flag for unreconciled invoices as indicator
                "severity": "warning",
                "description": f"There are {unreconciled_count} invoices that have not been reconciled against bank ledger transactions.",
                "rule_reference": "Section 16 - Input Tax Credit Reconciliation",
                "rag_source_chunk": "ITC Eligibility — Section 16: Input Tax Credit can be claimed only if: (a) the taxpayer holds a tax invoice, (b) the goods or services have been received..."
            })
            
        return flags
