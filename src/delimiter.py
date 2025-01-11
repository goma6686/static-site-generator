from textnode import TextNode, TextType

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