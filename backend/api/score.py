# api/score.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from db.models import CreditScore, ComplianceFlag, Business

router = APIRouter(prefix="/api")

@router.get("/score/{business_id}")
def get_credit_passport(business_id: str, db: Session = Depends(get_db)):
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    score = db.query(CreditScore).filter(CreditScore.business_id == business_id).order_by(CreditScore.computed_at.desc()).first()
    if not score:
        raise HTTPException(status_code=404, detail="Credit score details not computed yet")

    flags = db.query(ComplianceFlag).filter(ComplianceFlag.business_id == business_id).all()
    
    # Check if any agent has used fallback
    from db.models import AgentTraceLog
    fallback_logs = db.query(AgentTraceLog).filter(
        AgentTraceLog.business_id == business_id,
        AgentTraceLog.status == "fallback_used"
    ).all()
    using_fallback = len(fallback_logs) > 0

    # Compute average monthly revenue from transaction credits
    from db.models import Transaction
    from collections import defaultdict
    txns = db.query(Transaction).filter(Transaction.business_id == business_id).all()
    monthly_credits = defaultdict(float)
    for t in txns:
        if t.txn_type.lower() == "credit":
            month_str = t.txn_date.strftime("%Y-%m")
            monthly_credits[month_str] += t.amount
    avg_monthly_revenue = sum(monthly_credits.values()) / len(monthly_credits) if monthly_credits else 0.0

    explanation_data = score.explanation_json or {}

    return {
        "business_id": business_id,
        "business_name": business.name,
        "gstin": business.gstin,
        "score": score.score,
        "using_fallback": using_fallback,
        "demo_mode": business.demo_mode,
        "filing_rate": score.filing_rate,
        "reconciliation_rate": score.reconciliation_rate,
        "on_time_rate": score.on_time_rate,
        "avg_monthly_revenue": avg_monthly_revenue,
        "computed_at": score.computed_at.isoformat() + "Z",
        "factor_breakdown": score.explanation_json.get("factor_breakdown", {}) if score.explanation_json else {
            "filing_compliance": score.filing_rate * 20.0,
            "filing_timeliness": score.on_time_rate * 15.0,
            "invoice_reconciliation": score.reconciliation_rate * 20.0,
            "revenue_trend": 15.0,
            "cash_flow_consistency": score.transaction_consistency * 15.0,
            "compliance_health": 15.0
        },
        "explanation": explanation_data.get("explanation", "Your score breakdown is computed based on recent business ledgers."),
        "top_strength": explanation_data.get("top_strength", "Strong GST Compliance"),
        "top_action": explanation_data.get("top_action", "Reconcile outstanding invoices"),
        "compliance_flags": [
            {
                "flag_type": f.flag_type,
                "severity": f.severity,
                "description": f.description,
                "rule_reference": f.rule_reference,
                "rag_source_chunk": f.rag_source_chunk,
                "detected_at": f.detected_at.isoformat() + "Z",
                "resolved": f.resolved
            }
            for f in flags
        ],
        "grade": explanation_data.get("grade", "B+")
    }
