import unittest

from delimiter import split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_image
from textnode import TextNode, TextType

class TestDelimiter(unittest.TestCase):
    def test_one_delimiter(self):
        node = TextNode("Text with `code` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " here")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_multiple_delimiters(self):
        node = TextNode("Text with `code` and `more code` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "more code")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
        self.assertEqual(new_nodes[4].text, " here")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)

    def test_starts_with_delimiter(self):
        node = TextNode("`code` at start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "code")
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, " at start")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)

    def test_ends_with_delimiter(self):
        node = TextNode("end with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "end with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)

    def test_empty_delimiter(self):
        node = TextNode("Text with ``empty`` delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "empty")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, " delimiters")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_unmatched_delimiter(self):
        node = TextNode("Unmatched `delimiter here", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "`", TextType.CODE)

    def test_bold_delimiter(self):
        node = TextNode("Text with **bold** here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " here")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_even_unmatched_delimiter(self):
        node = TextNode("Text with `uneven* delimiters", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "*", TextType.CODE)

class TestMarkdownRegex(unittest.TestCase):
    def test_image_markdown(self):
        text = "[This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_link_markdown(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_no_image_markdown(self):
        text = "random text"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_bracket_markdown(self):
        text = "[This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])


class TestSplitNodesImage(unittest.TestCase):
    def test_no_image(self):
        old_nodes = [TextNode("random text", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "random text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_one_image(self):
        old_nodes = [TextNode("This is text with a link ![to boot dev]( https://www.boot.dev) here", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a link ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "to boot dev")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[2].text, " here")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_multiple_images(self):
        old_nodes = [TextNode("This is text with a link ![to boot dev]( https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev) here", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This is text with a link ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "to boot dev")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "to youtube")
        self.assertEqual(new_nodes[3].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[4].text, " here")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)