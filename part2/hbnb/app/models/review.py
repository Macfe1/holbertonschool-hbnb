from app.models.basemodel import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        #text validation
        if not text or not isinstance(text, str):
            raise ValueError("Invalid data: review text must be a non-empty string")
        #rating validation
        if not rating or not isinstance(rating, int):
            raise ValueError("Invalid data: rating must be a non-empty integer")
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")

        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id,
        }

    def update(self, data):
        validate_attributes = {
            'text': str,
            'rating': int,
            'place_id': str,
            'user_id': str
        }
        for key, value in data.items():
            expected_value = validate_attributes[key]
            if not key in validate_attributes:
                raise ValueError(f"'{key}' is not a valid attribute")
            
            if not isinstance(value, expected_value):
                raise ValueError(f"'{key}' is not the right type")
            
            setattr(self, key, value)

        self.save()
""" 
    def create_review(text, rating, user, place):
        return cls(text, rating, user, place)

    def updateReview(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save

    def deleteReview(self, place, user):
        if place_id =
"""
