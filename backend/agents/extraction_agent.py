# agents/extraction_agent.py
import json
import os
import requests
from utils.prompt_templates import EXTRACTION_BANK_STATEMENT, EXTRACTION_INVOICE, EXTRACTION_GST_RETURN
from utils.pdf_utils import extract_text_from_pdf

class ExtractionAgent:
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")

    def run(self, file_path: str, doc_type: str) -> dict:
        """
        Parses a document (invoice, bank_statement, gst_return) to extract structured JSON.
        Uses Gemini 1.5 Flash if available, otherwise falls back to a template matching or mock structure.
        """
        text_content = extract_text_from_pdf(file_path)
        
        # Define default template matching prompts
        if doc_type == "bank_statement":
            prompt = EXTRACTION_BANK_STATEMENT
        elif doc_type == "invoice":
            prompt = EXTRACTION_INVOICE
        elif doc_type == "gst_return":
            prompt = EXTRACTION_GST_RETURN
        else:
            raise ValueError(f"Unknown document type: {doc_type}")

        # If Gemini API Key is missing or invalid, generate high-quality fallback responses matching seed data
        if not self.api_key or self.api_key == "your_gemini_api_key":
            reason = "GOOGLE_API_KEY unset" if not self.api_key else "GOOGLE_API_KEY is placeholder"
            return {"data": self._fallback_extraction(doc_type, file_path, text_content=text_content), "fallback_used": True, "fallback_reason": reason}

        model_name = "gemini-3.1-flash-lite"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"{prompt}\n\nDocument Text Content:\n{text_content}"}
                    ]
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json"
            }
        }

        # We will attempt retries (up to 3 times) and log execution latency, latency per call, etc.
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
                
                print(f"[LLM LOG] Agent: Extraction, Model: {model_name}, Attempt: {attempt + 1}, HTTP Status: {http_status}, Latency: {latency_end - latency_start:.2f}s")
                
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
                
                # Sleep briefly before retry
                time.sleep(1)
            except requests.exceptions.Timeout as t_err:
                error_msg = f"Timeout error calling Gemini API: {t_err}"
                print(f"[LLM LOG] Agent: Extraction, Attempt: {attempt + 1}, Timeout Error: {t_err}")
                time.sleep(1)
            except Exception as e:
                error_msg = f"Request failed: {str(e)}"
                print(f"[LLM LOG] Agent: Extraction, Attempt: {attempt + 1}, Error: {e}")
                time.sleep(1)

        total_latency = time.time() - start_time
        print(f"[LLM LOG SUMMARY] Agent: Extraction, Model: {model_name}, Total Attempts: {retry_attempts + 1}, Final HTTP Status: {http_status}, Total Latency: {total_latency:.2f}s, Error Body: {response_body if http_status != 200 else 'None'}")

        if response is not None and http_status == 200:
            try:
                result_json = response.json()
                text_response = result_json["candidates"][0]["content"]["parts"][0]["text"]
                parsed_json = json.loads(text_response)
                return {"data": parsed_json, "fallback_used": False, "fallback_reason": ""}
            except Exception as parse_err:
                reason = f"JSON parse failure on LLM output: {parse_err}"
                print(f"[LLM ERROR] {reason}")
                return {"data": self._fallback_extraction(doc_type, file_path, text_content=text_content), "fallback_used": True, "fallback_reason": reason}
        else:
            final_reason = error_msg or "Failed to call Gemini API after retries"
            return {"data": self._fallback_extraction(doc_type, file_path, text_content=text_content), "fallback_used": True, "fallback_reason": final_reason}

    def _fallback_extraction(self, doc_type: str, file_path: str, text_content: str = "") -> dict:
        filename = os.path.basename(file_path).lower()
        
        # High quality mocks mirroring seed data if the filename indicates Ravi Kumar's files
        if "bank_statement" in filename or "bank" in filename:
            from demo.seed_data import DEMO_BANK_TRANSACTIONS
            return {
                "account_holder": "Ravi Kumar Textiles",
                "account_number_last4": "5432",
                "statement_period": { "from": "2026-01-01", "to": "2026-03-31" },
                "opening_balance": 150000.0,
                "closing_balance": 285400.0,
                "transactions": DEMO_BANK_TRANSACTIONS
            }
        
        elif "invoice_001" in filename or "001" in filename:
            return {
                "invoice_number": "RKT/2026/001",
                "invoice_date": "2026-01-05",
                "seller_name": "Ravi Kumar Textiles",
                "seller_gstin": "27AABCU9603R1ZM",
                "buyer_name": "Mehta Fabrics",
                "buyer_gstin": "27BBBCU9603R1ZN",
                "line_items": [
                    { "description": "Printed Cotton Fabric", "hsn_code": "5208", "quantity": 1000.0, "unit_price": 185.0 }
                ],
                "subtotal": 185000.0,
                "total_gst": 33300.0,
                "grand_total": 218300.0,
                "payment_terms": "Net 30"
            }

        elif "invoice_002" in filename or "002" in filename or "invoice" in filename:
            # General invoice fallback
            return {
                "invoice_number": "RKT/2026/022",
                "invoice_date": "2026-03-20",
                "seller_name": "Ravi Kumar Textiles",
                "seller_gstin": "27AABCU9603R1ZM",
                "buyer_name": "Patel Garments",
                "buyer_gstin": "27CCCU9603R1ZP",
                "line_items": [
                    { "description": "Designer Cotton Suits", "hsn_code": "5209", "quantity": 500.0, "unit_price": 190.0 }
                ],
                "subtotal": 95000.0,
                "total_gst": 17100.0,
                "grand_total": 112100.0,
                "payment_terms": "Net 15"
            }

        elif "gst" in filename or "return" in filename:
            from demo.seed_data import DEMO_GST_RETURN
            return DEMO_GST_RETURN
            
        else:
            # General default structure
            return {"status": "unsupported", "raw_extracted_text": text_content[:500] if text_content else ""}
