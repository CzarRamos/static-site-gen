import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def text_node_to_html_node(self, text_node):
        match (text_node.text_type):
            case TextType.TEXT:
                return LeafNode(None, text_node.text)
            case TextType.BOLD:
                return LeafNode("b", text_node.text)
            case TextType.ITALIC:
                return LeafNode("i", text_node.text)
            case TextType.CODE:
                return LeafNode("code", text_node.text)
            case TextType.LINK:
                return LeafNode("a", text_node.text, props={"href": text_node.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src":text_node.url, "alt": text_node.text})
            case _:
                raise Exception("Not a valid text type")
    
    def test_text(self):
        test_node = TextNode("This is a text node", TextType.TEXT)
        html_node = self.text_node_to_html_node(test_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
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
        self.test_text()



if __name__ == "__main__":
    unittest.main()
