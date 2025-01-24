from app.models.basemodel import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        if not self.text:
            raise ValueError("Missing review text")
        if not isinstance(self.text, str):
            raise ValueError("Review text must be a string")

        if not self.rating:
            raise ValueError("Missing rating")
        if not isinstance(self.rating, int):
            raise ValueError("Rating must be an integer")
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
