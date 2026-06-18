# api/compliance.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from.db.session import get_db
from.db.models import ComplianceFlag, Business

router = APIRouter(prefix="/api")

@router.get("/compliance/{business_id}")
def get_compliance_flags_list(business_id: str, db: Session = Depends(get_db)):
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
        
    flags = db.query(ComplianceFlag).filter(ComplianceFlag.business_id == business_id).all()
    
    return [
        {
            "id": f.id,
            "flag_type": f.flag_type,
            "severity": f.severity,
            "description": f.description,
            "rule_reference": f.rule_reference,
            "rag_source_chunk": f.rag_source_chunk,
            "detected_at": f.detected_at.isoformat() + "Z",
            "resolved": f.resolved
        }
        for f in flags
    ]
