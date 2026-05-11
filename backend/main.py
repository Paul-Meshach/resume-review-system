# This is the heart of your FastAPI app
# Everything gets wired together here

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import engine, Base
import models.user, models.candidate, models.review, models.notification  # Import to register models
from routers import auth, resumes, tls, reviews, notifications
import os

# Create all DB tables on startup
# In production, use Alembic migrations instead
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Resume Review Workflow API",
    description="End-to-end resume review system",
    version="1.0.0"
)

# CORS — allows your React app (port 5173) to call this API (port 8000)
# Without this, browsers block cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded files (so frontend can preview resumes)
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Register all routers — each adds its own prefix
app.include_router(auth.router)
app.include_router(resumes.router)
app.include_router(tls.router)
app.include_router(reviews.router)
app.include_router(notifications.router)

@app.get("/")
def health_check():
    return {"status": "Resume Review API is running ✅"}

# Run with: uvicorn main:app --reload