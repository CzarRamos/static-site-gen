import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        htmlnode = HTMLNode("tag1", "test value")
        htmlnode2 = HTMLNode("tag1", "test value")
        htmlnode3 = HTMLNode(props={ "href": "https://github.com/CzarRamos", "target": "_blank"})
        htmlnode4 = HTMLNode()
        htmlnode5 = HTMLNode(children=htmlnode4)
        self.assertEqual(htmlnode, htmlnode2)
        self.assertNotEqual(htmlnode, htmlnode3)
        self.assertNotEqual(htmlnode, htmlnode4)
        self.assertNotEqual(htmlnode, htmlnode5)
        print(htmlnode3.props_to_html())


if __name__ == "__main__":
    unittest.main()
