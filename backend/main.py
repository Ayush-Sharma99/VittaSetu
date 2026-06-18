# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.session import init_db
from api import upload, process, status, score, chat, demo, compliance, reconciliation

# Initialize SQLite database schema
init_db()

app = FastAPI(
    title="VittaSetu AI API",
    description="Financial system of record for India's 63 million MSMEs",
    version="1.0.0"
)

# CORS configurations
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001,https://vittasetu.vercel.app")
origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(upload.router)
app.include_router(process.router)
app.include_router(status.router)
app.include_router(score.router)
app.include_router(chat.router)
app.include_router(demo.router)
app.include_router(compliance.router)
app.include_router(reconciliation.router)

@app.get("/")
def read_root():
    return {"name": "VittaSetu AI API", "status": "running"}
