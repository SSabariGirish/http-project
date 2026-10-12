import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_init(self):
        node = HTMLNode("p", "Hello", None, {"class": "greeting"})

        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"class": "greeting"})

    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "Google",
            None,
            {"href": "https://google.com", "target": "_blank"}
        )

        self.assertEqual(
            node.props_to_html(),
            'href="https://google.com" target="_blank"'
        )

    def test_props_to_html_none(self):
        node = HTMLNode("p", "Hello", None, None)

        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode("p", "Hello", None, {})

        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("p", "Hello", None, {"class": "greeting"})

        self.assertEqual(
            repr(node),
            'HTMLNode(p, Hello, None, class="greeting")'
        )

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "Hello", None, None)

        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
