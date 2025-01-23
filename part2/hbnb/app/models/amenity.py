from app.models.basemodel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
    def update(self, data):
        validate_attributes = {
            'name': str
        }

        for key, value in data.items():
            if not key in validate_attributes:
                raise ValueError(f"'{key}' is not a valid attribute")
            if not isinstance(value, validate_attributes[key]):
                raise TypeError(f"'{value}' is not a valid type")
            setattr(self, key, value)
        self.save
