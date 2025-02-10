import re
import uuid
from datetime import datetime
from app import db, bcrypt
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Boolean, ForeignKey

class User(db.Model):
    """SQLAlchemy User Model"""
    __tablename__ = "users"

    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))  # ✅ Auto-generate UUID
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)  # ✅ Renamed from "password" to "password_hash"
    is_admin = Column(Boolean, default=False, nullable=False)

    created_at = Column(db.DateTime, default=datetime.utcnow)
    updated_at = Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # One-to-Many: User → Places
    places = relationship("Place", back_populates="owner", cascade="all, delete-orphan")

    # One-to-Many: User → Reviews
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, first_name: str, last_name: str, email: str, password: str, is_admin: bool = False):
        """Initialize User with hashed password"""
        self.id = str(uuid.uuid4())  # ✅ Ensure UUID is assigned in __init__

        # Validate first_name
        if not isinstance(first_name, str) or not first_name.strip():
            raise ValueError("First name is required and must be a non-empty string.")
        if len(first_name) > 50:
            raise ValueError("First name cannot exceed 50 characters.")
        self.first_name = first_name.strip()

        # Validate last_name
        if not isinstance(last_name, str) or not last_name.strip():
            raise ValueError("Last name is required and must be a non-empty string.")
        if len(last_name) > 50:
            raise ValueError("Last name cannot exceed 50 characters.")
        self.last_name = last_name.strip()

        # Validate email
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not isinstance(email, str) or not re.match(email_regex, email):
            raise ValueError("Invalid email format.")
        self.email = email.strip()

        # Hash and store password
        self.password_hash = self.hash_password(password)

        # Assign is_admin flag
        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean value.")
        self.is_admin = is_admin

    def hash_password(self, password):
        """Hashes the password before storing it."""
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password_hash, password)