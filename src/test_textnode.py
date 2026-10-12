import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_different_text(self):
        node = TextNode("hello", TextType.BOLD)
        node2 = TextNode("goodbye", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_different_type(self):
        node = TextNode("hello", TextType.BOLD)
        node2 = TextNode("hello", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_different_url(self):
        node = TextNode("Google", TextType.LINK, "google.com")
        node2 = TextNode("Google", TextType.LINK, "example.com")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node, LeafNode(None, "Hello, world!", None))

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node, LeafNode("b", "Bold text", None))

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node, LeafNode("i", "Italic text", None))

    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node, LeafNode("code", "print('hello')", None))

    def test_link(self):
        node = TextNode("Google", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node,
            LeafNode("a", "Google", {"href": "https://google.com"})
        )

    def test_image(self):
        node = TextNode("A cat", TextType.IMAGE, "cat.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node,
            LeafNode("img", None, {"src": "cat.png", "alt": "A cat"})
        )


if __name__ == "__main__":
    unittest.main()

