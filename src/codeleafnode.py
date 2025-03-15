from htmlnode import HTMLNode

class CodeLeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None or self.value == "":
            raise ValueError("All leaf nodes must have a value!")
        if self.tag == None or self.tag == "":
            return self.value
        if self.props == None:
            return f"<pre><{self.tag}>{self.value}</{self.tag}></pre>"
        return f"<pre><{self.tag}{self.props_to_html()}>{self.value}</{self.tag}></pre>"