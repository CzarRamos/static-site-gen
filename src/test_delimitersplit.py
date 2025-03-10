import unittest
from textnode import TextNode, TextType
from nodedelimiter import split_nodes_delimiter

class TestdelimiterSplit(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is a regular text node", TextType.TEXT)                           # all regular text
        node2 = TextNode("This is **a wonderful** text node", TextType.TEXT)                    # contains one bolded phrase
        node3 = TextNode("**BOLD TEXT NODE****here!!**", TextType.TEXT)                         # two bolded and squished together phrases
        node4 = TextNode("A new _text_ node!", TextType.TEXT)                                   # contains one italicized word
        node5 = TextNode("_italicized node_", TextType.ITALIC)                                  # already italicized text - should return as-is despite having delimiter present
        node6 = TextNode("this tag has `code` in it", TextType.TEXT)                            # contains one coded word
        node7 = TextNode("This **has** _multiple tags_", TextType.TEXT)                         # multiple tags, only testing for bolded words
        node8 = TextNode("_incomplete tag!! ", TextType.TEXT)                                   # incomplete tag - should throw an exception

        self.assertEqual(split_nodes_delimiter([node], "``", TextType.CODE),    [TextNode("This is a regular text node", TextType.TEXT)])
        self.assertEqual(split_nodes_delimiter([node2], "**", TextType.BOLD),   [TextNode("This is ", TextType.TEXT), TextNode("a wonderful", TextType.BOLD), TextNode(" text node", TextType.TEXT)])
        self.assertEqual(split_nodes_delimiter([node3], "**", TextType.BOLD),   [TextNode("BOLD TEXT NODE", TextType.BOLD), TextNode("here!!", TextType.BOLD)])
        self.assertEqual(split_nodes_delimiter([node4], "_", TextType.ITALIC),  [TextNode("A new ", TextType.TEXT), TextNode("text", TextType.ITALIC), TextNode(" node!", TextType.TEXT)])
        self.assertEqual(split_nodes_delimiter([node5], "_", TextType.ITALIC),  [TextNode("_italicized node_", TextType.ITALIC)])
        self.assertEqual(split_nodes_delimiter([node6], "`", TextType.CODE),    [TextNode("this tag has ", TextType.TEXT), TextNode("code", TextType.CODE), TextNode(" in it", TextType.TEXT)])
        self.assertEqual(split_nodes_delimiter([node7], "**", TextType.BOLD),   [TextNode("This ", TextType.TEXT), TextNode("has", TextType.BOLD), TextNode(" _multiple tags_", TextType.TEXT)])
        
        # Empty list input should output empty list as well:
        self.assertEqual(split_nodes_delimiter([], "**", TextType.BOLD),        [])

        try:
            # Exception thrown here due to missing tag  
            self.assertEqual(split_nodes_delimiter([node8], "_", TextType.ITALIC), [TextNode("incomplete tag!! ", TextType.TEXT)])
        except Exception as e:
            print(e)


if __name__ == "__main__":
    unittest.main()
