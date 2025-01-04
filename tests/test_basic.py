import os
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from bizcard_ai import get_image_information


class TestBasicFunctionality(unittest.TestCase):
    def test_business_card_core_details(self):
        json_data = get_image_information(
            os.path.join(
                os.path.dirname(__file__),
                "examples",
                "business_card_example1.png",
            )
        )
        self.assertEqual(json_data.get("name").lower(), "james johnson deo")
        self.assertEqual(json_data.get("phone_numbers"), ["+123-456-789"])
        self.assertEqual(json_data.get("email").lower(), "jamesdeo@gmail.com")
        self.assertEqual(
            json_data.get("address")
            .lower()
            .replace("\n", " ")
            .replace(",", ""),
            "204 s. pacific ave. allison park pa 15101",
        )
        self.assertEqual(json_data.get("role").lower(), "project manager")
        self.assertEqual(json_data.get("company").lower(), "company")

    def test_incomplete_business_card(self):
        json_data = get_image_information(
            os.path.join(
                os.path.dirname(__file__),
                "examples",
                "business_card_example2.png",
            )
        )
        self.assertEqual(json_data.get("name").lower(), "evan calkins")
        self.assertEqual(
            [
                phone.replace(" ", "")
                for phone in json_data.get("phone_numbers")
            ],
            ["3602197026"],
        )
        self.assertEqual(json_data.get("email").lower(), "evan@hobanpress.com")
        self.assertEqual(json_data.get("address").lower(), "")
        self.assertEqual(json_data.get("role").lower(), "")


if __name__ == "__main__":
    unittest.main()
