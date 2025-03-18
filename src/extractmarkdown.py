import re
from textnode import TextNode, TextType
from nodedelimiter import split_nodes_delimiter
from block import *
from htmlnode import HTMLNode
from leafnode import LeafNode
from codeleafnode import CodeLeafNode
from imageleafnode import ImageLeafNode
from parentnode import ParentNode
from constants import *

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
    
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    return new_nodes

def text_nodes_to_children_nodes(old_nodes):
    output_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.CODE:
            output_nodes.append(CodeLeafNode(CODE_TAG, old_node.text, {"url": old_node.url}))
        elif old_node.text_type == TextType.IMAGE:
            output_nodes.append(ImageLeafNode(IMAGE_TAG, {"src": old_node.url, "alt": old_node.text}))
        else:
            output_nodes.append(LeafNode(get_tag_from_TextType(old_node.text_type), old_node.text, {"href": old_node.url}))
    return output_nodes

def markdown_to_blocks(markdown):
    markdown_split = re.split(r'\n\n', markdown)
    for i in range(0, len(markdown_split)):
        markdown_split[i] = markdown_split[i].strip("\n").strip()
    return markdown_split

def get_header_node(markdown):
    count = get_header_number(markdown)
    adjusted_markdown = markdown[count:].strip()
    text_nodes = text_to_textnodes(adjusted_markdown)
    children_nodes = text_nodes_to_children_nodes(text_nodes)
    if len(children_nodes) > 1:
        return ParentNode(f"{HEADER_TAG}{count}", children_nodes)
    return LeafNode(f"{HEADER_TAG}{count}", adjusted_markdown)

def get_code_node(markdown):
    return CodeLeafNode(CODE_TAG, markdown.strip("```").strip())

def get_quote_node(markdown):
    adjusted_markdown = re.sub(r'(\n>|^> )', r'', markdown)
    text_nodes = text_to_textnodes(adjusted_markdown)
    children_nodes = text_nodes_to_children_nodes(text_nodes)
    if len(children_nodes):
        return ParentNode(QUOTE_TAG, children_nodes)
    return LeafNode(QUOTE_TAG, adjusted_markdown[count:])

def get_paragraph_node(markdown):
    text_nodes = text_to_textnodes(markdown)
    children_nodes = text_nodes_to_children_nodes(text_nodes)
    if len(children_nodes) > 0:
        return ParentNode(PARAGRAPH_TAG, children_nodes)
    return LeafNode(PARAGRAPH_TAG, markdown)

def get_list_item_nodes(markdown):
    text_nodes = text_to_textnodes(markdown)
    children_nodes = text_nodes_to_children_nodes(text_nodes)
    return children_nodes

def get_unordered_list_node(markdown):
    markdown_split = re.split(r'\n?- ', markdown)
    item_parent_nodes = []
    for item in markdown_split:
        if item != "":
            children_nodes = get_list_item_nodes(item)
            item_parent_nodes.append(ParentNode(LIST_ITEM_TAG, children_nodes))
    return ParentNode(UNORDERED_LIST_TAG, item_parent_nodes)

def get_ordered_list_node(markdown):
    markdown_split = re.split(r'\n?\d\. ', markdown)
    item_parent_nodes = []
    for item in markdown_split:
        if item != "":
            children_nodes = get_list_item_nodes(item)
            item_parent_nodes.append(ParentNode(LIST_ITEM_TAG, children_nodes))
    return ParentNode(ORDERED_LIST_TAG, item_parent_nodes)

def markdown_to_html_node(markdown):
    output_nodes = []
    blocks = markdown_to_blocks(markdown)
    text_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                output_nodes.append(get_header_node(block))
            case BlockType.PARAGRAPH:
                output_nodes.append(get_paragraph_node(block))
            case BlockType.CODE:
                output_nodes.append(get_code_node(block))
            case BlockType.QUOTE:
                output_nodes.append(get_quote_node(block))
            case BlockType.UNORDERED_LIST:
                output_nodes.append(get_unordered_list_node(block))
            case BlockType.ORDERED_LIST:
                output_nodes.append(get_ordered_list_node(block))
            case _:
                raise ValueError(f"'{block}' does not have a valid block type")
    return ParentNode(DIV_TAG, output_nodes)

def get_html_string_from_markdown(markdown):
    return markdown_to_html_node(markdown).to_html()