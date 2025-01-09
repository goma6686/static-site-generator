import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_initialization(self):
        node = HTMLNode(tag="a", value="Click here", children=None, props={"href": "https://www.google.com"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Click here")
        self.assertEqual(node.props, {"href": "https://www.google.com"})

    def test_props_to_html_single_attribute(self):
        node = HTMLNode(tag="a", props={"href": "https://www.google.com"})
        result = node.props_to_html()
        self.assertEqual(result, ' href=https://www.google.com')

    def test_props_to_html_multiple_attributes(self):
        node = HTMLNode(tag="a", props={"href": "https://www.google.com", "target": "_blank"})
        result = node.props_to_html()
        self.assertEqual(result, ' href=https://www.google.com  target=_blank')

    def test_props_to_html_no_attributes(self):
        node = HTMLNode(tag="div", props={})
        result = node.props_to_html()
        self.assertEqual(result, '')

    def test_repr(self):
        node = HTMLNode(tag="p", value="Hello", children=[], props={"class": "text"})
        result = repr(node)
        self.assertEqual(result, "HTMLNode(('p', 'Hello', [], {'class': 'text'}))")

class TestLeafNode(unittest.TestCase):
    def test_initialization(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Click me!")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"href": "https://www.google.com"})

    def test_with_children(self):
        with self.assertRaises(TypeError):
            LeafNode("p", "Hello", ["A"], {"class": "text"})

    def test_with_no_props(self):
        node = LeafNode("a", "Click me!")
        self.assertEqual(node.props, {})

    def test_no_value_to_html(self):
        with self.assertRaises(ValueError):
            LeafNode("a", None, {"href": "https://www.google.com"}).to_html()

    def test_no_tag_to_html(self):
        node = LeafNode(None, "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "Click me!")

class TestParentNode(unittest.TestCase):
    def test_initialization(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        result = node.to_html()
        self.assertEqual(result, "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_nested_nodes(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "b",
                    [
                        LeafNode("b", "second bold text"),
                        LeafNode(None, "second normal text"),
                        LeafNode("i", "second italic text")
                    ],
                ),
                LeafNode(None, "first normal text"),
                LeafNode("i", "first italic text"),
                LeafNode(None, "first Normal text"),
            ]
        )
        result = node.to_html()
        self.assertEqual(result, "<p><b><b>second bold text</b>second normal text<i>second italic text</i></b>first normal text<i>first italic text</i>first Normal text</p>")

    def test_multiple_children(self):
        node = ParentNode(
            "i",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
            ]
        )
        result = node.to_html()
        self.assertEqual(result, "<i><b>Bold text</b>Normal text<i>italic text</i></i>")

    def test_no_children(self):
        node = ParentNode(
            "p",
            [],
        )
        result = node.to_html()
        self.assertEqual(result, "<p></p>")

    def test_no_children_2(self):
        with self.assertRaises(ValueError):
            ParentNode("p", None).to_html()

    def test_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, []).to_html()

    def test_no_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b></p>",
        )
        
if __name__ == "__main__":
    unittest.main()