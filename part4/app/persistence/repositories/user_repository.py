from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    """A specialized repository for handling user-specific queries."""
    
    def __init__(self):
        """Initialize the repository with the User model."""
        super().__init__(User)

    def get_user_by_email(self, email):
        """Retrieve a user by email."""
        return self.model.query.filter_by(email=email).first()

    def add(self, obj):
        """Lazy import `db` to avoid circular imports"""
        from app import db  # ✅ Import inside method
        db.session.add(obj)
        db.session.commit()