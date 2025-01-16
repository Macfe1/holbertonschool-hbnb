from app.models.basemodel import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)
    
    def listed_reviews(self):
        return self.review

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
    
    def listed_amenities(self):
        return self.amenities
"""
    def create_place(self, owner, title, description, price, latitude, longitude):
        return Place(title, description, price, latitude, longitude, owner)

    def deletePlace(self, place_id):
        return self.id == place_id

    def updatePlace(self, place_id, **kwargs):
        if self.id == place_id:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            self.save()
"""