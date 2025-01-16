from app.models.basemodel import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
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
