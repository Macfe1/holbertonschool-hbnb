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

    def add_place(self, place):
        if isinstance(place, Place):
            self.places.append(place)
    
    def list_places(self):
        return self.places

"""    
    def updateProfile(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save

    def deleteUser(self, user_id):
        return self.id == user_id
"""