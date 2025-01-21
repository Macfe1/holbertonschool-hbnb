from app.models.basemodel import BaseModel
from app.models.place import Place

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
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
        return True
"""
    def deleteUser(self, user_id):
        return self.id == user_id
"""