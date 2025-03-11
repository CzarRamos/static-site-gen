import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 0,
    HEADING = 1,
    CODE = 2,
    QUOTE = 3,
    UNORDERED_LIST = 4,
    ORDERED_LIST = 5

def is_heading(string_input):
    found_lines = re.findall(r"^([#]+) ", string_input)
    #print(f"found lines: {found_lines}")
    return len(found_lines) > 0

def is_code(string_input):
    found_lines = re.findall(r"^(```)(?!`)[\s\S]+(?<!`)(```$)", string_input)
    return len(found_lines) > 0

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