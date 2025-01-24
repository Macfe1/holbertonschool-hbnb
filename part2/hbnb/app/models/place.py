from app.models.basemodel import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        if not title or not isinstance(title, str):
            raise ValueError("Invalid data: title must be a non-empty string")
        if not price or not isinstance(price, float):
            raise ValueError("Invalid data: price must be a non-empty integer")
        if price < 0.0:
            raise ValueError("Price must be a positive number")
        if price is None:
            raise ValueError("Price must be a positive number")

        if not latitude or not isinstance(latitude, float):
            raise ValueError("Invalid data: latitude must be a non-empty float")
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")

        if not longitude or not isinstance(longitude, float):
            raise ValueError("Invalid data: longitude must be a non-empty float")
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
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

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'reviews': self.reviews,
            'amenities': self.amenities,
        }

    def update(self, data):

        validate_attributes = {
            'title': str,
            'description': str,
            'price': float,
            'latitude': float,
            'longitude': float,
            'owner_id': str,
            'reviews': str,
            'amenities': str,
        }
        for key, value in data.items():
                expected_value = validate_attributes[key]
                if key in validate_attributes:
                    if isinstance(value, expected_value):
                        setattr(self, key, value)
        self.save()

"""
    def create_place(self, owner, title, description, price, latitude, longitude):
        return Place(title, description, price, latitude, longitude, owner)

    def deletePlace(self, place_id):
        return self.id == place_id
"""
