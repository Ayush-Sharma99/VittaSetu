# utils/prompt_templates.py

EXTRACTION_BANK_STATEMENT = """You are a financial document extraction specialist. Extract ALL transactions from this bank statement.
Return a JSON object with this exact schema:
{{
  "account_holder": "string",
  "account_number_last4": "string",
  "statement_period": {{ "from": "YYYY-MM-DD", "to": "YYYY-MM-DD" }},
  "opening_balance": 0.0,
  "closing_balance": 0.0,
  "transactions": [
    {{
      "date": "YYYY-MM-DD",
      "description": "string",
      "amount": 0.0,
      "type": "credit" | "debit",
      "balance_after": 0.0
    }}
  ]
}}
Do not hallucinate. If a field is not visible, use null. Extract every single transaction."""

EXTRACTION_INVOICE = """Extract structured data from this invoice image or PDF.
Return JSON:
{{
  "invoice_number": "string",
  "invoice_date": "YYYY-MM-DD",
  "seller_name": "string",
  "seller_gstin": "string or null",
  "buyer_name": "string",
  "buyer_gstin": "string or null",
  "line_items": [
    {{ "description": "string", "hsn_code": "string or null", "quantity": 0.0, "unit_price": 0.0 }}
  ],
  "subtotal": 0.0,
  "total_gst": 0.0,
  "grand_total": 0.0,
  "payment_terms": "string or null"
}}"""

EXTRACTION_GST_RETURN = """Extract filing data from this GST return document (GSTR-1, GSTR-3B, or similar).
Return JSON:
{{
  "return_type": "GSTR-1" | "GSTR-3B" | "GSTR-9" | "other",
  "filing_period": "string",
  "filing_date": "YYYY-MM-DD" or null,
  "gstin": "string",
  "taxable_turnover": 0.0,
  "total_tax_liability": 0.0,
  "tax_paid": 0.0,
  "late_fee": 0.0 or null,
  "status": "filed" | "pending" | "nil"
}}"""

COMPLIANCE_AUDITOR = """You are a GST compliance auditor. Given the retrieved rule context and the business's data:

RETRIEVED RULE CONTEXT:
{rag_context}

BUSINESS FINANCIAL DATA:
{financial_data_json}

For each compliance issue found, output a JSON array:
[{{
  "flag_type": "missing_filing" | "late_filing" | "rate_mismatch" | "threshold_breach" | "info",
  "severity": "critical" | "warning" | "info",
  "description": "plain English explanation of the issue (max 2 sentences)",
  "rule_reference": "exact rule name/number from the retrieved context",
  "rag_source_chunk": "the specific retrieved text that grounds this finding"
}}]

If no issues are found, return an empty array []. Do not hallucinate rules not present in the context."""

RECONCILIATION_FUZZY = """Match the following unmatched invoices to unmatched bank transactions where possible:

UNMATCHED INVOICES:
{invoices_json}

UNMATCHED BANK TRANSACTIONS:
{transactions_json}

Return JSON:
[{{
  "invoice_id": "string",
  "matched_transaction_id": "string or null",
  "confidence": "high" | "medium" | "low",
  "reasoning": "one sentence explanation"
}}]

Only match if reasonably confident. Return null for matched_transaction_id if no suitable transaction matches."""

CREDIT_SCORING_EXPLANATION = """You are an AI credit advisor for Indian MSMEs. Given a business's credit score breakdown:

SCORE: {score}/100
FACTOR BREAKDOWN: {factor_breakdown_json}
COMPLIANCE FLAGS: {flags_summary}

Write the explanation for the business owner. Use plain English (no jargon). Mention their top strength and top actionable area.
Output format: {{ "explanation": "...", "top_strength": "...", "top_action": "..." }}"""

CHAT_SYSTEM_PROMPT = """You are VittaSetu AI, a helpful financial advisor for small Indian businesses. 

Business context:
{business_context_json}

You can call these tools to get details:
- get_compliance_details: returns specific compliance flag details
- get_reconciliation_status: returns invoice matching status
- get_score_explanation: returns credit score factor breakdown
- get_transaction_summary: returns transaction statistics for a time period

Answer in plain English. Be specific — always use actual numbers from the data. Keep answers simple, short and easy to digest.
If the user writes in Hindi, respond in Hindi."""
