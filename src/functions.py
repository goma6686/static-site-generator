from textnode import TextNode, TextType
import re

#returns a new list of nodes, where any "text" type nodes in the input list as (potentially) split into multiple nodes based on syntax
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type is TextType.TEXT:
            #check if text node contains delimiter
            if delimiter not in node.text:
                new_list.append(node)
                continue
            #check if there is even number of delimiters
            if node.text.count(delimiter) % 2 != 0:
                raise Exception(f"Delimiter {delimiter} is not even, cannot split text node")
            
            text_chunks = node.text.split(delimiter)
            
            #add text chunks to new list
            for i in range(0, len(text_chunks)):
                #even chunks are text
                if i % 2 == 0:
                    if text_chunks[i] != "":
                        new_list.append(TextNode(text_chunks[i], node.text_type, node.url))
                #odd chunks are text between delimiters
                else:
                    if text_chunks[i] != "":
                        new_list.append(TextNode(text_chunks[i], text_type, node.url))
                    

        else:
            new_list.append(node)
    return new_list

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_list = []

    for node in old_nodes:

        #get all links in tuples
        links = extract_markdown_images(node.text)
        #if there are no links
        if not links:
            #if there is text
            if node.text:
                #add text node
                new_list.append(TextNode(node.text, node.text_type, node.url))
            continue
        
        #get text
        text = node.text
        #if there are links loop through
        for link_text, link in links:
            #find link
            try:
                escaped_link_text = re.escape(link_text)
                escaped_link = re.escape(link)
                match = re.search(rf"!\[({escaped_link_text})]\({escaped_link}\)", text)
                #get start and end
                start = match.start()
                end = match.end()
            except re.error:
                raise AttributeError(f"Invalid link: {link}")
            

            #if there is text before link
            if start > 0:
                #add text node
                new_list.append(TextNode(text[:start], node.text_type, node.url))
            #check if link_text is in markdown too
            node = TextNode(link_text, TextType.TEXT)
            nodes = [node]
            nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
            nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
            nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
            if len(nodes) > 0:
                link_text = nodes[0].text
            #add link node
            new_list.append(TextNode(link_text, TextType.IMAGE, link))
            #remove text
            text = text[end:]
        #if there is text after last link
        if text:
            #add text node
            new_list.append(TextNode(text, node.text_type, node.url))

    return new_list

def split_nodes_link(old_nodes):
    new_list = []

    for node in old_nodes:

        #get all links in tuples
        links = extract_markdown_links(node.text)
        #if there are no links
        if not links:
            #if there is text
            if node.text:
                #add text node
                new_list.append(TextNode(node.text, node.text_type, node.url))
            continue
        
        #get text
        text = node.text
        #if there are links loop through
        for link_text, link in links:
            #find link
            try:
                escaped_link_text = re.escape(link_text)
                escaped_link = re.escape(link)
                match = re.search(rf"\[({escaped_link_text})]\({escaped_link}\)", text)
                #get start and end
                start = match.start()
                end = match.end()
            except re.error:
                raise AttributeError(f"Invalid link: {link}")
            

            #if there is text before link
            if start > 0:
                #add text node
                new_list.append(TextNode(text[:start], node.text_type, node.url))
            
            #check if link_text is in markdown too
            node = TextNode(link_text, TextType.TEXT)
            nodes = [node]
            nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
            nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
            nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
            if len(nodes) > 0:
                link_text = nodes[0].text
            #add link node
            new_list.append(TextNode(link_text, TextType.LINK, link))
            #remove text
            text = text[end:]
        #if there is text after last link
        if text:
            #add text node
            new_list.append(TextNode(text, node.text_type, node.url))

    return new_list


def text_to_textnodes(text):
    #first node is text
    node = TextNode(text, TextType.TEXT)
    #start with a list containing the text node
    nodes = [node]
    #apply each split function to all nodes in the list
    nodes = split_nodes_image(nodes)
    print("After image split:", nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)

    return nodes

