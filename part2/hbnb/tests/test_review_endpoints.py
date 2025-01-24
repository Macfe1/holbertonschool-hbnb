import unittest
from app import create_app

class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        """Set up the test client."""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_review(self):
        """Test creating a new review."""
        response = self.client.post('/api/v1/reviews/', json={
            'text': 'Great place!',
            'rating': 5,
            'user_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            'place_id': '1fa85f64-5717-4562-b3fc-2c963f66afa6'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
        self.assertEqual(response.json['text'], 'Great place!')

    def test_create_review_invalid_data(self):
        """Test creating a review with invalid data."""
        response = self.client.post('/api/v1/reviews/', json={
            'text': '',
            'rating': 6,  # Invalid rating (should be between 1 and 5)
            'user_id': '',
            'place_id': ''
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_reviews(self):
        """Test retrieving all reviews."""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))

    def test_get_review_by_id(self):
        """Test retrieving a review by ID."""
        # Create a review first
        create_response = self.client.post('/api/v1/reviews/', json={
            'text': 'Nice place!',
            'rating': 4,
            'user_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            'place_id': '1fa85f64-5717-4562-b3fc-2c963f66afa6'
        })
        review_id = create_response.json['id']

        # Retrieve the review by ID
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['text'], 'Nice place!')

    def test_update_review(self):
        """Test updating a review."""
        # Create a review first
        create_response = self.client.post('/api/v1/reviews/', json={
            'text': 'Decent stay',
            'rating': 3,
            'user_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            'place_id': '1fa85f64-5717-4562-b3fc-2c963f66afa6'
        })
        review_id = create_response.json['id']

        # Update the review
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            'text': 'Amazing stay',
            'rating': 5
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['text'], 'Amazing stay')

    def test_delete_review(self):
        """Test deleting a review."""
        # Create a review first
        create_response = self.client.post('/api/v1/reviews/', json={
            'text': 'Not great',
            'rating': 2,
            'user_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            'place_id': '1fa85f64-5717-4562-b3fc-2c963f66afa6'
        })
        review_id = create_response.json['id']

        # Delete the review
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], 'Review deleted successfully')

    def test_get_reviews_by_place(self):
        """Test retrieving all reviews for a specific place."""
        # Create a review for a place
        self.client.post('/api/v1/reviews/', json={
            'text': 'Fantastic!',
            'rating': 5,
            'user_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            'place_id': '1fa85f64-5717-4562-b3fc-2c963f66afa6'
        })

        # Get reviews for the place
        response = self.client.get('/api/v1/reviews/places/1fa85f64-5717-4562-b3fc-2c963f66afa6/reviews')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))
        self.assertGreater(len(response.json), 0)

if __name__ == '__main__':
    unittest.main()

