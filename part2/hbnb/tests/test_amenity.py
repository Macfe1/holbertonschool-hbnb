from app.models.amenity import Amenity
from app.models.basemodel import BaseModel
import unittest

class TestAmenity(unittest.TestCase):

    def test_amenity_creation(self):
        amenity = Amenity(name="Wi-Fi")
        assert amenity.name == "Wi-Fi"
        print("Amenity creation test passed!")

if __name__ == '__main__':
    unittest.main()
