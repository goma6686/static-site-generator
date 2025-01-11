import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_no_url_eq(self):
        node = TextNode("One", TextType.ITALIC, None)
        node2 = TextNode("One", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("One", TextType.BOLD, "ww")
        node2 = TextNode("Two", TextType.ITALIC, "ww")
        self.assertNotEqual(node, node2)

    def test_bad_data(self):
        self.assertRaises(TypeError, lambda: TextNode())

    def text_to_html_node(self):
        text_node = TextNode("Random Text", TextType.TEXT)
        bold_node = TextNode("Random Text", TextType.BOLD)
        italic_node = TextNode("Random Text", TextType.ITALIC)
        code_node = TextNode("Random Text", TextType.CODE)
        link_node = TextNode("Random Link Text", TextType.LINK, "https://www.google.com")
        image_node = TextNode("Random Alt Text", TextType.IMAGE, "https://some_image.jpg")

        self.assertEqual(repr(text_node), "HTMLNode(None, 'Random Text', None, {})")
        self.assertEqual(repr(bold_node), "HTMLNode('b', 'Random Text', None, {})")
        self.assertEqual(repr(italic_node), "HTMLNode('i', 'Random Text', None, {})")
        self.assertEqual(repr(code_node), "HTMLNode('code', 'Random Text', None, {})")
        self.assertEqual(repr(link_node), "HTMLNode('a', 'Random Link Text', None, {'href': 'https://www.google.com'})")
        self.assertEqual(repr(image_node), "HTMLNode('img', None, None, {'src': 'https://some_image.jpg', 'alt': 'Random Alt Text'})")

if __name__ == "__main__":
    unittest.main()