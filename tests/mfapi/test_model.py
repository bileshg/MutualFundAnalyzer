import unittest

from src.mfapi.model import SchemeSearchResult


class TestMFAPIModelConfig(unittest.TestCase):
    def test_field_name_construction_is_supported(self):
        result = SchemeSearchResult(scheme_code=123, scheme_name="Test Scheme")

        self.assertEqual(result.scheme_code, 123)
        self.assertEqual(result.scheme_name, "Test Scheme")

    def test_string_fields_are_stripped(self):
        result = SchemeSearchResult.model_validate(
            {"schemeCode": 123, "schemeName": "  Test Scheme  "}
        )

        self.assertEqual(result.scheme_name, "Test Scheme")


if __name__ == "__main__":
    unittest.main()
