from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(node)
    a = HTMLNode("<b>", "random sentence", ["a"], {"href": "https://www.google.com", "a": "asdad"})
    print(a)
    b = LeafNode("p", "This is a paragraph of text.")
    c = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    print(b.to_html())
    print(c.to_html())
    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )
    print(node.to_html())

main()