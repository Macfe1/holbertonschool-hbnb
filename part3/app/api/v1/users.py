import json
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(description='Whether the user is an admin'),
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        try:
            new_user = facade.create_user(user_data)
            return {
                "id": new_user.id,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 400

    def get(self):
        """Get Users"""
        users = facade.get_users()
        return json.dumps([user.to_dict() for user in users])

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.response(403, 'Forbidden access')
    @jwt_required()
    def put(self, user_id):
        """Update user information"""
        data = request.get_json()

        existing_user = facade.get_user(user_id)
        if not existing_user:
            return {'error': 'User not found'}, 404

        #To get the token id and is_admin
        current_user = get_jwt_identity()

        if current_user['id'] != user_id:
            return {'error': 'Unauthorized action.'}, 403

        if data.get('email') or data.get('password'):
            return {'error': 'You cannot modify email or password.'}, 400

        # Validate attributes and set attributes
        try:
            update_user = facade.update_user(user_id, data)
            if update_user:
                return {'message': 'User updated successfully'}, 200
            return {'error': 'Failed to update user'}, 400
        except Exception as e:
            return {'error': str(e)}, 400
