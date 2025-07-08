import unittest
from block_markdown import(
    BlockType,
    markdown_to_blocks,
    block_to_block_type
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

if __name__ == "__main__":
    unittest.main()