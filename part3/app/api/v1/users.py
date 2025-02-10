from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1.auth_helpers import is_admin_user
from app.services import facade

# Define the users namespace
api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password for the user'),
    'is_admin': fields.Boolean(required=False, description='Specifies if the user has admin privileges (default: False)')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user (Admin-only, except for the first user)"""
        user_data = api.payload

        # Check if there are any existing users
        existing_users = facade.user_repo.get_all()

        # If no users exist, make the first user an admin
        if not existing_users:
            user_data['is_admin'] = True
        elif not is_admin_user():
            return {'error': 'Admin access required'}, 403  # Reject non-admins

        # Ensure email is unique
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Create the user
        new_user = facade.create_user(user_data)

        # ✅ Return a dictionary instead of a User object
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'is_admin': new_user.is_admin
        }, 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve all users"""
        users = facade.user_repo.get_all()
        return [{
            'id': user.id, 
            'first_name': user.first_name, 
            'last_name': user.last_name, 
            'email': user.email, 
            'is_admin': user.is_admin
        } for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }, 200
    
    @jwt_required()
    @api.expect(user_model, validate=False)
    @api.response(200, 'User successfully updated')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'You cannot modify email or password')
    def put(self, user_id):
        """Modify any user's details (Admins-only)"""
        if not is_admin_user():
            return {'error': 'Admin access required'}, 403  # Reject non-admins

        user_data = api.payload

        # Ensure email is unique (if changing it)
        if "email" in user_data:
            existing_user = facade.get_user_by_email(user_data["email"])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        updated_user = facade.update_user(user_id, user_data)

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email,
            'is_admin': updated_user.is_admin
        }, 200

