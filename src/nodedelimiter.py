from textnode import TextNode, TextType
from leafnode import LeafNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if len(old_nodes) >= 1:
        for node in old_nodes:
            if delimiter not in node.text or node.text_type != TextType.TEXT:
                new_nodes.append(node)
                continue
            split_text_list = node.text.split(delimiter)
            if len(split_text_list) % 2 == 0:
                raise Exception(f"Invalid syntax - missing closing '{delimiter}' at '{split_text_list[-1]}'")
            for i in range(0, len(split_text_list)):
                current_word = split_text_list[i]
                if i % 2 == 0:
                    if current_word != "":
                        new_nodes.append(TextNode(current_word, TextType.TEXT))
                else:
                    if current_word != "":
                        new_nodes.append(TextNode(current_word, text_type))
    return new_nodes