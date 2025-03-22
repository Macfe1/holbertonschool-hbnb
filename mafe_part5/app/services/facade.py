from app.persistence.repositories.user_repository import UserRepository
from app.persistence.repositories.place_repository import PlaceRepository
from app.persistence.repositories.review_repository import ReviewRepository
from app.persistence.repositories.amenity_repository import AmenityRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    
    # USER METHODS
    def create_user(self, user_data):
        """Creates a new user and hashes the password before storing"""
        from app import db  # ✅ Import db inside the method to avoid circular imports
        
        # Ensure is_admin defaults to False if not provided (matches API logic)
        if 'is_admin' not in user_data:
            user_data['is_admin'] = False

        user = User(**user_data)
        user.hash_password(user_data['password'])  # ✅ Hash the password before storing
        db.session.add(user)
        db.session.commit()
        return user

    def get_user(self, user_id):
        """"Retrieves a user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)
        
    def update_user(self, user_id, user_data):
        """Update a user's details, ensuring email and password are not modified"""
        user = self.get_user(user_id)

        if not user:
            return None  # User not found

        # Ensure only admins can update the email
        if "email" in user_data:
            existing_user = self.get_user_by_email(user_data["email"])
            if existing_user and existing_user.id != user_id:
                return None  # Email already in use

        self.user_repo.update(user_id, user_data)  # Update the user
        return self.get_user(user_id)  # Return updated user

    # AMENITY METHODS
    def create_amenity(self, amenity_data):
        """Creates a new amenity and adds it to the repository."""
        # Validate required fields
        if 'name' not in amenity_data or not amenity_data['name'].strip():
            raise ValueError("Amenity name is required.")

        # Check if amenity already exists (by name)
        existing_amenity = self.amenity_repo.get_by_attribute("name", amenity_data["name"])
        if existing_amenity:
            raise ValueError("Amenity with this name already exists.")

        amenity = Amenity(amenity_data['name'])
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieves an amenity by its ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieves all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Updates an existing amenity."""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found.")
        if 'name' in amenity_data:
            if not amenity_data['name'].strip():
                raise ValueError("Amenity name cannot be empty.")
            # Check if a different amenity already has this name
            existing_amenity = self.amenity_repo.get_by_attribute("name", amenity_data["name"])
            if existing_amenity and existing_amenity.id != amenity_id:
                raise ValueError("An amenity with this name already exists.")

        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity

    # PLACE METHODS
    def create_place(self, place_data):
        """Creates a new place with validation for price, latitude, and longitude."""
        required_fields = ["title", "price", "latitude", "longitude", "owner_id"]
        for field in required_fields:
            if field not in place_data:
                raise ValueError(f"{field} is required.")

        # Validate price (must be a non-negative float)
        if not isinstance(place_data["price"], (int, float)) or place_data["price"] < 0:
            raise ValueError("Price must be a non-negative number.")

        # Validate latitude (-90 to 90)
        if not (-90 <= place_data["latitude"] <= 90):
            raise ValueError("Latitude must be between -90 and 90.")

        # Validate longitude (-180 to 180)
        if not (-180 <= place_data["longitude"] <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        # Validate owner exists
        owner = self.user_repo.get(place_data["owner_id"])
        if not owner:
            raise ValueError("Owner not found.")

        # Create and store place
        place = Place(
            title=place_data["title"],
            owner_id=owner.id,
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            description=place_data.get("description", ""),
        )

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieves a place by ID, including associated owner and amenities."""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return place

    def get_all_places(self):
        """Retrieves all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Updates an existing place."""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found.")

        # Validate and update price
        if "price" in place_data:
            if not isinstance(place_data["price"], (int, float)) or place_data["price"] < 0:
                raise ValueError("Price must be a non-negative number.")

        # Validate and update latitude
        if "latitude" in place_data:
            if not (-90 <= place_data["latitude"] <= 90):
                raise ValueError("Latitude must be between -90 and 90.")

        # Validate and update longitude
        if "longitude" in place_data:
            if not (-180 <= place_data["longitude"] <= 180):
                raise ValueError("Longitude must be between -180 and 180.")

        self.place_repo.update(place_id, place_data)
        return place
    
    # REVIEW METHODS
    def create_review(self, review_data):
        """Creates a new review with validation for user_id, place_id, and rating."""
        required_fields = ["text", "rating", "user_id", "place_id"]
        for field in required_fields:
            if field not in review_data or not review_data[field]:
                raise ValueError(f"{field} is required.")

        # Validate rating (must be between 1 and 5)
        if not isinstance(review_data["rating"], int) or not (1 <= review_data["rating"] <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")

        # Validate user exists
        user = self.user_repo.get(review_data["user_id"])
        if not user:
            raise ValueError("User not found.")

        # Validate place exists
        place = self.place_repo.get(review_data["place_id"])
        if not place:
            raise ValueError("Place not found.")

        # Create and store review (without ORM relationships)
        review = Review(
            text=review_data["text"],
            rating=review_data["rating"],
            user_id=review_data["user_id"],  # ✅ Store only the user_id
            place_id=review_data["place_id"]  # ✅ Store only the place_id
        )

        self.review_repo.add(review)  # ✅ Save review in the repository
        return review

    def get_review(self, review_id):
        """Retrieves a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieves all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieves all reviews for a specific place."""
        return self.review_repo.get_reviews_by_attribute('place_id', place_id)
    
    def get_reviews_by_place_and_user(self, place_id, user_id):
        """Retrieve a review left by a specific user for a specific place"""
        reviews = self.review_repo.get_all()  # Get all reviews
        for review in reviews:
            if review.place_id == place_id and review.user_id == user_id:
                return review  # Return the existing review if found
        return None  # No review found

    def update_review(self, review_id, review_data):
        """Updates an existing review."""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found.")

        if "rating" in review_data:
            if not isinstance(review_data["rating"], int) or not (1 <= review_data["rating"] <= 5):
                raise ValueError("Rating must be an integer between 1 and 5.")

        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
        """Deletes a review."""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found.")

        # Remove the review from the associated place
        if review in review.place.reviews:
            review.place.reviews.remove(review)  # ✅ Ensure it is removed from the Place

        self.review_repo.delete(review_id)  # ✅ Remove it from the repository
        return True