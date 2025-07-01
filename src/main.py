from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    text_node = TextNode("This is some anchor text", TextType.LINK, "https://bootdev.com")
    print(text_node)
    
main()