import unittest
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Create a sample user to associate with the place
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.user_id = response.json['id']

    def test_create_place(self):
        """Test creating a place with valid data"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Cabin",
            "description": "A beautiful cabin in the woods",
            "price": 150.0,
            "latitude": 45.0,
            "longitude": -120.0,
            "owner_id": self.user_id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)
        self.assertEqual(response.json["title"], "Cozy Cabin")

    def test_get_place(self):
        """Test retrieving a place by ID"""
        # Create a place
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Cabin",
            "description": "A beautiful cabin in the woods",
            "price": 150.0,
            "latitude": 45.0,
            "longitude": -120.0,
            "owner_id": self.user_id
        })
        place_id = create_response.json['id']

        # Retrieve the place
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], place_id)

    def test_create_place_invalid_data(self):
        """Test creating a place with invalid data"""
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "price": -50.0,
            "latitude": 95.0,  # Invalid latitude
            "longitude": 190.0,  # Invalid longitude
            "owner_id": "invalid-user-id"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

if __name__ == "__main__":
    unittest.main()
