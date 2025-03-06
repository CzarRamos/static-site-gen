import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("A new text node!", TextType.BOLD)
        node4 = TextNode("A new text node!", TextType.BOLD, "https://github.com/CzarRamos")
        node5 = TextNode(None, None)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node, node5)


if __name__ == "__main__":
    unittest.main()
