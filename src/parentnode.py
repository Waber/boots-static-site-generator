from src.htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: str, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        if self.children is None:
            raise ValueError("All parent nodes must have a children")
        representation = f"<{self.tag}>"
        for child in self.children:
            representation += child.to_html()
        return representation + f"</{self.tag}>"

