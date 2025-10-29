import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from gesture_module import GestureModule

class TestGestureModule(unittest.TestCase):
    def setUp(self):
        """Set up a GestureModule instance before each test."""
        # Note: This will fail if the model file is not present.
        # For a real-world scenario, you might mock the model loading.
        self.gesture_module = GestureModule()

    def test_translation_dict_initialization(self):
        """Test that the translation dictionary is initialized correctly."""
        self.assertIsNotNone(self.gesture_module.translation_dict)
        self.assertIsInstance(self.gesture_module.translation_dict, dict)
        self.assertGreater(len(self.gesture_module.translation_dict), 0)

    def test_translation_dict_keys(self):
        """Test that the translation dictionary contains the expected keys."""
        expected_keys = [
            "Closed_Fist", "Open_Palm", "Pointing_Up", "Thumb_Down",
            "Thumb_Up", "Victory", "ILoveYou"
        ]
        for key in expected_keys:
            self.assertIn(key, self.gesture_module.translation_dict)

if __name__ == '__main__':
    unittest.main()
