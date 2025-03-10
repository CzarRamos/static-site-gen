import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        leafnode = LeafNode("p", "This is a paragraph of text.")
        leafnode2 = LeafNode("p", "This is a paragraph of text.")
        leafnode3 = LeafNode("a", "My github page!", { "href": "https://github.com/CzarRamos", "target": "_blank"})
        leafnode4 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        leafnode5 = LeafNode(None, "this should be plain text", {})
        leafnode6 = LeafNode("h1", "Header test")
        self.assertEqual(leafnode, leafnode2)
        self.assertNotEqual(leafnode, leafnode3)
        self.assertNotEqual(leafnode, leafnode4)
        self.assertNotEqual(leafnode, leafnode5)


if __name__ == "__main__":
    unittest.main()
