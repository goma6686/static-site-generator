from htmlnode import LeafNode, ParentNode
from inline_functions import text_to_textnodes
from textnode import TextType
import re

def markdown_to_blocks(markdown):
    #get blocks
    blocks = markdown.split("\n\n")

    #strip any leading or trailing whitespace from each block
    for i in range(0, len(blocks)):
        blocks[i] = blocks[i].strip()

    #make 'some text  \n  with spaces' => 'some text\nwith spaces'
    blocks = [re.sub(r'\s*\n\s*', '\n', node).strip() for node in blocks]
    #remove empty leftover strings 
    blocks = [x for x in blocks if x.strip()]
        
    return blocks

def block_to_block_type(markdown_block):
    #Headings start with 1-6 # characters, followed by a space and then the heading text.
    if markdown_block.startswith("###### ") or \
       markdown_block.startswith("##### ") or \
       markdown_block.startswith("#### ") or \
       markdown_block.startswith("### ") or \
       markdown_block.startswith("## ") or \
       markdown_block.startswith("# "):
        return "heading"
    
    #Code blocks must start with 3 backticks and end with 3 backticks.
    if markdown_block[0:3] == "```" and markdown_block[-3:len(markdown_block)] == "```":
        return "code"
    
    blocks = markdown_block.split("\n")

    #Every line in a quote block must start with a > character.
    if blocks[0].startswith(">"):
        for block in blocks:
            if not block.startswith(">"):
                raise ValueError("Invalid blockquote")
        return "quote"
        
    #Every line in an unordered list block must start with a * or - character, followed by a space.
    if blocks[0].startswith("* ") or blocks[0].startswith("- "):
        for block in blocks:
            if not (block.startswith("* ") or block.startswith("- ")):
                raise ValueError("Invalid unordered list")
        return "unordered_list"
    
    #Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
    if blocks[0][0:3] == "1. ":
        for i in range(1, len(blocks)):
            if not blocks[i].startswith(f"{str(i+1)}. "):
                raise ValueError("Invalid ordered list")
        return "ordered_list"
        
    #If none of the above conditions are met, the block is a normal paragraph.
    return "paragraph"

    #converts a full markdown document into a single parent HTMLNode
def markdown_to_html(markdown):
    #create the parent HTMLNode
    main = ParentNode(tag="div", children=[])
    #split markdown into blocks
    blocks = markdown_to_blocks(markdown)
    #convert each block into an HTMLNode
    for i in range(0, len(blocks)):
        #based on type, create a new HTMLNode with the correct data
        block_node = get_block_node(blocks[i])
        #append the parent HTMLNode to the main HTMLNode
        main.children.append(block_node)
        
    return main

def get_block_node(block):
    """Converts a single markdown block into an HTMLNode object"""
    block_type = block_to_block_type(block)
    match block_type:
        case "heading":
            return get_heading_node(block)
        case "code":
            return get_code_node(block)
        case "quote":
            return get_quote_node(block)
        case "unordered_list":
            return get_unordered_list_node(block)
        case "ordered_list":
            return get_ordered_list_node(block)
        case "paragraph":
            return get_paragraph_node(block)

def get_heading_node(block):
    #get the level of the heading
    level = block.count("#")
    #get the text of the heading
    heading_text = block[level+1:]
    #create the HTMLNode
    heading_node = LeafNode(tag=f"h{level}", value=heading_text)
    
    return heading_node

def get_code_node(block):
    #get the code text
    code_text = block.split("```")[1].split("```")[0]

    if code_text.startswith("\n"):
        code_text = code_text[1:]
    #create the HTMLNode
    code_node = ParentNode(tag="pre", children=[LeafNode(tag="code", value=code_text)])
    
    return code_node

def get_quote_node(block):
    #get the children
    quotes = block.split("\n")
    #create the HTMLNode
    quote_node = ParentNode(tag="blockquote", children=[])
    for quote in quotes:
        if not quote.startswith(">"):
            raise ValueError("Invalid blockquote")
        #strip any leading or trailing whitespace from each quote
        quote = quote[1:].strip()
        quote_node.children.append(LeafNode(tag=None, value=text_to_children(quote)))
    return quote_node

def get_unordered_list_node(block):
    #get the children
    children = block.split("\n")
    #strip any leading or trailing whitespace from each child
    children = [child.lstrip() for child in children]
    #create the HTMLNode
    unordered_list_node = ParentNode(tag="ul", children=[LeafNode(tag="li", value=text_to_children(child[2:len(child)])) for child in children])
    
    return unordered_list_node

def get_ordered_list_node(block):
    #get the children
    children = block.split("\n")
    #strip any leading or trailing whitespace from each child
    children = [child.lstrip() for child in children]
    #create the HTMLNode
    ordered_list_node = ParentNode(tag="ol", children=[LeafNode(tag="li", value=text_to_children(child[3:len(child)])) for child in children])
    return ordered_list_node

def get_paragraph_node(block):
    #create the HTMLNode
    paragraph_node = LeafNode(tag="p", value=text_to_children(block))
    return paragraph_node

def text_to_children(text):
    children = []
    #split text into text nodes
    text_nodes = text_to_textnodes(text)
    #convert each text node into an HTMLNode
    for text_node in text_nodes:
        if text_node.text_type == TextType.IMAGE:
            children.append(LeafNode(tag="img", value=None, props={"src": text_node.url, "alt": text_node.text}).to_html())
        if text_node.text_type == TextType.LINK:
            children.append(LeafNode(tag="a", value=text_node.text, props={"href": text_node.url}).to_html())
        if text_node.text_type == TextType.ITALIC:
            children.append(LeafNode(tag="i", value=text_node.text).to_html())
        if text_node.text_type == TextType.BOLD:
            children.append(LeafNode(tag="b", value=text_node.text).to_html())
        if text_node.text_type == TextType.CODE:
            children.append(LeafNode(tag="code", value=text_node.text).to_html())
        if text_node.text_type == TextType.TEXT:
            children.append(LeafNode(tag=None, value=text_node.text).to_html())
    
    return ''.join(children)
