

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other_htmlnode):
        return self.tag == other_htmlnode.tag and self.value == other_htmlnode.value and self.children == other_htmlnode.children and self.props == other_htmlnode.props

    def props_to_html(self):
        output = ""
        if self.props != None:
            for item in self.props:
                prop = self.props[item]
                if prop != None:
                    output += f" {item}=\"{self.props[item]}\""
        return output

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"