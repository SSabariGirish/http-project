from htmlnode import HTMLNode

class ParentNode(HTMLNode):

    def __init__(
        self, 
        tag: str | None, 
        children: list[HTMLNode] | None, 
        props: dict[str, str] | None = None
    ):
        super().__init__(tag, None, children, props)
    
    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Parent Nodes must have tags")

        if self.children is None:
            raise ValueError("Parent Nodes must have children")
        
        prop_starter = f"<{self.tag}>"
        prop_ender = f"</{self.tag}>"

        prop_str = ""
        for child in self.children:
            prop_str += child.to_html()
        
        return prop_starter + prop_str + prop_ender
    