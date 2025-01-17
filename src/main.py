from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from functions import text_to_textnodes

def main():
    text = "an image with ![**bold**](https://i.imgur.com/fJRm4Vk.jpeg) alt text"
    nodes = text_to_textnodes(text)
    print(f"final nodes: {nodes}")

main()