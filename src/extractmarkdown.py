import re
from textnode import TextNode, TextType
from nodedelimiter import split_nodes_delimiter

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def get_delimiter(item, text_type):
    delimiter = ""
    match text_type:
        case TextType.IMAGE:
            delimiter = f"![{item[0]}]({item[1]})"
        case TextType.LINK:
            delimiter = f"[{item[0]}]({item[1]})"
    return delimiter

def get_nodes(string_input, func, text_type):
    new_nodes = []
    if string_input == "":
        return new_nodes
    items = func(string_input)
    if len(items) > 0:
        split_text = string_input.split(get_delimiter(items[0], text_type))
        if len(split_text) > 0:
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(items[0][0], text_type, items[0][1]))
        if len(split_text) > 1:
            new_nodes.extend(get_nodes(split_text[1], func, text_type))
    else:
        new_nodes.append(TextNode(string_input, TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images_found = extract_markdown_images(node.text)
        if node.text_type == TextType.TEXT and len(images_found) > 0:
            new_nodes.extend(get_nodes(node.text, extract_markdown_images, TextType.IMAGE))
        else:
            if node.text != "":
                new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links_found = extract_markdown_links(node.text)
        if node.text_type == TextType.TEXT and len(links_found) > 0:
            new_nodes.extend(get_nodes(node.text, extract_markdown_links, TextType.LINK))
        else:
            if node.text != "":
                new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def markdown_to_blocks(markdown):
    markdown_split = markdown.split("\n\n")
    for i in range(0, len(markdown_split)):
        markdown_split[i] = markdown_split[i].strip("\n").strip()
    return markdown_split