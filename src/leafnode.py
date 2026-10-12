from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    def __init__(self, tag: str | None, value: str | None, props: dict[str, str] | None):
        super().__init__(tag, value, None, props)
    
    def to_html(self) -> str:
        if self.tag == "img":
            inner_tag = super().props_to_html()
            return f"<img {inner_tag}/>"

        if self.value is None:
            raise ValueError("Leaf Nodes must have a value")

        if self.tag is None:
            return self.value

        if self.tag == "a":
            inner_tag = super().props_to_html()
            return f'<a {inner_tag}>{self.value}</a>'
        else:
            return f'<{self.tag}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        prop_str = super().props_to_html()
        return f"LeafNode({self.tag}, {self.value}, {prop_str})"
    
    def __eq__(self, other: LeafNode) -> bool:
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.props == other.props
        )