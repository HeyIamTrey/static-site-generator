from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    split_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            split_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception("invalid markdown syntax: There is no delimiter pair")
            for i in range(len(split_text)):
                if i % 2 == 1 and split_text[i] == "":
                    raise Exception("invalid markdown syntax: There is no text between the delimiters")
                elif i % 2 == 0:
                    split_nodes.append(TextNode(split_text[i], TextType.TEXT))
                else:
                    split_nodes.append(TextNode(split_text[i], text_type))
    for node in split_nodes:
        if node.text != "":
            new_nodes.append(node)
    return new_nodes