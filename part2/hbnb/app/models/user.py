from app.models.basemodel import BaseModel
from app.models.place import Place
import re

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        # first_name validation
        if not first_name or not isinstance(first_name, str):
            raise ValueError("Invalid data: first_name must be a non-empty string")
        self.first_name = first_name
        # last_name validation
        if not last_name or not isinstance(last_name, str):
            raise ValueError("Invalid data: last_name must be a non-empty string")
        self.last_name = last_name
        # email validation
        if not email or not isinstance(email, str):
            raise ValueError("Invalid data: email must be a non-empty string")
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid data: email is not in a valid format")
        self.email = email
        self.is_admin = is_admin
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
            'email': str,
            'is_admin': bool,
        }
        for key, value in data.items():
            expected_value = valid_attributes[key]
            if key not in valid_attributes:
                raise ValueError(f"'{key}' is not a valid attribute")

            if not isinstance(value, expected_value):
                raise ValueError(f"'{key}' is not the right type")

            setattr(self, key, value)

        self.save()
"""
    def deleteUser(self, user_id):
        return self.id == user_id
"""