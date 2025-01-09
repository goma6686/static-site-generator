from functools import reduce

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        #A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.tag = tag
        #A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.value = value
        #A list of HTMLNode objects representing the children of this node
        self.children = children
        #A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        return " ".join(f" {key}={value}" for key, value in self.props.items())
    
    def __repr__(self):
        return f"HTMLNode({self.tag, self.value, self.children, self.props})"
    
class LeafNode(HTMLNode):
    #does not allow children
    def __init__(self, tag, value, props={}):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("value is required for a leaf node")
        
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props={}):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is required for a parent node")
        
        if self.children is None:
            raise ValueError("children are required for ParentNode")
        
        return f"<{self.tag}>{reduce(lambda x, y: x + y.to_html(), self.children, "")}</{self.tag}>"