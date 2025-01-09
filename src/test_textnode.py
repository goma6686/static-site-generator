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

if __name__ == "__main__":
    unittest.main()