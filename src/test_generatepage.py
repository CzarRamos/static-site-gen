import unittest
from generatepage import *

class TestGeneratePage(unittest.TestCase):
    def test_eq(self):

        ########## extract_title TEST ##########
        EXPECTED_EXCEPTIONS_COUNT = 2
        current_exceptions_occurred = 0

        # Normal header in markdown
        title_normal_header = """# Title of my page here!
        ## While this is a header 2
        And this is a paragraph
        """
        self.assertEqual("Title of my page here!", extract_title(title_normal_header))

        # Header 1 with an intentional # in its text
        title_extra_symbol_in_header = """# #Title of my page here!
        ## While this is a header 2
        And this is a paragraph
        """
        self.assertEqual("#Title of my page here!", extract_title(title_extra_symbol_in_header))

        # Misplaced header 1 in markdown
        title_misplaced_header = """## This is header 2
        # Title of my page here
        And this is a paragraph
        """
        try:
            self.assertEqual("Title of my page here", extract_title(title_misplaced_header))
        except Exception as e:
            print(f"Misplaced Header sample exception: {e}")
            current_exceptions_occurred += 1

        # Missing header in markdown
        title_missing_header = """## There is no header
        And this is a paragraph
        """
        try:
            self.assertEqual("There is no header", extract_title(title_missing_header))
        except Exception as e:
            print(f"Missing Header sample exception: {e}")
            current_exceptions_occurred +=1

        self.assertEqual(expected_exceptions_count, current_exceptions_occurred)