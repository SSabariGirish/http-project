import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(doc: str) -> BlockType:
    
    if re.match(r"^#{1,6} ", doc):
        return BlockType.HEADING
    
    if re.match(r"^```\n(.*?)```$", doc, re.DOTALL):
        return BlockType.CODE
    
    
    doc_list = doc.split("\n")
    q_yes = True
    u_list = True
    o_list = True

    for line in doc_list:
        if not line.startswith(">"):
            q_yes = False
            break
    
    if q_yes:
        return BlockType.QUOTE

    for line in doc_list:
        if not re.match(r"^- ", line):
            u_list = False
            break
    
    if u_list:
        return BlockType.UNORDERED_LIST
    
    for i, line in enumerate(doc_list):
        if not re.match(rf"^{i + 1}\. ", line):
            o_list = False
            break
    
    if o_list:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH


    

    

