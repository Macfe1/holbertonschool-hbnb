import unittest
from app import create_app

class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity(self):
        """Test creating a new amenity"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("Wi-Fi", response.json['name'])

    def test_create_amenity_duplicate(self):
        """Test creating a duplicate amenity"""
        self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })  # Create the initial amenity

        response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })  # Attempt to create a duplicate
        self.assertEqual(response.status_code, 400)
        self.assertIn("already exist", response.json['error'])

    def test_get_all_amenities(self):
        """Test retrieving a list of amenities"""
        self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })
        self.client.post('/api/v1/amenities/', json={
            "name": "Pool"
        })

        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Wi-Fi", response.json)
        self.assertIn("Pool", response.json)

    def test_get_amenity_by_id(self):
        """Test retrieving an amenity by ID"""
        create_response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })
        amenity_id = create_response.json['id']

        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Wi-Fi")

    def test_get_amenity_not_found(self):
        """Test retrieving a non-existent amenity"""
        response = self.client.get('/api/v1/amenities/invalid-id')
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json['error'])

    def test_update_amenity(self):
        """Test updating an amenity"""
        create_response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })
        amenity_id = create_response.json['id']

        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "High-Speed Wi-Fi"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("upated", response.json['Sucess'])

    def test_update_amenity_not_found(self):
        """Test updating a non-existent amenity"""
        response = self.client.put('/api/v1/amenities/invalid-id', json={
            "name": "High-Speed Wi-Fi"
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json['error'])

if __name__ == '__main__':
    unittest.main()
