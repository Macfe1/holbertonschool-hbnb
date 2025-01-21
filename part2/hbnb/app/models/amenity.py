from app.models.basemodel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name
    
    def to_dict(self):
        return{
            'id': self.name
        }
