from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    def get_reviews_by_attribute(self, attr_name, attr_value):
        """Retrieves all reviews for a specific place or user."""
        return self.model.query.filter_by(**{attr_name: attr_value}).all()