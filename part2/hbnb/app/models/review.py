from app.models.basemodel import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        if not text or not isinstance(text, str):
            raise ValueError("Invalid data: review text must be a non-empty string")
        # Validate rating
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place': self.place.id if self.place else None,
            'user': self.user.id if self.user else None,
        }
        

    def update(self, data):
        validate_attributes = {
            'text': str,
            'rating': int,
            'place': str,
            'user': str,
        }
        for key, value in data.items():
                expected_value = validate_attributes[key]
                if key in validate_attributes:
                    if isinstance(value, expected_value):
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
