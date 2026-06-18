# api/demo.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from backend.db.session import get_db
from backend.db.models import Business, Document, Transaction, Invoice, ComplianceFlag, CreditScore, AgentTraceLog
from backend.demo.seed_data import DEMO_BUSINESS, DEMO_BANK_TRANSACTIONS, DEMO_INVOICES, DEMO_GST_RETURN
from backend.agents.orchestrator import pipeline

router = APIRouter(prefix="/api/demo")

@router.post("/reset")
def reset_demo(db: Session = Depends(get_db)):
    """
    Clears all tables and seeds Ravi Kumar's profile and initial state (demo_mode=True).
    Does NOT seed the extracted details so the processing flow can be demonstrated live.
    """
    # Delete related records
    db.query(AgentTraceLog).delete()
    db.query(CreditScore).delete()
    db.query(ComplianceFlag).delete()
    db.query(Transaction).delete()
    db.query(Invoice).delete()
    db.query(Document).delete()
    db.query(Business).delete()
    db.commit()

    # Create Ravi Kumar's business
    business = Business(
        name=DEMO_BUSINESS["name"],
        gstin=DEMO_BUSINESS["gstin"],
        email=DEMO_BUSINESS["email"],
        phone=DEMO_BUSINESS["phone"],
        demo_mode=True
    )
    db.add(business)
    db.commit()
    db.refresh(business)

    # Pre-add documents with a simulated "uploaded" status.
    # The actual pdf files can reside as placeholders, we save references.
    docs_to_create = [
        {"filename": "bank_statement_ravi.pdf", "doc_type": "bank_statement"},
        {"filename": "invoice_001_ravi.pdf", "doc_type": "invoice"},
        {"filename": "invoice_002_ravi.pdf", "doc_type": "invoice"},
        {"filename": "gst_return_ravi.pdf", "doc_type": "gst_return"}
    ]

    created_docs = []
    for d in docs_to_create:
        doc = Document(
            business_id=business.id,
            doc_type=d["doc_type"],
            filename=d["filename"],
            file_path=f"./backend/demo/synthetic_docs/{d['filename']}",
            extraction_status="pending"
        )
        db.add(doc)
        created_docs.append(doc)
    db.commit()

    return {
        "status": "success",
        "message": "Demo database reset and seeded with Ravi Kumar Textiles metadata.",
        "business_id": business.id,
        "documents": [{"id": doc.id, "filename": doc.filename, "type": doc.doc_type} for doc in created_docs]
    }


@router.get("/run")
def run_full_demo(business_id: str, db: Session = Depends(get_db)):
    """
    Convenience run-through: triggers pipeline and returns job details.
    """
    import uuid
    job_id = str(uuid.uuid4())
    pipeline.run_pipeline(business_id, job_id)
    return {
        "status": "completed",
        "job_id": job_id,
        "business_id": business_id
    }
