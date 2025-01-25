import unittest
from app import create_app

class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Create a sample user and place to associate with the review
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice.smith@example.com"
        })
        self.user_id = user_response.json['id']

        place_response = self.client.post('/api/v1/places/', json={
            "title": "Beautiful Beach House",
            "description": "A relaxing retreat by the sea",
            "price": 300.0,
            "latitude": 34.0,
            "longitude": -118.0,
            "owner_id": self.user_id
        })
        self.place_id = place_response.json['id']

    def test_create_review(self):
        """Test creating a review with valid data"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Amazing stay, would visit again!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)
        self.assertEqual(response.json["text"], "Amazing stay, would visit again!")
        self.assertEqual(response.json["rating"], 5)

    def test_get_review(self):
        """Test retrieving a review by ID"""
        # Create a review
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Lovely experience!",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = create_response.json['id']

        # Retrieve the review
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], review_id)
        self.assertEqual(response.json['text'], "Lovely experience!")

    def test_create_review_invalid_data(self):
        """Test creating a review with invalid data"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 6,  # Invalid rating (should be between 1 and 5)
            "user_id": "invalid-user-id",
            "place_id": "invalid-place-id"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

if __name__ == "__main__":
    unittest.main()
