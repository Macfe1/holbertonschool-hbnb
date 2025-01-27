from flask_restx import Namespace, Resource, fields
from app.services import facade
import json
from flask import request

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Adding the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload

        existing_user = facade.get_user(place_data['owner_id'])
        if not existing_user:
            return {'error': 'User not found'}, 400

        if not isinstance(place_data['price'], float) or place_data['price'] <= 0.0:
            raise ValueError("Price have an invalid type or value")

        if not isinstance(place_data['latitude'], float) or not (-90 <= place_data['latitude'] <= 90):
            raise ValueError(f"Latitude have an invalid type or value")

        if not isinstance(place_data['longitude'], float) or not (-180 <= place_data['longitude'] <= 180):
            raise ValueError(f"Longitude have an inavlid type or value")

        else:
            place = facade.create_place(place_data)
            print("enterd here")
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner_id': place.owner_id,
                'amenities': place.amenities
            }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        list_of_places = facade.get_all_places()
        return json.dumps([place.to_dict() for place in list_of_places])

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place_by_id = facade.get_place(place_id)
        if not place_by_id:
            return {'error': 'Place not found'}, 404
        return {'id': place_by_id.id, 'title': place_by_id.title, 'description': place_by_id.description, 'price': place_by_id.price, 'latitude': place_by_id.latitude, 'longitude': place_by_id.longitude, 'owner_id': place_by_id.owner_id, 'amenities': place_by_id.amenities, 'reviews': [review.to_dict() for review in place_by_id.reviews]}

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        data = request.get_json()

        place_exist = facade.get_place(place_id)
        if not place_exist:
            return {'error': 'Place not found'}, 404

        update_place = facade.update_place(place_id, data)
        if not update_place:
            return {'error': 'Invalid input data to update palce'}, 400
        return {'success': 'Place updated successfully'}, 200
