import unittest

from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):

    def test_plain_text(self):
        text = "Hello world"
        expected = [
            TextNode("Hello world", TextType.TEXT)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_bold(self):
        text = "This is **bold** text"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_italic(self):
        text = "This is _italic_ text"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_code(self):
        text = "Run `print('hello')` now"
        expected = [
            TextNode("Run ", TextType.TEXT),
            TextNode("print('hello')", TextType.CODE),
            TextNode(" now", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_image(self):
        text = "Look at this ![obi wan image](https://example.com/obi.jpg)"
        expected = [
            TextNode("Look at this ", TextType.TEXT),
            TextNode(
                "obi wan image",
                TextType.IMAGE,
                "https://example.com/obi.jpg",
            ),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_link(self):
        text = "Visit [Boot.dev](https://boot.dev) today"
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
            TextNode(" today", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_multiple_markdown_formats(self):
        text = "A **bold** and _italic_ word with `code`"
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_image_and_link_together(self):
        text = (
            "Image ![cat](https://example.com/cat.png) "
            "and [website](https://example.com)"
        )
        expected = [
            TextNode("Image ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "https://example.com/cat.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("website", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_full_example(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image",
                TextType.IMAGE,
                "https://i.imgur.com/fJRm4Vk.jpeg",
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_empty_string(self):
        self.assertEqual(text_to_textnodes(""), [])

    def test_multiple_bold_sections(self):
        text = "**first** then **second**"
        expected = [
            TextNode("first", TextType.BOLD),
            TextNode(" then ", TextType.TEXT),
            TextNode("second", TextType.BOLD),
        ]
        self.assertEqual(text_to_textnodes(text), expected)


if __name__ == "__main__":
    unittest.main()