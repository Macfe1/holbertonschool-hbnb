import unittest
from app import create_app

class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity(self):
        """Test creating an amenity with valid data"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)
        self.assertEqual(response.json["name"], "Wi-Fi")

    def test_get_amenity(self):
        """Test retrieving an amenity by ID"""
        # Create an amenity
        create_response = self.client.post('/api/v1/amenities/', json={
            "name": "Swimming Pool"
        })
        amenity_id = create_response.json['id']

        # Retrieve the amenity
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], amenity_id)
        self.assertEqual(response.json['name'], "Swimming Pool")

    def test_create_amenity_invalid_data(self):
        """Test creating an amenity with invalid data"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""  # Invalid: Empty name
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

if __name__ == "__main__":
    unittest.main()
