# db/models.py
import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Float, Boolean, DateTime, Date, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class Business(Base):
    __tablename__ = "businesses"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    gstin = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    demo_mode = Column(Boolean, default=False)

    documents = relationship("Document", back_populates="business", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="business", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="business", cascade="all, delete-orphan")
    compliance_flags = relationship("ComplianceFlag", back_populates="business", cascade="all, delete-orphan")
    credit_scores = relationship("CreditScore", back_populates="business", cascade="all, delete-orphan")
    agent_trace_logs = relationship("AgentTraceLog", back_populates="business", cascade="all, delete-orphan")


class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True, default=generate_uuid)
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    doc_type = Column(String, nullable=False)  # "bank_statement" | "invoice" | "gst_return"
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    upload_time = Column(DateTime, default=datetime.utcnow)
    extraction_status = Column(String, default="pending")  # "pending" | "processing" | "done" | "error"
    extracted_json = Column(JSON, nullable=True)

    business = relationship("Business", back_populates="documents")
    transactions = relationship("Transaction", back_populates="document", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="document", cascade="all, delete-orphan")


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True, default=generate_uuid)
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    source_document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    txn_date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    txn_type = Column(String, nullable=False)  # "credit" | "debit"
    category = Column(String, default="other")  # "sales" | "purchase" | "tax" | "salary" | "other"
    reconciled = Column(Boolean, default=False)
    invoice_match_id = Column(String, ForeignKey("invoices.id"), nullable=True)

    business = relationship("Business", back_populates="transactions")
    document = relationship("Document", back_populates="transactions")
    matched_invoice = relationship("Invoice", foreign_keys=[invoice_match_id])


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(String, primary_key=True, default=generate_uuid)
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    source_document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    invoice_number = Column(String, nullable=False)
    invoice_date = Column(Date, nullable=False)
    vendor_or_customer = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    gst_amount = Column(Float, nullable=False)
    gst_rate = Column(Float, nullable=False)
    hsn_code = Column(String, nullable=True)
    reconciled = Column(Boolean, default=False)

    business = relationship("Business", back_populates="invoices")
    document = relationship("Document", back_populates="invoices")


class ComplianceFlag(Base):
    __tablename__ = "compliance_flags"
    id = Column(String, primary_key=True, default=generate_uuid)
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    flag_type = Column(String, nullable=False)  # "missing_filing" | "late_filing" | "rate_mismatch" | "threshold_breach" | "info"
    severity = Column(String, nullable=False)  # "critical" | "warning" | "info"
    description = Column(String, nullable=False)
    rule_reference = Column(String, nullable=True)
    rag_source_chunk = Column(String, nullable=True)
    detected_at = Column(DateTime, default=datetime.utcnow)
    resolved = Column(Boolean, default=False)

    business = relationship("Business", back_populates="compliance_flags")


class CreditScore(Base):
    __tablename__ = "credit_scores"
    id = Column(String, primary_key=True, default=generate_uuid)
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    score = Column(Float, nullable=False)
    computed_at = Column(DateTime, default=datetime.utcnow)
    filing_rate = Column(Float, default=1.0)
    on_time_rate = Column(Float, default=1.0)
    reconciliation_rate = Column(Float, default=1.0)
    revenue_trend = Column(String, default="stable")  # "growing" | "stable" | "declining"
    transaction_consistency = Column(Float, default=1.0)
    compliance_penalty = Column(Float, default=0.0)
    explanation_json = Column(JSON, nullable=True)
    version = Column(String, default="1")

    business = relationship("Business", back_populates="credit_scores")


class AgentTraceLog(Base):
    __tablename__ = "agent_trace_logs"
    id = Column(String, primary_key=True, default=generate_uuid)
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    job_id = Column(String, nullable=False)
    agent_name = Column(String, nullable=False)  # "extraction" | "compliance" | "reconciliation" | "scoring" | "orchestrator"
    step_number = Column(String, default="1")
    input_summary = Column(String, nullable=True)
    output_summary = Column(String, nullable=True)
    reasoning = Column(String, nullable=True)
    status = Column(String, nullable=False)  # "running" | "done" | "error"
    duration_ms = Column(String, default="0")
    timestamp = Column(DateTime, default=datetime.utcnow)

    business = relationship("Business", back_populates="agent_trace_logs")
