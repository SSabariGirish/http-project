
import unittest

from main import extract_title


class TestExtractTitle(unittest.TestCase):

    def test_simple_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_title_with_whitespace(self):
        self.assertEqual(extract_title("#   Hello World  "), "Hello World")

    def test_title_after_other_content(self):
        md = "Some introductory text\n\n# Tolkien Fan Club\n"
        self.assertEqual(extract_title(md), "Tolkien Fan Club")

    def test_ignores_h2(self):
        md = "## Not an H1\n\n# Actual Title"
        self.assertEqual(extract_title(md), "Actual Title")

    def test_no_h1_raises_exception(self):
        with self.assertRaises(Exception):
            extract_title("## Only an H2")


if __name__ == "__main__":
    unittest.main()
