import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):


    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!", None)
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me", {"href": "https://example.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://example.com">Click me</a>'
        )

    def test_leaf_to_html_raw_text(self):
        node = LeafNode(None, "Just plain text", None)
        self.assertEqual(node.to_html(), "Just plain text")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None, None)

        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_different_tag(self):
        node = LeafNode("b", "Bold text", None)
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    def test_leaf_repr(self):
        node = LeafNode("p", "Hello, world!", None)
        self.assertEqual(
            repr(node),
            "LeafNode(p, Hello, world!, )"
        )



if __name__ == "__main__":
    unittest.main()

