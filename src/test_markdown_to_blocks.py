import unittest
import textwrap

from markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):


    def test_markdown_to_blocks(self):
        md = textwrap.dedent("""
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
    """).strip()
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_markdown_to_blocks_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])


    def test_markdown_to_blocks_only_whitespace(self):
        self.assertEqual(markdown_to_blocks("   \n\n   \n\n"), [])


    def test_markdown_to_blocks_single_block(self):
        md = "This is a single paragraph."
        self.assertEqual(
            markdown_to_blocks(md),
            ["This is a single paragraph."],
        )


    def test_markdown_to_blocks_multiple_blocks(self):
        md = "First block\n\nSecond block\n\nThird block"
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block", "Second block", "Third block"],
        )


    def test_markdown_to_blocks_extra_blank_lines(self):
        md = "\n\nFirst block\n\n\n\nSecond block\n\n"
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block", "Second block"],
        )


    def test_markdown_to_blocks_preserves_single_newlines(self):
        md = "Line one\nLine two\nLine three"
        self.assertEqual(
            markdown_to_blocks(md),
            ["Line one\nLine two\nLine three"],
        )


    def test_markdown_to_blocks_strips_whitespace(self):
        md = "   First block   \n\n   Second block   "
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block", "Second block"],
        )


if __name__ == "__main__":
    unittest.main()