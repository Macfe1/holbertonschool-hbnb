from app.models.basemodel import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        #text validation
        if not text or not isinstance(text, str):
            raise ValueError("Invalid data: review text must be a non-empty string")

        # Validate rating
        if rating is None:
            raise ValueError("Rating must be an integer between 1 and 5")
        
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer between 1 and 5")

        if not 1 <= rating <= 5:
            raise ValueError("Rating must be an integer between 1 and 5")

        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id if self.place_id else None,
            'user_id': self.user_id if self.user_id else None,
        }

    def update(self, data):
        validate_attributes = {
            'text': str,
            'rating': int,
            'place_id': str,
            'user_id': str,
        }
        for key, value in data.items():
            expected_value = validate_attributes[key]
            if not key in validate_attributes:
                raise ValueError(f"'{key}' is not a valid attribute")
            
            if not isinstance(value, expected_value):
                raise ValueError(f"'{key}' is not the right type")
            
            setattr(self, key, value)
        self.save()
