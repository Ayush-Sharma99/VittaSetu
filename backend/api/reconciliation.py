# api/reconciliation.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.db.models import Invoice, Business

router = APIRouter(prefix="/api")

@router.get("/reconciliation/{business_id}")
def get_invoices_reconciliation_list(business_id: str, db: Session = Depends(get_db)):
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
        
    invoices = db.query(Invoice).filter(Invoice.business_id == business_id).all()
    
    return [
        {
            "id": inv.id,
            "invoice_number": inv.invoice_number,
            "invoice_date": inv.invoice_date.isoformat(),
            "vendor_or_customer": inv.vendor_or_customer,
            "amount": inv.amount,
            "gst_amount": inv.gst_amount,
            "gst_rate": inv.gst_rate,
            "hsn_code": inv.hsn_code,
            "reconciled": inv.reconciled
        }
        for inv in invoices
    ]
