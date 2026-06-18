# api/status.py
import json
import asyncio
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from.db.session import get_db
from.db.models import AgentTraceLog

router = APIRouter(prefix="/api")

@router.get("/status/{job_id}")
async def get_job_status(job_id: str, db: Session = Depends(get_db)):
    """
    Streams AgentTraceLog events for the given job_id as Server-Sent Events (SSE) or queries them dynamically.
    For polling simplification, if SSE headers are not explicitly required, we return a list,
    but here we implement full SSE streaming support to meet the specification exactly.
    """
    async def event_generator():
        sent_ids = set()
        completed = False
        retry_count = 0
        
        while not completed and retry_count < 300:
            # Re-fetch logs inside loop to pick up background process updates
            # Create a localized session for async usage
            from.db.session import SessionLocal
            loop_db = SessionLocal()
            try:
                logs = loop_db.query(AgentTraceLog).filter(
                    AgentTraceLog.job_id == job_id
                ).order_by(AgentTraceLog.timestamp.asc()).all()
                
                for log in logs:
                    if log.id not in sent_ids:
                        data = {
                            "agent": log.agent_name,
                            "step": int(log.step_number),
                            "status": log.status,
                            "message": log.output_summary if log.status == "done" else log.input_summary,
                            "reasoning": log.reasoning,
                            "duration": log.duration_ms
                        }
                        yield f"data: {json.dumps(data)}\n\n"
                        sent_ids.add(log.id)
                        
                        # Stop generator once scoring step is finished/completed
                        if log.agent_name == "scoring" and log.status == "done":
                            completed = True
                            yield f"data: {json.dumps({'type': 'complete', 'redirect': '/dashboard'})}\n\n"
                            break
            except Exception as e:
                print(f"SSE loop error: {e}")
            finally:
                loop_db.close()
                
            if not completed:
                await asyncio.sleep(0.5)
                retry_count += 1
                
    return StreamingResponse(event_generator(), media_type="text/event-stream")
