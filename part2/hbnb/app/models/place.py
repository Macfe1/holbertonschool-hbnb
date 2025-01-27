from app.models.basemodel import BaseModel
from app.models.review import Review

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        # title validation
        if not title or not isinstance(title, str):
            raise ValueError("Invalid data: title must be a non-empty string")
        # price validation
        if not price or price is None:
            return ValueError("Price cannot be empty")
        if not isinstance(price, float):
            raise ValueError("Price must be a float")
        if price < 0.0:
            raise ValueError("Price must be a positive number")
        #latitude validation
        if not latitude or not isinstance(latitude, float):
            raise ValueError("Invalid data: latitude must be a non-empty float")
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        #longitude validation
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
            'reviews': [review.to_dict() for review in self.reviews],
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
            'reviews': list,
            'amenities': str,
        }
        for key, value in data.items():
                expected_value = validate_attributes[key]
                if not key in validate_attributes:
                    raise ValueError(f"'{key}' is not a valid attribute")
                #Verify that review is a list of dictionaries
                if key == 'reviews':
                    if not isinstance(value, list):
                        raise ValueError(f"'reviews' should be a list")
                    self.reviews = []
                    for review in value:
                        if isinstance(review, Review): #Case that review is a list of objects
                            self.reviews.append(review)
                        elif isinstance(review, dict): #Case that review is a list of dictionaries
                            self.reviews.append(Review(**review))
                        else:
                            raise ValueError(f"Each review must be a Review object or a dictionary")
                    continue

                if not isinstance(value, expected_value):
                    raise ValueError(f"'{key}' is not the right type")
                setattr(self, key, value)
        self.save()

        """ 
        def listed_reviews(self):
        return self.reviews
        """

