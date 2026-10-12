import unittest

from block_to_block import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        self.assertEqual(block_to_block_type("# Hello"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Hello"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Hello"), BlockType.HEADING)

    def test_invalid_heading(self):
        self.assertEqual(block_to_block_type("####### Hello"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#Hello"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Hello # Heading"), BlockType.PARAGRAPH)

    def test_code_block(self):
        self.assertEqual(
            block_to_block_type("```\nprint('Hello')\n```"),
            BlockType.CODE,
        )
        self.assertEqual(
            block_to_block_type("```\nline 1\nline 2\n```"),
            BlockType.CODE,
        )

    def test_invalid_code_block(self):
        self.assertEqual(
            block_to_block_type("```\nprint('Hello')"),
            BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type("print('Hello')\n```"),
            BlockType.PARAGRAPH,
        )

    def test_quote_block(self):
        self.assertEqual(
            block_to_block_type("> Hello\n> World"),
            BlockType.QUOTE,
        )
        self.assertEqual(
            block_to_block_type(">Hello\n>World"),
            BlockType.QUOTE,
        )

    def test_invalid_quote_block(self):
        self.assertEqual(
            block_to_block_type("> Hello\nWorld"),
            BlockType.PARAGRAPH,
        )

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- Apple\n- Banana\n- Orange"),
            BlockType.UNORDERED_LIST,
        )

    def test_invalid_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- Apple\nBanana\n- Orange"),
            BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type("-Apple\n- Banana"),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. First\n2. Second\n3. Third"),
            BlockType.ORDERED_LIST,
        )

    def test_invalid_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. First\n3. Second"),
            BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type("2. First\n3. Second"),
            BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type("1.First\n2. Second"),
            BlockType.PARAGRAPH,
        )

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("This is a normal paragraph."),
            BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type("Hello\nThis is another line."),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()
