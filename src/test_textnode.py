import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from splitnodes import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is an image", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a test", TextType.LINK)
        node2 = TextNode("This is different", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a url test", TextType.ITALIC, "https://www.google.com")
        node2 = TextNode("This is a url test", TextType.ITALIC, "https://www.google.com")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a test", TextType.LINK, "https://www.google.com")
        self.assertEqual("TextNode(This is a test, link, https://www.google.com)", repr(node))

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "<b>This is a text node</b>")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "<i>This is a text node</i>")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "<code>This is a text node</code>")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, {"href": "https://www.google.com"})
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), '<a href="https://www.google.com">This is a text node</a>')

    def test_image(self):
        node = TextNode("alt text", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src":"https://www.google.com", "alt": "alt text"}
        )
        self.assertEqual(html_node.to_html(), '<img src="https://www.google.com" alt="alt text"></img>')

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT), 
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT)
            ]
        )

    def test_split_nodes_delimiter_not_text(self):
        node = TextNode("This is a test for the node **not** being TextType.TEXT", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a test for the node **not** being TextType.TEXT", TextType.BOLD)
            ]
        )

    def test_split_nodes_delimiter_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            []
        )
    
    def test_split_nodes_delimeter_just_markdown_word(self):
        node = TextNode("**bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [TextNode("bold", TextType.BOLD)]
        )

    def test_split_nodes_delimiter_just_delimiters(self):
        node = TextNode("text **** more text", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_nodes_delimiter_one_pair(self):
        node = TextNode("This is a **test", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_nodes_delimiter_multiple_nodes(self):
        node = TextNode("This is the **first** test", TextType.TEXT)
        node2 = TextNode("**This** is the second test", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is the ", TextType.TEXT),
                TextNode("first", TextType.BOLD),
                TextNode(" test", TextType.TEXT),
                TextNode("This", TextType.BOLD),
                TextNode(" is the second test", TextType.TEXT)
            ]
        )

    def test_split_nodes_delimiter_multiple_delimiters(self):
        node = TextNode("**This** test has **multiple** bold words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This", TextType.BOLD),
                TextNode(" test has ", TextType.TEXT),
                TextNode("multiple", TextType.BOLD),
                TextNode(" bold words", TextType.TEXT)
            ]
        )

if __name__ == "__main__":
    unittest.main()