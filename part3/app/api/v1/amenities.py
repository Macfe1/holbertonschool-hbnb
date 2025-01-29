from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
import json

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource): 
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload

        try:
            # Check for existing amenity
            existing_amenity = facade.get_amenity_by_name(amenity_data['name'])
            if existing_amenity:
                return {'error': 'The amenity already exists'}, 400

            # Create a new amenity
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return json.dumps([amenity.to_dict() for amenity in amenities])

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity_by_id = facade.get_amenity(amenity_id)
        if not amenity_by_id:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity_by_id.id,'name': amenity_by_id.name}

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""

        data = request.get_json()

        existing_amenity = facade.get_amenity(amenity_id)
        if not existing_amenity:
            return {'error': 'Amenity not found'}, 404
        
        update_amenity = facade.update_amenity(amenity_id, data)
        if not update_amenity:
            return {'error': 'Invalid request'}, 400
        return {'Sucess': 'Amenity updated', 'id': existing_amenity.id, 'name': existing_amenity.name}, 200
