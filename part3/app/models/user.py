from flask_bcrypt import Bcrypt
from app import db
from app.models.basemodel import BaseModel
from app.models.place import Place
import re

bcrypt = Bcrypt()

class User(BaseModel):

    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        # first_name validation
        if not first_name or not isinstance(first_name, str):
            raise ValueError("Invalid data: first_name must be a non-empty string")
        # last_name validation
        if not last_name or not isinstance(last_name, str):
            raise ValueError("Invalid data: last_name must be a non-empty string")
        # email validation
        if not email or not isinstance(email, str):
            raise ValueError("Invalid data: email must be a non-empty string")
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid data: email is not in a valid format")
        # password validation
        if not password or not isinstance(password, str):
            raise ValueError("Invalid data: password must be a non-empty string")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.password = self.hash_password(password)
        self.places = []

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
        }

    def add_place(self, place):
        if isinstance(place, Place):
            self.places.append(place)
    
    def list_places(self):
        return self.places

    def update(self, data):
        """Update user attributes from the data passed"""
        valid_attributes = {
            'first_name': str,
            'last_name': str,
            'is_admin': bool,
        }
        for key, value in data.items():
            expected_value = valid_attributes[key]
            if key not in valid_attributes:
                raise ValueError(f"'{key}' is not a valid attribute")

            if not isinstance(value, expected_value):
                raise ValueError(f"'{key}' is not the right type")

            if key == "password":
                value = self.hash_password(value)

            setattr(self, key, value)

        self.save()

    def hash_password(self, password):
        """Hashes the password before storing it."""
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
