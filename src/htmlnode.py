class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props == None:
            return ""
        html_string = ""
        for prop in self.props:
            key = f" {prop}="
            value = f'"{self.props[prop]}"'
            string = key + value
            html_string += string
        return html_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children:{self.children}, {self.props_to_html()})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Invalid HTML: value must be provided")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Invalid HTML: tag must be provided")
        if self.children == None:
            raise ValueError("Invalid HTML: children must be provided")
        returnable = f"<{self.tag}>"
        for child in self.children:
            returnable += child.to_html()
        returnable += f"</{self.tag}>"

        return returnable