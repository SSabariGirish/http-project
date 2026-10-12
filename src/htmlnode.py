class HTMLNode:

    def __init__(self, tag: str | None, value: str | None, children: list[HTMLNode] | None, props: dict[str, str] | None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Function is empty")
    
    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        prop_str = ""
        for key, value in self.props.items():
            prop_str += f'{key}="{value}" '
        prop_str = prop_str.strip()

        return prop_str
    
    def __repr__(self):
        prop_str = self.props_to_html()
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {prop_str})"
    