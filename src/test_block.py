import unittest
from block import *

class TextBlock(unittest.TestCase):

    def test_eq(self):
        
        ########## block_to_block_type TEST ##########
        
        # PARAGRAPHS
        paragraph_sample = "This is just plain text"
        self.assertEqual(block_to_block_type(paragraph_sample), BlockType.PARAGRAPH)

        not_heading_sample = "#This is not a header"
        self.assertEqual(block_to_block_type(not_heading_sample), BlockType.PARAGRAPH)

        not_code_sample = "``` This is not a code block ``"
        self.assertEqual(block_to_block_type(not_code_sample), BlockType.PARAGRAPH)

        not_quote_sample = "T>his is not a quote"
        self.assertEqual(block_to_block_type(not_quote_sample), BlockType.PARAGRAPH)

        not_unordered_list_sample = "-This is not an ordered list\n- all items in the list needs a space after the dash"
        self.assertEqual(block_to_block_type(not_unordered_list_sample), BlockType.PARAGRAPH)

        not_ordered_list_sample = "1. This is not\n2. An ordered\n33. List"
        self.assertEqual(block_to_block_type(not_code_sample), BlockType.PARAGRAPH) 

        # HEADER
        heading_sample = "# This is a header"
        self.assertEqual(block_to_block_type(heading_sample), BlockType.HEADING)

        heading2_sample = "## This also a header"
        self.assertEqual(block_to_block_type(heading2_sample), BlockType.HEADING)

        heading_extreme_sample = "########################## This is still a header"
        self.assertEqual(block_to_block_type(heading_extreme_sample), BlockType.HEADING)

        misplaced_symbol_heading_sample = "T# his is NOT a header"
        self.assertNotEqual(block_to_block_type(misplaced_symbol_heading_sample), BlockType.HEADING)

        # CODE
        code_sample = "```This is a code block```"
        self.assertEqual(block_to_block_type(code_sample), BlockType.CODE)

        code2_sample = "``` This is still a code block ```"
        self.assertEqual(block_to_block_type(code2_sample), BlockType.CODE)

        code3_sample = "```Also a code block ```"
        self.assertEqual(block_to_block_type(code3_sample), BlockType.CODE)

        code4_sample = "``` And this is still a code block```"
        self.assertEqual(block_to_block_type(code3_sample), BlockType.CODE)

        space_in_code_sample = "``` ```" # Still a code block
        self.assertEqual(block_to_block_type(code3_sample), BlockType.CODE)

        odd_format_code_sample = "``` ` ` ```" # This is still a code block
        self.assertEqual(block_to_block_type(odd_format_code_sample), BlockType.CODE)

        empty_code_sample = "``````" # NOT a code block
        self.assertNotEqual(block_to_block_type(empty_code_sample), BlockType.CODE)

        extra_symbol_in_code_sample = "````Also NOT a code block```"
        self.assertNotEqual(block_to_block_type(extra_symbol_in_code_sample), BlockType.CODE)

        extra_symbol2_in_code_sample = "```This is still NOT a code block````"
        self.assertNotEqual(block_to_block_type(extra_symbol2_in_code_sample), BlockType.CODE)

        # QUOTE
        quote_sample = ">This is a quote"
        self.assertEqual(block_to_block_type(quote_sample), BlockType.QUOTE)

        multiple_quotes_sample = ">This is a quote\n> This quote has a space after the symbol\n>And a third quote"
        self.assertEqual(block_to_block_type(multiple_quotes_sample), BlockType.QUOTE)

        extra_symbols_quote_sample = ">>This is still a quote>>"
        self.assertEqual(block_to_block_type(extra_symbols_quote_sample), BlockType.QUOTE)

        extra_whitespace_quote_sample = ">            This quote intentionally has a lot of whitespace, and it is still a quote"
        self.assertEqual(block_to_block_type(extra_whitespace_quote_sample), BlockType.QUOTE)

        mising_newline_quote_sample = ">This is a quote> and this is still part of the first quote"
        self.assertEqual(block_to_block_type(mising_newline_quote_sample), BlockType.QUOTE)

        misplaced_symbol_quote_sample = "This is NOT a quote>"
        self.assertNotEqual(block_to_block_type(misplaced_symbol_quote_sample), BlockType.QUOTE)

        misplaced_symbol2_quote_sample = "This is still >NOT a quote"
        self.assertNotEqual(block_to_block_type(misplaced_symbol2_quote_sample), BlockType.QUOTE)

        # UNORDERED LIST

        unordered_list_sample = "- this is one item\n- this is another\n- and a third item "
        self.assertEqual(block_to_block_type(unordered_list_sample), BlockType.UNORDERED_LIST)

        single_item_unordered_list_sample = "- this is one item in an unordered list"
        self.assertEqual(block_to_block_type(single_item_unordered_list_sample), BlockType.UNORDERED_LIST)

        single_item_whitespace_unordered_list_sample = "- " # This unordered list contains one item that has only whitespace in it
        self.assertEqual(block_to_block_type(single_item_whitespace_unordered_list_sample), BlockType.UNORDERED_LIST)

        whitespace_populated_unordered_list_sample = "- \n- \n- " # Still an unordered list, albeit looking empty
        self.assertEqual(block_to_block_type(whitespace_populated_unordered_list_sample), BlockType.UNORDERED_LIST)

        bad_format_unordered_list_sample = "-This is not a list\n-Because we are missing a space after the dash"
        self.assertNotEqual(block_to_block_type(bad_format_unordered_list_sample), BlockType.UNORDERED_LIST)

        bad_format2_unordered_list_sample = "- This is not a list\n-Because all items need a space after the dash"
        self.assertNotEqual(block_to_block_type(bad_format2_unordered_list_sample), BlockType.UNORDERED_LIST)

        # ORDERED LIST

        ordered_list_sample = "1. Item 1\n2. Item 2\n3. Item 3 "
        self.assertEqual(block_to_block_type(ordered_list_sample), BlockType.ORDERED_LIST)

        single_item_ordered_list_sample = "1. This is a single item in an ordered list"
        self.assertEqual(block_to_block_type(single_item_ordered_list_sample), BlockType.ORDERED_LIST)

        unpopulated_ordered_list_sample = "1.\n2.\n3." # This is still an ordered list, even if there is no characters present
        self.assertEqual(block_to_block_type(unpopulated_ordered_list_sample), BlockType.ORDERED_LIST)

        whitespace_populated_ordered_list_sample = "1. \n2. \n3. " # This ordered list is populated by a space
        self.assertEqual(block_to_block_type(whitespace_populated_ordered_list_sample), BlockType.ORDERED_LIST)

        bad_format_ordered_list_sample = "1 First Item\n 2 Second Item\n3 Third Item " # This ordered list is missing a dot after each number
        self.assertNotEqual(block_to_block_type(bad_format_ordered_list_sample), BlockType.ORDERED_LIST)

        bad_format2_ordered_list_sample = "1. First Item\n 2. Second Item\n3 Third Item " # All items on the list needs a dot after the number
        self.assertNotEqual(block_to_block_type(bad_format2_ordered_list_sample), BlockType.ORDERED_LIST)

        off_count_ordered_list_sample = "2. Second Item\n 3. Third Item\n4. Fourth Item " # The ordered list needs to start at 1.
        self.assertNotEqual(block_to_block_type(off_count_ordered_list_sample), BlockType.ORDERED_LIST)

        off_count2_ordered_list_sample = "1. First Item\n 22. Second Item\n3. Third Item " # Second item typo - should be 2. instead of 22.
        self.assertNotEqual(block_to_block_type(off_count2_ordered_list_sample), BlockType.ORDERED_LIST)