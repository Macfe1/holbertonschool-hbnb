from app import db
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from app.models.place_amenity import place_amenity

class Amenity(db.Model):
    """SQLAlchemy Amenity Model"""
    __tablename__ = 'amenities'

    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))  # Auto-generate UUID
    name = Column(String(255), nullable=False, unique=True)

    # Many-to-Many Relationship with Place
    places = relationship("Place", secondary=place_amenity, back_populates="amenities")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name: str):
        """Initialize Amenity with Validation"""
        self.id = str(uuid.uuid4())  # Ensure UUID is assigned in __init__

        # Validate name (required, max 50 characters)
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Amenity name is required and must be a non-empty string.")
        if len(name) > 50:
            raise ValueError("Amenity name cannot exceed 50 characters.")
        self.name = name.strip()
