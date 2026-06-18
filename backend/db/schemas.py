# db/schemas.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from typing import List, Optional, Dict, Any

class BusinessBase(BaseModel):
    name: str
    gstin: Optional[str] = None
    email: str
    phone: Optional[str] = None
    demo_mode: bool = False

class BusinessCreate(BusinessBase):
    pass

class BusinessSchema(BusinessBase):
    id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class DocumentBase(BaseModel):
    business_id: str
    doc_type: str
    filename: str
    file_path: str
    extraction_status: str = "pending"
    extracted_json: Optional[Dict[str, Any]] = None

class DocumentSchema(DocumentBase):
    id: str
    upload_time: datetime
    model_config = ConfigDict(from_attributes=True)

class TransactionBase(BaseModel):
    business_id: str
    source_document_id: Optional[str] = None
    txn_date: date
    description: str
    amount: float
    txn_type: str
    category: str = "other"
    reconciled: bool = False
    invoice_match_id: Optional[str] = None

class TransactionSchema(TransactionBase):
    id: str
    model_config = ConfigDict(from_attributes=True)

class InvoiceBase(BaseModel):
    business_id: str
    source_document_id: Optional[str] = None
    invoice_number: str
    invoice_date: date
    vendor_or_customer: str
    amount: float
    gst_amount: float
    gst_rate: float
    hsn_code: Optional[str] = None
    reconciled: bool = False

class InvoiceSchema(InvoiceBase):
    id: str
    model_config = ConfigDict(from_attributes=True)

class ComplianceFlagBase(BaseModel):
    business_id: str
    flag_type: str
    severity: str
    description: str
    rule_reference: Optional[str] = None
    rag_source_chunk: Optional[str] = None
    resolved: bool = False

class ComplianceFlagSchema(ComplianceFlagBase):
    id: str
    detected_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CreditScoreBase(BaseModel):
    business_id: str
    score: float
    filing_rate: float
    on_time_rate: float
    reconciliation_rate: float
    revenue_trend: str
    transaction_consistency: float
    compliance_penalty: float
    explanation_json: Optional[Dict[str, Any]] = None
    version: str = "1"

class CreditScoreSchema(CreditScoreBase):
    id: str
    computed_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AgentTraceLogBase(BaseModel):
    business_id: str
    job_id: str
    agent_name: str
    step_number: str
    input_summary: Optional[str] = None
    output_summary: Optional[str] = None
    reasoning: Optional[str] = None
    status: str
    duration_ms: str

class AgentTraceLogSchema(AgentTraceLogBase):
    id: str
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
