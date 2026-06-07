from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    itineraries = relationship("Itinerary", back_populates="user")
    votes = relationship("Vote", back_populates="user")

class Place(Base):
    __tablename__ = "places"
    
    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    city = Column(String, index=True)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    avg_rating = Column(Float, default=0)
    price_level = Column(Integer)  # 0-4
    typical_duration = Column(Integer)  # in minutes
    tags = Column(JSON)  # ['historical', 'nature', 'food']
    image_url = Column(String)
    
    votes = relationship("Vote", back_populates="place")
    itinerary_items = relationship("ItineraryItem", back_populates="place")

class Itinerary(Base):
    __tablename__ = "itineraries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    destination_city = Column(String)
    destination_country = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    total_budget = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="itineraries")
    days = relationship("ItineraryDay", back_populates="itinerary", cascade="all, delete-orphan")

class ItineraryDay(Base):
    __tablename__ = "itinerary_days"
    
    id = Column(Integer, primary_key=True, index=True)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"))
    day_number = Column(Integer)
    date = Column(DateTime)
    
    itinerary = relationship("Itinerary", back_populates="days")
    items = relationship("ItineraryItem", back_populates="day", cascade="all, delete-orphan")

class ItineraryItem(Base):
    __tablename__ = "itinerary_items"
    
    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("itinerary_days.id"))
    place_id = Column(Integer, ForeignKey("places.id"))
    order_index = Column(Integer)
    start_time = Column(String)  # "09:00"
    estimated_cost = Column(Float)
    
    day = relationship("ItineraryDay", back_populates="items")
    place = relationship("Place", back_populates="itinerary_items")

class Vote(Base):
    __tablename__ = "votes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    place_id = Column(Integer, ForeignKey("places.id"))
    rating = Column(Integer)  # 1-5
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="votes")
    place = relationship("Place", back_populates="votes")
