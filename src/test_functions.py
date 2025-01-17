import unittest

from functions import *
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

class TestTextToNode(unittest.TestCase):
    def test_text_to_node(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "text")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " with an ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, " word and a ")
        self.assertEqual(nodes[4].text_type, TextType.TEXT)
        self.assertEqual(nodes[5].text, "code block")
        self.assertEqual(nodes[5].text_type, TextType.CODE)
        self.assertEqual(nodes[6].text, " and an ")
        self.assertEqual(nodes[6].text_type, TextType.TEXT)
        self.assertEqual(nodes[7].text, "obi wan image")
        self.assertEqual(nodes[7].text_type, TextType.IMAGE)
        self.assertEqual(nodes[8].text, " and a ")
        self.assertEqual(nodes[8].text_type, TextType.TEXT)
        self.assertEqual(nodes[9].text, "link")
        self.assertEqual(nodes[9].text_type, TextType.LINK)

    def text_text_bold_to_node(self):
        text = "**just bold text**"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes[0].text, "just bold text")
        self.assertEqual(nodes[0].text_type, TextType.BOLD)

    def link_then_bold_to_node(self):
        text = "a [link](https://boot.dev) then some **bold** text"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes[0].text, "a ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "link")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[2].text, " then some ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text, "bold")
        self.assertEqual(nodes[3].text_type, TextType.BOLD)
        self.assertEqual(nodes[4].text, " text")
        self.assertEqual(nodes[4].text_type, TextType.TEXT)

    def image_with_bold_alt(self):
        text = "an image with ![**bold**](https://i.imgur.com/fJRm4Vk.jpeg) alt text"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes[0].text, "an image with ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(nodes[2].text, " alt text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
