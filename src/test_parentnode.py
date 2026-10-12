import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child", None)
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span></div>"
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild", None)
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_multiple_children(self):
        child1 = LeafNode("span", "Hello", None)
        child2 = LeafNode("b", "World", None)
        parent = ParentNode("div", [child1, child2])

        self.assertEqual(
            parent.to_html(),
            "<div><span>Hello</span><b>World</b></div>"
        )

    def test_to_html_no_tag(self):
        parent = ParentNode(None, [LeafNode("b", "child", None)])

        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_no_children(self):
        parent = ParentNode("div", None)

        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_empty_children(self):
        parent = ParentNode("div", [])

        self.assertEqual(parent.to_html(), "<div></div>")

if __name__ == "__main__":
    unittest.main()
