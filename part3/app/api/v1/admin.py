from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
import facade

api = Namespace('admin', description='Administrator operations')

def is_admin():
    current_user = get_jwt_identity()
    return current_user.get('is_admin', False)



@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {'message': 'User created successfully', 'user': new_user}, 201




@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    def put(self, user_id):
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        updated_user = facade.update_user(user_id, data)
        return {'message': 'User updated successfully', 'user': updated_user}, 200



@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    def post(self):
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        amenity_data = request.json
        new_amenity = facade.create_amenity(amenity_data)
        return {'message': 'Amenity created successfully', 'amenity': new_amenity}, 201



@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    def put(self, amenity_id):
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        updated_amenity = facade.update_amenity(amenity_id, data)
        return {'message': 'Amenity updated successfully', 'amenity': updated_amenity}, 200



@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    def put(self, place_id):
        current_user = get_jwt_identity()
        is_admin_user = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not is_admin_user and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        data = request.json
        updated_place = facade.update_place(place_id, data)
        return {'message': 'Place updated successfully', 'place': updated_place}, 200

