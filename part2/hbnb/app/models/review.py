from app.models.basemodel import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        if not self.text or not isinstance(self.text, str):
            raise ValueError("Invalid data: review text must be a non-empty string")

        if not self.rating or not isinstance(self.rating, int):
            raise ValueError("Invalid data: rating must be a non-empty integer")
        if not 1 <= self.rating <= 5:
            raise ValueError("Rating must be between 1 and 5")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
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
