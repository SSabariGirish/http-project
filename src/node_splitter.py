from textnode import TextNode, TextType
from markdown_extractions import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(
    old_nodes: list[TextNode], 
    delimiter: str, 
    text_type: TextType) -> list[TextNode]:

    new_nodes = []

    for old_node in old_nodes:
        
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        
        else:    
            if text_type not in TextType:
                raise Exception("Invalid Markdown syntax provided")
            
            old_text = old_node.text
            split_words = old_text.split(delimiter)

            if len(split_words) % 2 == 0:
                raise Exception("Invalid Markdown syntax provided")
            
            temp_node_list = []

            for i, word in enumerate(split_words):
                if word == "":
                    continue
                
                if i % 2 == 0:
                    t = TextNode(word, TextType.TEXT)
                    temp_node_list.append(t)
                else:
                    t = TextNode(word, text_type)
                    temp_node_list.append(t)

            new_nodes.extend(temp_node_list)
    
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        matches = extract_markdown_images(old_node.text)

        if not matches:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text

        for alt_text, url in matches:
            markdown_image = f"![{alt_text}]({url})"
            before, remaining_text = remaining_text.split(markdown_image, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        matches = extract_markdown_links(old_node.text)

        if not matches:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text

        for link_text, url in matches:
            markdown_link = f"[{link_text}]({url})"
            before, remaining_text = remaining_text.split(markdown_link, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, url))

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


