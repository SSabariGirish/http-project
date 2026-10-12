import unittest
from markdown_extractions import (
    extract_markdown_images,
    extract_markdown_links,
)


class TestExtractMarkdownImages(unittest.TestCase):

    def test_single_image(self):
        text = "![rick roll](https://example.com/rick.gif)"
        expected = [("rick roll", "https://example.com/rick.gif")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        text = (
            "![rick roll](https://example.com/rick.gif) "
            "![obi wan](https://example.com/obi.jpeg)"
        )
        expected = [
            ("rick roll", "https://example.com/rick.gif"),
            ("obi wan", "https://example.com/obi.jpeg"),
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_no_images(self):
        text = "This is just plain text."
        self.assertEqual(extract_markdown_images(text), [])

    def test_empty_string(self):
        self.assertEqual(extract_markdown_images(""), [])

    def test_image_with_surrounding_text(self):
        text = "Before ![cat](https://example.com/cat.png) after."
        expected = [("cat", "https://example.com/cat.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_spaces_in_alt_text(self):
        text = "![a cute little cat](https://example.com/cat.png)"
        expected = [("a cute little cat", "https://example.com/cat.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_empty_alt_text(self):
        text = "![](https://example.com/image.png)"
        expected = [("", "https://example.com/image.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_empty_url(self):
        text = "![cat]()"
        expected = [("cat", "")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_links_are_not_images(self):
        text = "[click here](https://example.com)"
        self.assertEqual(extract_markdown_images(text), [])

    def test_mixed_images_and_links(self):
        text = (
            "[a link](https://example.com) "
            "![an image](https://example.com/image.png)"
        )
        expected = [("an image", "https://example.com/image.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_query_parameters(self):
        text = "![photo](https://example.com/photo.png?size=large&id=5)"
        expected = [
            ("photo", "https://example.com/photo.png?size=large&id=5")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_unclosed_image_syntax(self):
        text = "![cat](https://example.com/cat.png"
        self.assertEqual(extract_markdown_images(text), [])


class TestExtractMarkdownLinks(unittest.TestCase):

    def test_single_link(self):
        text = "[to boot dev](https://www.boot.dev)"
        expected = [("to boot dev", "https://www.boot.dev")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        text = (
            "[to boot dev](https://www.boot.dev) "
            "[to youtube](https://www.youtube.com/@bootdotdev)"
        )
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_no_links(self):
        text = "This is just plain text."
        self.assertEqual(extract_markdown_links(text), [])

    def test_empty_string(self):
        self.assertEqual(extract_markdown_links(""), [])

    def test_link_with_surrounding_text(self):
        text = "Before [click here](https://example.com) after."
        expected = [("click here", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_spaces_in_text(self):
        text = "[visit the official website](https://example.com)"
        expected = [
            ("visit the official website", "https://example.com")
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_empty_text(self):
        text = "[](https://example.com)"
        expected = [("", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_empty_url(self):
        text = "[click here]()"
        expected = [("click here", "")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_images_are_not_links(self):
        text = "![cat](https://example.com/cat.png)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_mixed_links_and_images(self):
        text = (
            "[a link](https://example.com) "
            "![an image](https://example.com/image.png)"
        )
        expected = [("a link", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_query_parameters(self):
        text = "[search](https://example.com/search?q=python&page=2)"
        expected = [
            ("search", "https://example.com/search?q=python&page=2")
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_unclosed_link_syntax(self):
        text = "[click here](https://example.com"
        self.assertEqual(extract_markdown_links(text), [])


if __name__ == "__main__":
    unittest.main()