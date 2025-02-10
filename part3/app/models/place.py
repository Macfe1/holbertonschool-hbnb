from app import db
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.place_amenity import place_amenity

class Place(db.Model):
    """SQLAlchemy Place Model"""
    __tablename__ = 'places'

    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))  # Auto-generate UUID
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # One-to-Many: Place → User (owner)
    owner_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    owner = relationship("User", back_populates="places")

    # One-to-Many: Place → Reviews
    reviews = relationship("Review", back_populates="place", cascade="all, delete-orphan")

    # Many-to-Many: Place ↔ Amenity
    amenities = relationship("Amenity", secondary=place_amenity, back_populates="places")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, title: str, price: float, latitude: float, longitude: float, owner_id: str, description: str = ""):
        """Initialize Place with Validations"""
        self.id = str(uuid.uuid4())  # Ensure UUID is assigned in __init__

        # Validate title
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title is required and must be a non-empty string.")
        if len(title) > 255:
            raise ValueError("Title cannot exceed 255 characters.")
        self.title = title.strip()

        # Validate price
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number.")
        self.price = float(price)

        # Validate latitude
        if not isinstance(latitude, (int, float)) or not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be a float between -90.0 and 90.0.")
        self.latitude = float(latitude)

        # Validate longitude
        if not isinstance(longitude, (int, float)) or not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be a float between -180.0 and 180.0.")
        self.longitude = float(longitude)

        # Validate description (optional)
        if not isinstance(description, str):
            raise ValueError("Description must be a string.")
        self.description = description.strip() if description else ""

        self.owner_id = owner_id  # Ensure owner_id is stored