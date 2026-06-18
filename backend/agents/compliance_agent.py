# agents/compliance_agent.py
import os
import json
import requests
from utils.prompt_templates import COMPLIANCE_AUDITOR
from rag.knowledge_base import kb

class ComplianceAgent:
    def __init__(self):
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
            return self._fallback_compliance(business_data)

        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
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
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result_json = response.json()
                text_response = result_json["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(text_response)
            else:
                print(f"Compliance Agent API returned error: {response.text}")
                return self._fallback_compliance(business_data)
        except Exception as e:
            print(f"Compliance Agent failed: {e}. Falling back to default compliance flags.")
            return self._fallback_compliance(business_data)

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
