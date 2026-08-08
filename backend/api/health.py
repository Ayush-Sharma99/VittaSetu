# api/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from db.models import AgentTraceLog

router = APIRouter(prefix="/api")

@router.get("/health/agents")
def get_agents_health(db: Session = Depends(get_db)):
    agents = ["extraction", "compliance", "reconciliation", "scoring", "chat"]
    health_status = {}

    for agent in agents:
        # Find the latest log for the agent
        latest_log = db.query(AgentTraceLog).filter(
            AgentTraceLog.agent_name == agent
        ).order_by(AgentTraceLog.timestamp.desc()).first()

        if not latest_log:
            health_status[agent] = {
                "status": "unknown",
                "message": "Agent has not been executed yet.",
                "fallback_used": False,
                "reason": None
            }
        else:
            # Check if fallback was used in the latest job for this agent
            fallback_log = db.query(AgentTraceLog).filter(
                AgentTraceLog.agent_name == agent,
                AgentTraceLog.job_id == latest_log.job_id,
                AgentTraceLog.status == "fallback_used"
            ).first()

            if fallback_log:
                health_status[agent] = {
                    "status": "fallback_active",
                    "message": "Agent is currently using fallback/mock data.",
                    "fallback_used": True,
                    "reason": fallback_log.reasoning,
                    "last_run": latest_log.timestamp.isoformat()
                }
            else:
                health_status[agent] = {
                    "status": "healthy",
                    "message": "Agent completed successfully on last run.",
                    "fallback_used": False,
                    "reason": None,
                    "last_run": latest_log.timestamp.isoformat()
                }

    return health_status
