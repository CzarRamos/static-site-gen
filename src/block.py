import re
from enum import Enum
from textnode import TextType

class BlockType(Enum):
    PARAGRAPH = 0,
    HEADING = 1,
    CODE = 2,
    QUOTE = 3,
    UNORDERED_LIST = 4,
    ORDERED_LIST = 5

def get_tag_from_TextType(text_type):
    match text_type:
        case TextType.BOLD:
            return "b"
        case TextType.ITALIC:
            return "i"
        case TextType.CODE:
            return "code"
        case TextType.LINK:
            return "a"
        case TextType.IMAGE:
            return "img"
        case _: 
            return ""

def is_heading(string_input):
    found_lines = re.findall(r"^([#]{1,6}) ", string_input)
    return len(found_lines) > 0

def is_code(string_input):
    found_lines = re.findall(r"^(```)(?!`)[\s\S]+(?<!`)(```$)", string_input)
    found_lines2 = re.findall(r"(```)", string_input)
    return (len(found_lines) > 0 and len(found_lines2) == 2)

def is_quote(string_input):
    input_split = string_input.split("\n")
    for text in input_split:
        found_lines = re.findall(r"^(>)", text)
        if len(found_lines) == 0:
            return False
    return True

def is_unordered_list(string_input):
    input_split = string_input.split("\n")
    for text in input_split:
        found_lines = re.findall(r"^(- )", text)
        if len(found_lines) == 0:
            return False
    return True

def is_ordered_list(string_input):
    input_split = string_input.split("\n")
    for i in range(0, len(input_split)):
        found_lines = re.findall(r"^(\d.)", input_split[i])
        if f"{i+1}." not in found_lines:
            return False
    return True

def block_to_block_type(markdown):
    if is_heading(markdown):
        return BlockType.HEADING
    if is_code(markdown):
        return BlockType.CODE
    if is_quote(markdown):
        return BlockType.QUOTE
    if is_unordered_list(markdown):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(markdown):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def return_within_range(number, min, max):
    if number >= min and number <= max:
        return number
    elif number <= min:
        return min
    else:
        return max

def get_header_number(markdown):
    count = -1
    found_lines = re.findall(r"^([#]{1,6})", markdown)
    if len(found_lines) > 0:
        symbols = found_lines[-1]
        count = return_within_range((len(symbols)), 1, 6)
    return count

def wrap_heading(markdown):
    count = get_header_number(markdown)
    return f"<h{count}>{markdown[count:].strip()}</h{count}>"

def wrap_paragraph(markdown):
    return f"<p>{markdown}</p>"

def wrap_code(markdown):
    return f"<pre><code>{markdown.strip()[3:-3]}</code></pre>"

