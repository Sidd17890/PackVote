from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Place
from ..ml.recommender import PlaceRecommender
import requests
import os

router = APIRouter()
recommender = PlaceRecommender()

@router.get("/search")
def search_places(
    q: str,
    city: Optional[str] = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Search places by name or city"""
    query = db.query(Place)
    
    if q:
        query = query.filter(Place.name.ilike(f"%{q}%"))
    if city:
        query = query.filter(Place.city.ilike(f"%{city}%"))
    
    places = query.limit(limit).all()
    
    # If no results, fetch from Google Places API
    if not places and os.getenv("GOOGLE_PLACES_API_KEY"):
        places = fetch_from_google_places(q, city)
    
    return places

@router.get("/recommendations/{place_id}")
def get_recommendations(
    place_id: int,
    n: int = 10,
    db: Session = Depends(get_db)
):
    """Get AI-powered place recommendations"""
    recommendations = recommender.recommend(place_id, db, n)
    
    # Fetch full place details
    result = []
    for rec in recommendations:
        place = db.query(Place).filter(Place.id == rec['place_id']).first()
        if place:
            result.append({
                'place': place,
                'similarity': rec['similarity_score']
            })
    
    return result

@router.get("/city/{city}")
def get_city_places(
    city: str,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get top places in a city"""
    places = recommender.recommend_for_city(city, db, limit)
    return places

def fetch_from_google_places(query: str, city: str = None):
    """Fallback to Google Places API"""
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    search_query = f"{query} {city}" if city else query
    
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": search_query,
        "key": api_key
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []
