from app import db
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

class Review(db.Model):
    """SQLAlchemy Review Model"""
    __tablename__ = 'reviews'

    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))  # ✅ Auto-generate UUID
    text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)

    # ✅ One-to-Many: Review → User
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="reviews")  # ✅ Define relationship with User

    # ✅ One-to-Many: Review → Place
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    place = relationship("Place", back_populates="reviews")  # ✅ Define relationship with Place

    created_at = Column(db.DateTime, default=datetime.utcnow)
    updated_at = Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, text: str, rating: int, user_id: str, place_id: str):
        """Initialize Review with Validations"""
        self.id = str(uuid.uuid4())  # ✅ Ensure UUID is assigned in __init__

        # ✅ Validate text
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Review text is required and must be a non-empty string.")
        self.text = text.strip()

        # ✅ Validate rating
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")
        self.rating = rating

        # ✅ Validate user_id
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("User ID is required.")
        self.user_id = user_id.strip()

        # ✅ Validate place_id
        if not isinstance(place_id, str) or not place_id.strip():
            raise ValueError("Place ID is required.")
        self.place_id = place_id.strip()