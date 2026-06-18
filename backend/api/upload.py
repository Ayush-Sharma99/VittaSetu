# api/upload.py
import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from db.models import Document, Business

router = APIRouter(prefix="/api")

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploaded_docs")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    doc_type: str = Form(...), # "bank_statement" | "invoice" | "gst_return"
    business_id: str = Form(...),
    db: Session = Depends(get_db)
):
    if doc_type not in ["bank_statement", "invoice", "gst_return"]:
        raise HTTPException(status_code=400, detail="Invalid doc_type parameter")

    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    target_path = os.path.join(UPLOAD_DIR, unique_filename)

    try:
        with open(target_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write file: {str(e)}")

    doc = Document(
        business_id=business_id,
        doc_type=doc_type,
        filename=file.filename,
        file_path=target_path,
        extraction_status="pending"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {
        "document_id": doc.id,
        "filename": doc.filename,
        "status": "uploaded"
    }
