import unittest

from src.utils.string_utils import normalize_string, pascal_case, snake_case


class TestStringUtils(unittest.TestCase):
    def test_normalize_basic(self):
        s = "  Hello   WORLD  "
        expected = "hello world"
        self.assertEqual(normalize_string(s), expected)

    def test_normalize_whitespace_types(self):
        s = "Hello\t\n  WORLD  Foo"
        expected = "hello world foo"
        self.assertEqual(normalize_string(s), expected)

    def test_normalize_empty(self):
        self.assertEqual(normalize_string(""), "")

    def test_pascal_case_basic(self):
        s = "hello world"
        expected = "HelloWorld"
        self.assertEqual(pascal_case(s), expected)

    def test_pascal_case_multiple_whitespace(self):
        s = "  multiple   words here "
        expected = "MultipleWordsHere"
        self.assertEqual(pascal_case(s), expected)

    def test_pascal_case_punctuation_preserved(self):
        # The implementation simply splits on whitespace and capitalizes each chunk,
        # so punctuation inside words is preserved but casing within that chunk
        # follows Python's str.capitalize() behavior.
        s = "already-Pascal case"
        expected = "Already-pascalCase"
        self.assertEqual(pascal_case(s), expected)

    def test_snake_case_basic(self):
        s = "Hello World"
        expected = "hello_world"
        self.assertEqual(snake_case(s), expected)

    def test_snake_case_multiple_whitespace_and_case(self):
        s = "  MixED   Case  Words  "
        expected = "mixed_case_words"
        self.assertEqual(snake_case(s), expected)

    def test_non_string_inputs_raise_attribute_error(self):
        # The functions expect a str and will raise AttributeError for None
        with self.assertRaises(AttributeError):
            normalize_string(None)
        with self.assertRaises(AttributeError):
            pascal_case(None)
        with self.assertRaises(AttributeError):
            snake_case(None)


if __name__ == "__main__":
    unittest.main()
