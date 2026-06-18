# api/chat.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from.db.session import get_db
from.db.models import Business, CreditScore, ComplianceFlag, Transaction, Invoice
from.agents.chat_agent import ChatAgent

router = APIRouter(prefix="/api")
chat_agent = ChatAgent()

class ChatRequest(BaseModel):
    business_id: str
    message: str

@router.post("/chat")
def chat_with_advisor(req: ChatRequest, db: Session = Depends(get_db)):
    business = db.query(Business).filter(Business.id == req.business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    # Retrieve score details, flags, transactions and invoices to provide rich contextual parameters
    score = db.query(CreditScore).filter(CreditScore.business_id == req.business_id).first()
    flags = db.query(ComplianceFlag).filter(ComplianceFlag.business_id == req.business_id).all()
    transactions = db.query(Transaction).filter(Transaction.business_id == req.business_id).all()
    invoices = db.query(Invoice).filter(Invoice.business_id == req.business_id).all()

    business_context = {
        "score": score.score if score else 71.0,
        "grade": score.explanation_json.get("grade", "B+") if (score and score.explanation_json) else "B+",
        "factor_breakdown": score.explanation_json.get("factor_breakdown", {}) if (score and score.explanation_json) else {},
        "flags_count": len(flags),
        "flags": [{"flag_type": f.flag_type, "severity": f.severity, "description": f.description} for f in flags],
        "transactions_summary": {
            "total_transactions": len(transactions),
            "credits": sum(t.amount for t in transactions if t.txn_type == "credit"),
            "debits": sum(t.amount for t in transactions if t.txn_type == "debit")
        },
        "invoices_summary": {
            "total_invoices": len(invoices),
            "reconciled": sum(1 for i in invoices if i.reconciled),
            "unreconciled": sum(1 for i in invoices if not i.reconciled)
        }
    }

    response = chat_agent.run(req.message, business_context)
    return response
