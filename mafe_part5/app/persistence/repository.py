from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class SQLAlchemyRepository:
    def __init__(self, model):
        """Initialize with a SQLAlchemy model."""
        self.model = model

    def add(self, obj):
        """Adds an object to the database."""
        from app import db  # ✅ Lazy import `db` to avoid circular import
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """Retrieves an object by its ID."""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Retrieves all objects of this type."""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Updates an existing object with new data."""
        from app import db  # ✅ Lazy import `db`
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
            return obj

    def delete(self, obj_id):
        """Deletes an object from the database."""
        from app import db  # ✅ Lazy import `db`
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """Retrieves an object based on a specific attribute."""
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
