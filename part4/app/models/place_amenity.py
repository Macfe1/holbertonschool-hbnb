from app import db

# ✅ Association Table for Many-to-Many (Place ↔ Amenity)
place_amenity = db.Table(
    'place_amenity',
    db.metadata,  # ✅ Prevent multiple declarations
    db.Column('place_id', db.String(60), db.ForeignKey('places.id', ondelete="CASCADE"), primary_key=True),
    db.Column('amenity_id', db.String(60), db.ForeignKey('amenities.id', ondelete="CASCADE"), primary_key=True)
)