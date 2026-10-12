import unittest
from textnode import TextNode, TextType
from node_splitter import split_nodes_delimiter, split_nodes_image, split_nodes_link


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_basic_code_split(self):
        node = TextNode("This is `code` text", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_multiple_code_blocks(self):
        node = TextNode("`first` and `second`", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("first", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.CODE),
        ]

        self.assertEqual(result, expected)

    def test_entire_text_is_code(self):
        node = TextNode("`code`", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [TextNode("code", TextType.CODE)]

        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        node = TextNode("Just normal text", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [TextNode("Just normal text", TextType.TEXT)]

        self.assertEqual(result, expected)

    def test_unmatched_opening_delimiter(self):
        node = TextNode("This is `unfinished code", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_unmatched_closing_delimiter(self):
        node = TextNode("This is code`", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_already_formatted_node_is_preserved(self):
        node = TextNode("already bold", TextType.BOLD)

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(result, [node])

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("Hello `world`", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("Another `example`", TextType.TEXT),
        ]

        result = split_nodes_delimiter(nodes, "`", TextType.CODE)

        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.CODE),
            TextNode("already bold", TextType.BOLD),
            TextNode("Another ", TextType.TEXT),
            TextNode("example", TextType.CODE),
        ]

        self.assertEqual(result, expected)

    def test_invalid_text_type(self):
        node = TextNode("Some text", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", "invalid")

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_single_image(self):
        node = TextNode(
            "![cat](https://example.com/cat.png)",
            TextType.TEXT,
        )

        self.assertListEqual(
            [TextNode("cat", TextType.IMAGE, "https://example.com/cat.png")],
            split_nodes_image([node]),
        )

    def test_no_images(self):
        node = TextNode("Just normal text.", TextType.TEXT)

        self.assertListEqual(
            [node],
            split_nodes_image([node]),
        )

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)

        self.assertListEqual(
            [node],
            split_nodes_image([node]),
        )

    def test_image_at_start(self):
        node = TextNode(
            "![cat](https://example.com/cat.png) follows",
            TextType.TEXT,
        )

        self.assertListEqual(
            [
                TextNode("cat", TextType.IMAGE, "https://example.com/cat.png"),
                TextNode(" follows", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_image_at_end(self):
        node = TextNode(
            "Look at this ![cat](https://example.com/cat.png)",
            TextType.TEXT,
        )

        self.assertListEqual(
            [
                TextNode("Look at this ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "https://example.com/cat.png"),
            ],
            split_nodes_image([node]),
        )

    def test_preserve_existing_non_text_node(self):
        node = TextNode("already an image", TextType.IMAGE, "cat.png")

        self.assertListEqual(
            [node],
            split_nodes_image([node]),
        )

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("Hello ![cat](cat.png)", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("![dog](dog.png) goodbye", TextType.TEXT),
        ]

        self.assertListEqual(
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "cat.png"),
                TextNode("Already bold", TextType.BOLD),
                TextNode("dog", TextType.IMAGE, "dog.png"),
                TextNode(" goodbye", TextType.TEXT),
            ],
            split_nodes_image(nodes),
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube",
                    TextType.LINK,
                    "https://www.youtube.com/@bootdotdev",
                ),
            ],
            new_nodes,
        )

    def test_single_link(self):
        node = TextNode(
            "[Boot.dev](https://www.boot.dev)",
            TextType.TEXT,
        )

        self.assertListEqual(
            [TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")],
            split_nodes_link([node]),
        )

    def test_no_links(self):
        node = TextNode("Just normal text.", TextType.TEXT)

        self.assertListEqual(
            [node],
            split_nodes_link([node]),
        )

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)

        self.assertListEqual(
            [node],
            split_nodes_link([node]),
        )

    def test_link_at_start(self):
        node = TextNode(
            "[Boot.dev](https://www.boot.dev) is useful",
            TextType.TEXT,
        )

        self.assertListEqual(
            [
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" is useful", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_link_at_end(self):
        node = TextNode(
            "Visit [Boot.dev](https://www.boot.dev)",
            TextType.TEXT,
        )

        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
            ],
            split_nodes_link([node]),
        )

    def test_preserve_existing_non_text_node(self):
        node = TextNode("already a link", TextType.LINK, "https://example.com")

        self.assertListEqual(
            [node],
            split_nodes_link([node]),
        )

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("Visit [Boot.dev](https://www.boot.dev)", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("[YouTube](https://youtube.com) today", TextType.TEXT),
        ]

        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("Already bold", TextType.BOLD),
                TextNode("YouTube", TextType.LINK, "https://youtube.com"),
                TextNode(" today", TextType.TEXT),
            ],
            split_nodes_link(nodes),
        )

    def test_image_is_not_split_as_link(self):
        node = TextNode(
            "Look at ![cat](https://example.com/cat.png)",
            TextType.TEXT,
        )

        self.assertListEqual(
            [node],
            split_nodes_link([node]),
        )


if __name__ == "__main__":
    unittest.main()