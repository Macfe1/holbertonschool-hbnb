import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        """Set up the test client."""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        """Test creating a new user."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
        self.assertEqual(response.json['email'], "john.doe@example.com")

    def test_create_user_duplicate_email(self):
        """Test creating a user with a duplicate email."""
        # First user creation
        self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        # Attempting to create another user with the same email
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Smith",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'Email already registered')

    def test_get_all_users(self):
        """Test retrieving all users."""
        # Create a user first
        self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Wonder",
            "email": "alice.wonder@example.com"
        })
        # Retrieve all users
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))
        self.assertGreater(len(response.json), 0)

    def test_get_user_by_id(self):
        """Test retrieving a user by ID."""
        # Create a user first
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "Mark",
            "last_name": "Twain",
            "email": "mark.twain@example.com"
        })
        user_id = create_response.json['id']

        # Retrieve the user by ID
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], "mark.twain@example.com")

    def test_get_user_by_invalid_id(self):
        """Test retrieving a user by an invalid ID."""
        response = self.client.get('/api/v1/users/invalid-id')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'User not found')

    def test_update_user(self):
        """Test updating a user's information."""
        # Create a user first
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "Sarah",
            "last_name": "Connor",
            "email": "sarah.connor@example.com"
        })
        user_id = create_response.json['id']

        # Update the user's information
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Sarah",
            "last_name": "Reese",
            "email": "sarah.connor@example.com"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], 'User updated successfully')

    def test_update_user_invalid_id(self):
        """Test updating a user with an invalid ID."""
        response = self.client.put('/api/v1/users/invalid-id', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'User not found')

if __name__ == '__main__':
    unittest.main()

