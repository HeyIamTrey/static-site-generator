import unittest
from inline_markdown import(
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_code(self):
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

    def test_delim_not_text(self):
        node = TextNode("This is a test for the node **not** being TextType.TEXT", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a test for the node **not** being TextType.TEXT", TextType.BOLD)
            ]
        )

    def test_delim_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            []
        )

    def test_delim_just_markdown_word(self):
        node = TextNode("**bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [TextNode("bold", TextType.BOLD)]
        )

    def test_delim_one_pair(self):
        node = TextNode("This is a **test", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_delim_multiple_nodes(self):
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

    def test_delim_multiple_delims(self):
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

    def test_delim_bold_and_italic(self):
        node = TextNode("This test has a **bold** and _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This test has a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT)
            ]
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown__multiple_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ], 
            matches
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ],
            matches
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            new_nodes
        )

    def test_split_images_multiple_nodes(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        node2 = TextNode("This is also text with an image ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("This is also text with an image ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_multiple_nodes(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.TEXT)
        node2 = TextNode("This is also text with a link [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        new_nodes = split_nodes_link([node, node2])
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("This is also text with a link ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            new_nodes
        )

    def test_split_images_image_first(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) This is text with an image first", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" This is text with an image first", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_link_first(self):
        node = TextNode("[to boot dev](https://www.boot.dev) This is text with a link first", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" This is text with a link first", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_images_wrong_text_type(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        node2 = TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
        new_nodes = split_nodes_image([node, node2])
        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes
        )

    def test_split_links_wrong_text_type(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.TEXT)
        node2 = TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
        new_nodes = split_nodes_link([node, node2])
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            new_nodes
        )

    def test_split_images_just_image(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")], new_nodes
        )

    def test_split_links_just_image(self):
        node = TextNode("[to boot dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")], new_nodes
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

    def test_text_to_textnodes_empty_string(self):
        text = ""
        new_nodes = text_to_textnodes(text)
        self.assertEqual(new_nodes, [])

    def test_text_to_textnodes_no_markdown(self):
        text = "This text does not include any form of markdown syntax"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [TextNode("This text does not include any form of markdown syntax", TextType.TEXT)],
            new_nodes
        )

    def test_text_to_textnodes(self):
        text = "This text only includes **one** form of markdown syntax"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This text only includes ", TextType.TEXT),
                TextNode("one", TextType.BOLD),
                TextNode(" form of markdown syntax", TextType.TEXT)
            ],
            new_nodes
        )

    def test_text_to_textnodes_multiple(self):
        text = "This text **includes** multiple **bold** words as well as an _italic_ word"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This text ", TextType.TEXT),
                TextNode("includes", TextType.BOLD),
                TextNode(" multiple ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" words as well as an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT)
            ],
            new_nodes
        )

    def test_text_to_textnodes_unclosed_delim(self):
        text = "This text **includes an _unclosed_ delimiter"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)

    def test_text_to_textnodes_empty_delim(self):
        text = "This text includes **** an _empty_ delimiter"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This text includes ", TextType.TEXT),
                TextNode(" an ", TextType.TEXT),
                TextNode("empty", TextType.ITALIC),
                TextNode(" delimiter", TextType.TEXT)
            ],
            new_nodes
        )

if __name__ == "__main__":
    unittest.main()