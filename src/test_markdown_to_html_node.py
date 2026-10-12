import unittest

from markdown_to_html_node import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>"
            "<p>This is another paragraph with <i>italic</i> text and "
            "<code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """```
This is text that _should_ remain
the **same** even with inline stuff
```"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><pre><code>This is text that _should_ remain\n"
            "the **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "# Hello World"

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><h1>Hello World</h1></div>",
        )

    def test_multiple_heading_levels(self):
        md = """# Heading 1

## Heading 2

### Heading 3

###### Heading 6"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><h1>Heading 1</h1>"
            "<h2>Heading 2</h2>"
            "<h3>Heading 3</h3>"
            "<h6>Heading 6</h6></div>",
        )

    def test_heading_with_inline_formatting(self):
        md = "# Hello **World**"

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><h1>Hello <b>World</b></h1></div>",
        )

    def test_quote(self):
        md = """> This is a quote
> It spans multiple lines
> And has **bold text**"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is a quote It spans multiple lines "
            "And has <b>bold text</b></blockquote></div>",
        )

    def test_unordered_list(self):
        md = """- Apple
- Banana
- Orange"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><ul><li>Apple</li><li>Banana</li>"
            "<li>Orange</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """1. First
2. Second
3. Third"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><ol><li>First</li><li>Second</li>"
            "<li>Third</li></ol></div>",
        )

    def test_list_items_with_inline_formatting(self):
        md = """- **Bold item**
- _Italic item_
- `Code item`"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><ul><li><b>Bold item</b></li>"
            "<li><i>Italic item</i></li>"
            "<li><code>Code item</code></li></ul></div>",
        )

    def test_mixed_block_types(self):
        md = """# My Document

A normal paragraph.

> A famous quote

- One
- Two

1. First
2. Second"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><h1>My Document</h1>"
            "<p>A normal paragraph.</p>"
            "<blockquote>A famous quote</blockquote>"
            "<ul><li>One</li><li>Two</li></ul>"
            "<ol><li>First</li><li>Second</li></ol></div>",
        )

    def test_empty_document(self):
        md = ""

        node = markdown_to_html_node(md)

        self.assertEqual(node.to_html(), "<div></div>")


if __name__ == "__main__":
    unittest.main()