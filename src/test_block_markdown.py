import unittest
from block_markdown import(
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
)

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_block(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_leading_trailing_newlines(self):
        md = """

This is block one

This is block two

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is block one",
                "This is block two",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = "This is just one block of text."
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is just one block of text.",
            ],
        )

    def test_markdown_to_blocks_empty_input(self):
        md = "   \n\n \t \n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        )

    def test_block_to_block_type_heading(self):
        block1 = "# This is a heading"
        block2 = "## This is also a heading"
        block3 = "### This is also, also a heading"
        block4 = "#### This is also, also, also, a heading"
        block5 = "##### This is also, also, also, also a heading"
        block6 = "###### This is also, also, also, also, also a heading"

        block_type1 = block_to_block_type(block1)
        block_type2 = block_to_block_type(block2)
        block_type3 = block_to_block_type(block3)
        block_type4 = block_to_block_type(block4)
        block_type5 = block_to_block_type(block5)
        block_type6 = block_to_block_type(block6)

        self.assertEqual(block_type1, BlockType.HEADING)
        self.assertEqual(block_type2, BlockType.HEADING)
        self.assertEqual(block_type3, BlockType.HEADING)
        self.assertEqual(block_type4, BlockType.HEADING)
        self.assertEqual(block_type5, BlockType.HEADING)
        self.assertEqual(block_type6, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = "```\nThis is a block of code text\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)
    
    def test_block_to_block_type_quote(self):
        block = "> This is a block\n> of quote text"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_ulist(self):
        block = "- This is a block\n- of unordered list text"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ULIST)

    def test_block_to_block_text_olist(self):
        block = "1. This is a block\n2. of ordered list text"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.OLIST)

    def test_block_to_block_type_paragraph(self):
        block = "This is a block of paragraph text"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
### This is a level three heading

This is paragraph text

###### This is a level six heading
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is a level three heading</h3><p>This is paragraph text</p><h6>This is a level six heading</h6></div>"
        )

    def test_quoteblock(self):
        md = """
>This is a block
>of **quote** text

This is paragraph text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a block of <b>quote</b> text</blockquote><p>This is paragraph text</p></div>"
        )

    def test_olist(self):
        md = """
1. This is the **first** item
2. This is the _second_ item
3. This is the third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is the <b>first</b> item</li><li>This is the <i>second</i> item</li><li>This is the third item</li></ol></div>"
        )

    def test_ulist(self):
        md = """
- This is the **first** item
- This is the _second_ item
- This is the third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is the <b>first</b> item</li><li>This is the <i>second</i> item</li><li>This is the third item</li></ul></div>"
        )

    def test_both_lists(self):
        md = """
1. This is the **first** item
2. This is the _second_ item
3. This is the third item

- This is the **first** item
- This is the _second_ item
- This is the third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is the <b>first</b> item</li><li>This is the <i>second</i> item</li><li>This is the third item</li></ol><ul><li>This is the <b>first</b> item</li><li>This is the <i>second</i> item</li><li>This is the third item</li></ul></div>"
        )

if __name__ == "__main__":
    unittest.main()