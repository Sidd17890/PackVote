import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Place, Vote
import pickle
import os

class PlaceRecommender:
    def __init__(self):
        self.tfidf_matrix = None
        self.place_ids = None
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        
    def train(self, db: Session):
        """Train content-based recommender"""
        places = db.query(Place).all()
        
        if not places:
            return
            
        # Create feature matrix from place descriptions and tags
        features = []
        for place in places:
            tags_str = ' '.join(place.tags) if place.tags else ''
            feature_text = f"{place.name} {place.description} {tags_str}"
            features.append(feature_text)
        
        self.tfidf_matrix = self.vectorizer.fit_transform(features)
        self.place_ids = [p.id for p in places]
        
        # Save model
        os.makedirs('app/ml/models', exist_ok=True)
        with open('app/ml/models/recommender_model.pkl', 'wb') as f:
            pickle.dump({
                'tfidf_matrix': self.tfidf_matrix,
                'place_ids': self.place_ids,
                'vectorizer': self.vectorizer
            }, f)
    
    def load_model(self):
        """Load trained model"""
        model_path = 'app/ml/models/recommender_model.pkl'
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                data = pickle.load(f)
                self.tfidf_matrix = data['tfidf_matrix']
                self.place_ids = data['place_ids']
                self.vectorizer = data['vectorizer']
    
    def recommend(self, place_id: int, db: Session, n_recommendations: int = 10):
        """Get similar place recommendations"""
        if place_id not in self.place_ids:
            return []
            
        idx = self.place_ids.index(place_id)
        sim_scores = cosine_similarity(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()
        
        # Get top N similar places (excluding itself)
        similar_indices = sim_scores.argsort()[::-1][1:n_recommendations+1]
        
        recommendations = []
        for i in similar_indices:
            recommendations.append({
                'place_id': self.place_ids[i],
                'similarity_score': float(sim_scores[i])
            })
        
        return recommendations
    
    def recommend_for_city(self, city: str, db: Session, n: int = 10):
        """Recommend top places in a city"""
        places = db.query(Place).filter(Place.city.ilike(f"%{city}%")).all()
        
        if not places:
            return []
        
        # Sort by rating and popularity
        sorted_places = sorted(places, key=lambda x: x.avg_rating, reverse=True)
        return sorted_places[:n]
