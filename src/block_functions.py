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