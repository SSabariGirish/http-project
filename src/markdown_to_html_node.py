from markdown_to_blocks import markdown_to_blocks
from block_to_block import block_to_block_type,  BlockType
from text_to_textnodes import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

from htmlnode import HTMLNode
from parentnode import ParentNode


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)    
        children.append(html_node)
    return children

def markdown_to_html_node(doc: str) -> HTMLNode:

    cleaned_blocks = markdown_to_blocks(doc)
    list_of_html_nodes = []
    for block in cleaned_blocks:

        block_type = block_to_block_type(block)

        match block_type:

            case BlockType.HEADING:
                
                first_block = block.split()[0]
                h_size = first_block.count('#')
                
                value = " ".join(block.split()[1:])
                children = text_to_children(value)

                heading_node = ParentNode(f"h{h_size}", children)
                list_of_html_nodes.append(heading_node)
            
            case BlockType.PARAGRAPH:

                cleaned_block = block.replace("\n", " ")
                children = text_to_children(cleaned_block)
                
                para_node = ParentNode("p", children)
                list_of_html_nodes.append(para_node)
            
            case BlockType.CODE:

                front_removed = block[3:]
                back_removed = front_removed[:-3]
                back_removed = back_removed.lstrip()

                node_to_text = TextNode(back_removed, TextType.TEXT)
                leaf_node = text_node_to_html_node(node_to_text)

                children = [leaf_node]

                code_node = ParentNode("code", children)
                pre_node = ParentNode("pre", [code_node])
                list_of_html_nodes.append(pre_node)
            
            case BlockType.QUOTE:

                split_block = block.split("\n")
                split_block = [line[1:].lstrip() for line in split_block]
                cleaned_lines = " ".join(split_block)
                children = text_to_children(cleaned_lines) 

                quote_node = ParentNode("blockquote", children)
                list_of_html_nodes.append(quote_node)
            
            case BlockType.UNORDERED_LIST:

                split_block = block.split("\n")
                split_block = [line[2:].lstrip() for line in split_block]
                
                li_nodes = []
                for line in split_block:
                    children = text_to_children(line)
                    li_node = ParentNode("li", children)
                    li_nodes.append(li_node)
                
                ul_node = ParentNode("ul", li_nodes)
                list_of_html_nodes.append(ul_node)
            
            case BlockType.ORDERED_LIST:

                split_block = block.split("\n")
                split_block = [line.split(". ", 1)[1] for line in split_block]
                
                li_nodes = []
                for line in split_block:
                    children = text_to_children(line)
                    li_node = ParentNode("li", children)
                    li_nodes.append(li_node)
                
                ol_node = ParentNode("ol", li_nodes)
                list_of_html_nodes.append(ol_node)


    final_node = ParentNode("div", list_of_html_nodes)
    return final_node    

