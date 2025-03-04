from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('protected', description='Protected operations')

@api.route('/')
class ProtectedResource(Resource):
    @jwt_required()
    @api.response(200, 'Access granted')
    @api.response(401, 'Missing or invalid token')
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user_id = get_jwt_identity()  # Extract user ID from JWT
        claims = get_jwt()  # Extract additional claims (like is_admin)
        is_admin = claims.get("is_admin", False)  # Default to False if missing

        return {
            'message': f'Hello, user {current_user_id}',
            'is_admin': is_admin
        }, 200