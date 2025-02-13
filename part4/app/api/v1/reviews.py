from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from app.api.v1.auth_helpers import is_admin_user

# API Namespace for Reviews
api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'You cannot review your own place')
    @api.response(400, 'You have already reviewed this place')
    def post(self):
        """Create a new review (Users cannot review their own places or review the same place twice)"""
        current_user_id = get_jwt_identity()
        review_data = api.payload.copy()  # Copy payload to avoid modifying the original request
        review_data['user_id'] = current_user_id  # Inject user_id from JWT

        # Fetch the place
        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404

        # ✅ Use owner_id instead of place.owner.id
        if place.owner_id == current_user_id:
            return {'error': 'You cannot review your own place'}, 400

        # Check if user already reviewed this place
        existing_review = facade.get_reviews_by_place_and_user(review_data['place_id'], current_user_id)
        if existing_review:
            return {'error': 'You have already reviewed this place'}, 400

        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'place_id': new_review.place_id,
                'user_id': new_review.user_id
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [{'id': review.id, 'text': review.text, 'rating': review.rating} for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'place_id': review.place_id,  # 🔧 Changed from `review.place.id`
            'user_id': review.user_id  # 🔧 Changed from `review.user.id`
        }, 200

    @jwt_required()
    @api.expect(review_model, validate=False)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review (Only creator can modify)"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        # ✅ Use `user_id` instead of `user.id`
        if review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403  # Prevent non-owners from modifying

        data = api.payload
        try:
            updated_review = facade.update_review(review_id, data)
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'place_id': updated_review.place_id,
                'user_id': updated_review.user_id
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Admins or review owners can delete reviews"""
        current_user_id = get_jwt_identity()

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # ✅ Admins can delete any review
        if not is_admin_user() and review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 404
