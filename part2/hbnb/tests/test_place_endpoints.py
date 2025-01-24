import unittest
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        """Set up the Flask test client and any necessary data."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.default_user_id = "123e4567-e89b-12d3-a456-426614174000"

        # Create a default user for testing
        self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "id": self.default_user_id
        })

    def test_create_place(self):
        """Test creating a new place."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.default_user_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
        self.assertEqual(response.json['title'], "Cozy Apartment")

    def test_create_place_invalid_data(self):
        """Test creating a place with invalid data."""
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "price": -100.0,
            "latitude": 200.0,
            "longitude": -400.0,
            "owner_id": self.default_user_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_places(self):
        """Test retrieving all places."""
        # Create a place first
        self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "description": "A house by the beach",
            "price": 150.0,
            "latitude": 34.0194,
            "longitude": -118.4912,
            "owner_id": self.default_user_id,
            "amenities": []
        })

        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))
        self.assertGreaterEqual(len(response.json), 1)

    def test_get_place_by_id(self):
        """Test retrieving a place by ID."""
        # Create a place first
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Luxury Villa",
            "description": "An upscale place to stay",
            "price": 200.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.default_user_id,
            "amenities": []
        })
        place_id = create_response.json['id']

        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['title'], "Luxury Villa")

    def test_update_place(self):
        """Test updating a place."""
        # Create a place first
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Small Cabin",
            "description": "A cozy cabin in the woods",
            "price": 80.0,
            "latitude": 60.0,
            "longitude": -150.0,
            "owner_id": self.default_user_id,
            "amenities": []
        })
        place_id = create_response.json['id']

        # Update the place
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "Updated Cabin",
            "price": 90.0
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['success'], "Place updated successfully")

    def test_update_nonexistent_place(self):
        """Test updating a place that does not exist."""
        response = self.client.put('/api/v1/places/nonexistent-id', json={
            "title": "Nonexistent Place"
        })
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()

