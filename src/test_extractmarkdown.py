import unittest
from textnode import TextNode, TextType
from extractmarkdown import *

class TextExtractMarkdown(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        #node = markdown_to_html_node(md)
        # html = node.to_html()
        # self.assertEqual(
        #     html,
        #     "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        # )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        #node = markdown_to_html_node(md)
        # html = node.to_html()
        # self.assertEqual(
        #     html,
        #     "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        # )


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

        ########## text_to_textnodes TEST ##########
        sample = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        sample_nodes = text_to_textnodes(sample)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            sample_nodes
        )

        ########## markdown_to_blocks TEST ##########

        markdown_sample = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        markdown_sample_blocks = markdown_to_blocks(markdown_sample)
        self.assertEqual(
        markdown_sample_blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )

        full_markdown_sample = """# Heading 1

## Heading 2

### Heading 3

This is a paragraph with **bold text**, _italic text_, and ```inline code```. The paragraph continues with more text to make it longer and more representative of real-world content. Here's a [link to Boot.dev](https://boot.dev) that you might need to parse. When parsing paragraphs, you'll need to handle multiple sentences and maintain the formatting correctly throughout the entire block of text, which can sometimes be challenging.

Another paragraph with _more italic_ and **bold stuff** to parse. This additional text makes the paragraph longer and gives you more content to work with. Here's another [example link](https://example.com) in the middle of text. Testing with longer paragraphs helps ensure your parser can handle real-world scenarios where users might write extensive content with various inline formatting elements scattered throughout their text.

![Sample image description](https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png)

> This is a block quote with a [link](https://example.com)
> that continues on a second line
> and even adds a third line to make it longer

- Unordered list item 1 with some extra text to make it longer
- Unordered list item 2 with a [link to documentation](https://example.com)
- Unordered list item with **bold** and _italic_ formatting mixed into a longer sentence

1. Ordered list item 1 with extended text to test longer content
2. Ordered list item 2 with more words and a ![tiny image](https://github.com/favicon.ico) inline
3. Ordered list item with ```code``` and _italic_ formatting embedded in a much longer line of text

```
This is a code block
It preserves **formatting** and _doesn't_ parse markdown
It can have multiple lines
And can be quite lengthy with lots of content
That should all be preserved exactly as written
Including [links](https://example.com) that should NOT be parsed
```

#### Heading 4 **This is bolded text** _italics here_ and ```apparently code as well```

Paragraph after code block with simple text. This final paragraph gives you one more block to test your parser with. It ensures that your code correctly handles content that comes after special blocks like code blocks, and provides a good closing test case for your markdown to HTML converter."""
            
        html_nodes = markdown_to_html_node(full_markdown_sample)
        self.assertEqual("""<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><p>This is a paragraph with <b>bold text</b>, <i>italic text</i>, and <pre><code>inline code</code></pre>. The paragraph continues with more text to make it longer and more representative of real-world content. Here's a <a href="https://boot.dev">link to Boot.dev</a> that you might need to parse. When parsing paragraphs, you'll need to handle multiple sentences and maintain the formatting correctly throughout the entire block of text, which can sometimes be challenging.</p><p>Another paragraph with <i>more italic</i> and <b>bold stuff</b> to parse. This additional text makes the paragraph longer and gives you more content to work with. Here's another <a href="https://example.com">example link</a> in the middle of text. Testing with longer paragraphs helps ensure your parser can handle real-world scenarios where users might write extensive content with various inline formatting elements scattered throughout their text.</p><p><img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="Sample image description" /></p><blockquote>This is a block quote with a <a href="https://example.com">link</a> that continues on a second line and even adds a third line to make it longer</blockquote><ul><li>Unordered list item 1 with some extra text to make it longer</li><li>Unordered list item 2 with a <a href="https://example.com">link to documentation</a></li><li>Unordered list item with <b>bold</b> and <i>italic</i> formatting mixed into a longer sentence</li></ul><ol><li>Ordered list item 1 with extended text to test longer content</li><li>Ordered list item 2 with more words and a <img src="https://github.com/favicon.ico" alt="tiny image" /> inline</li><li>Ordered list item with <pre><code>code</code></pre> and <i>italic</i> formatting embedded in a much longer line of text</li></ol><pre><code>This is a code block
It preserves **formatting** and _doesn't_ parse markdown
It can have multiple lines
And can be quite lengthy with lots of content
That should all be preserved exactly as written
Including [links](https://example.com) that should NOT be parsed</code></pre><h4>Heading 4 <b>This is bolded text</b> <i>italics here</i> and <pre><code>apparently code as well</code></pre></h4><p>Paragraph after code block with simple text. This final paragraph gives you one more block to test your parser with. It ensures that your code correctly handles content that comes after special blocks like code blocks, and provides a good closing test case for your markdown to HTML converter.</p></div>""",
html_nodes.to_html())



        md_test = """# Heading 1

## Heading 2

### Heading 3

This is a paragraph with **bold text**, _italic text_, `inline code`, and [a link](https://boot.dev).

- Unordered list item 1
- Unordered list item 2 with **bold**
- Unordered list item 3

1. Ordered list item 1
2. Ordered list item 2 with _italic_
3. Ordered list item 3

> This is a blockquote with some ```code``` inside.

```
This is a code block
It should **not** parse markdown
It should preserve
    indentation and
line breaks
```"""

        md_to_html_nodes = markdown_to_html_node(md_test)
        self.assertEqual("""<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><p>This is a paragraph with <b>bold text</b>, <i>italic text</i>, <pre><code>inline code</code></pre>, and <a href="https://boot.dev">a link</a>.</p><ul><li>Unordered list item 1</li><li>Unordered list item 2 with <b>bold</b></li><li>Unordered list item 3</li></ul><ol><li>Ordered list item 1</li><li>Ordered list item 2 with <i>italic</i></li><li>Ordered list item 3</li></ol><blockquote>This is a blockquote with some <pre><code>code</code></pre> inside.</blockquote><pre><code>This is a code block
It should **not** parse markdown
It should preserve
    indentation and
line breaks</code></pre></div>""", md_to_html_nodes.to_html())

