from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from app.api.v1.auth_helpers import is_admin_user

api = Namespace('places', description='Place operations')

# Define the place model for input validation and documentation
place_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place (Only authenticated users)"""
        current_user_id = get_jwt_identity()  # Get the logged-in user's ID
        place_data = api.payload

        # Ensure the owner_id matches the authenticated user
        place_data['owner_id'] = current_user_id

        try:
            new_place = facade.create_place(place_data)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id  # ✅ Keep only this, no nested owner object
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [{
            'id': place.id, 
            'title': place.title, 
            'latitude': place.latitude, 
            'longitude': place.longitude
        } for place in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner_id  # ✅ Keep only this, no nested owner object
        }, 200

    @jwt_required()
    @api.expect(place_model, validate=False)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Admins or owners can modify places"""
        current_user_id = get_jwt_identity()

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # ✅ Admins can update any place
        if not is_admin_user() and place.owner.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        data = api.payload

        try:
            updated_place = facade.update_place(place_id, data)
            return {
                'id': updated_place.id,
                'title': updated_place.title,
                'description': updated_place.description,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'owner_id': updated_place.owner_id  # ✅ Keep only this, no nested owner object
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        
@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)

        if reviews is None:  # If no reviews exist for the place, return 404
            return {'error': 'Place not found'}, 404

        # ✅ Ensure reviews is a list before iterating
        if not isinstance(reviews, list):
            reviews = [reviews]  # Convert single object to list to avoid TypeError

        return [{'id': review.id, 'text': review.text, 'rating': review.rating} for review in reviews], 200