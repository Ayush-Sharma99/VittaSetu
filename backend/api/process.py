# api/process.py
import uuid
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.db.models import Business
from backend.agents.orchestrator import pipeline

router = APIRouter(prefix="/api")

@router.post("/process")
def trigger_pipeline(
    business_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    # Generate a unique job ID to track this pipeline run
    job_id = str(uuid.uuid4())

    # Trigger pipeline in background
    background_tasks.add_task(pipeline.run_pipeline, business_id=business_id, job_id=job_id)

    return {
        "job_id": job_id,
        "business_id": business_id,
        "status": "processing"
    }
