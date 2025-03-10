import unittest
from textnode import TextNode, TextType
from extractmarkdown import *

class TextExtractMarkdown(unittest.TestCase):

    def test_eq(self):

        ########## extract_markdown_images TEST ##########

        # empty alt text and image
        plain_text = extract_markdown_images("This is just text")
        self.assertListEqual([], plain_text)

        # empty alt text and image
        empty_text_empty_image = extract_markdown_images("This is text with an ![]() ")
        self.assertListEqual([("", "")], empty_text_empty_image)

        # empty alt text containing an image
        empty_text_with_image = extract_markdown_images("This is text with an ![](https://fakeimage.com/example.png) ")
        self.assertListEqual([("", "https://fakeimage.com/example.png")], empty_text_with_image)

        # empty image containing alt text
        missing_image_with_text = extract_markdown_images("This is text with an ![image]() ")
        self.assertListEqual([("image", "")], missing_image_with_text)

        # single image in text
        single_image = extract_markdown_images("This is text with an ![image](https://fakeimage.com/example.png) ")
        self.assertListEqual([("image", "https://fakeimage.com/example.png")], single_image)

        # multiple images in text
        multiple_images = extract_markdown_images("This is text with an ![image](https://fakeimage.com/example.png) and a ![second image](https://fakeimage.com/anotherexample.png)")
        self.assertListEqual([("image", "https://fakeimage.com/example.png"), ("second image", "https://fakeimage.com/anotherexample.png")], multiple_images)

        ########## extract_markdown_links TEST ##########

        # empty alt text and image
        only_text = extract_markdown_links("This is only text, no links here.")
        self.assertListEqual([], only_text)

        # empty alt text and link
        empty_text_empty_link = extract_markdown_links("This is text with an []() ")
        self.assertListEqual([("", "")], empty_text_empty_link)

        # empty alt text containing a link
        empty_text_with_link = extract_markdown_links("This is text with an [](https://fakelink.com) ")
        self.assertListEqual([("", "https://fakelink.com")], empty_text_with_link)

        # empty image containing alt text
        missing_link_with_text = extract_markdown_links("This is text with an [example link]() ")
        self.assertListEqual([("example link", "")], missing_link_with_text)

        # single link
        single_link = extract_markdown_links("This is text with an [example link](https://fakelink.com)")
        self.assertListEqual([("example link", "https://fakelink.com")], single_link)

        # multiple links
        multiple_links = extract_markdown_links("This is text with an [example link](https://fakelink.com) and [another link](https://anotherfakelink.com)")
        self.assertListEqual([("example link", "https://fakelink.com"), ("another link", "https://anotherfakelink.com")], multiple_links)
        
        ########## split_nodes_image TEST ##########

        # empty text in node
        empty_node = TextNode("", TextType.TEXT)
        empty_node_split = split_nodes_image([empty_node])
        self.assertListEqual([], empty_node_split)

        # no images, only plain text
        generic_text_node = TextNode("No images, only text here.", TextType.TEXT)
        generic_text_node_image = split_nodes_image([generic_text_node])
        self.assertListEqual(
            [
                TextNode("No images, only text here.", TextType.TEXT),
            ],
            generic_text_node_image,
        )

        # node only containing an image
        image_only_node = TextNode("![image](https://fakeimage.com/example.png)", TextType.TEXT)
        image_only_node_split = split_nodes_image([image_only_node])
        self.assertListEqual([TextNode("image", TextType.IMAGE, "https://fakeimage.com/example.png")], image_only_node_split)

        # node only containing an image
        image_node = TextNode("This is text with an ![image](https://fakeimage.com/example.png)", TextType.TEXT)
        image_node_split = split_nodes_image([image_node])
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT), TextNode("image", TextType.IMAGE, "https://fakeimage.com/example.png")], image_node_split)

        # multiple images in text
        multiple_images_node = TextNode(
        "This is text with an ![image](https://fakeimage.com/example.png) and another ![second image](https://fakeimage.com/anotherexample.png)",
        TextType.TEXT
        )
        multiple_images_node_split = split_nodes_image([multiple_images_node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://fakeimage.com/example.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://fakeimage.com/anotherexample.png"
                ),
            ],
            multiple_images_node_split
        )

        # using multiple kinds of nodes as input
        all_node_examples = [empty_node, generic_text_node, image_only_node, image_node, multiple_images_node]
        all_node_examples_split = split_nodes_image(all_node_examples)
        self.assertListEqual(
            [
                TextNode("No images, only text here.", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://fakeimage.com/example.png"),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://fakeimage.com/example.png"),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://fakeimage.com/example.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://fakeimage.com/anotherexample.png"
                ),
            ],
            all_node_examples_split
        )

        ########## split_nodes_link TEST ##########

        # empty text in node
        empty_link_node = TextNode("", TextType.TEXT)
        empty_link_node_split = split_nodes_image([empty_link_node])
        self.assertListEqual([], empty_link_node_split)

        # no links, only plain text
        only_text_node = TextNode("No links, only text here.", TextType.TEXT)
        only_text_node_split = split_nodes_link([only_text_node])
        self.assertListEqual(
            [
                TextNode("No links, only text here.", TextType.TEXT),
            ],
            only_text_node_split
        )

        # a single link in text
        only_link_node = TextNode("This is text with a [link](https://fakelink.com)", TextType.TEXT)
        only_link_node_split = split_nodes_link([only_link_node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://fakelink.com")
            ],
            only_link_node_split
        )

        # a single link in text
        link_node = TextNode("This is text with a [link](https://fakelink.com)", TextType.TEXT)
        link_node_split = split_nodes_link([link_node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://fakelink.com")
            ],
            link_node_split
        )

        # multiple links in text
        multiple_links_node = TextNode(
        "This is text with a [link](https://fakelink.com) and another [second link](https://anotherfakelink.com)",
        TextType.TEXT,
        )
        multiple_links_node_split = split_nodes_link([multiple_links_node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://fakelink.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://anotherfakelink.com"
                ),
            ],
            multiple_links_node_split
        )




        



