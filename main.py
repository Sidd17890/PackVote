from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models, routers
from .ml.recommender import PlaceRecommender
from .ml.budget_predictor import BudgetPredictor
import logging

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="PackVote API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ML models
recommender = PlaceRecommender()
budget_predictor = BudgetPredictor()

# Include routers
app.include_router(routers.auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(routers.places.router, prefix="/api/places", tags=["places"])
app.include_router(routers.itineraries.router, prefix="/api/itineraries", tags=["itineraries"])
app.include_router(routers.votes.router, prefix="/api/votes", tags=["votes"])

@app.on_event("startup")
async def startup_event():
    logging.info("Loading ML models...")
    recommender.load_model()
    budget_predictor.load_model()

@app.get("/")
def root():
    return {"message": "Welcome to PackVote API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
