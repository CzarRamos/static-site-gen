from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tags, children, props=None):
        super().__init__(tags, None, children, props)
        self.tags = tags
        self.children = children
        self.props = props
    
    def to_html(self):
        output = ""
        if self.tags == None:
            raise ValueError("ParentNode is missing a tag")
        if self.children == None:
            raise ValueError("ParentNode is missing children")
        for child in self.children:
            if isinstance(child, ParentNode):
                output += child.to_html()
            else:
                output += child.to_html()
        
        return f"<{self.tags}{self.props_to_html()}>{output}</{self.tags}>"       

