from textnode import TextNode, TextType
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