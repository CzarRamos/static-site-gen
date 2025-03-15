from htmlnode import HTMLNode

class ImageLeafNode(HTMLNode):
    def __init__(self, tag, props=None):
        super().__init__(tag, None, None, props)

    def to_html(self):
        if self.tag == None or self.tag == "":
            return self.value
        if self.props == None:
            return f"<{self.tag} {self.value}>"
        return f"<{self.tag}{self.props_to_html()} />"