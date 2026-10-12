
def markdown_to_blocks(doc: str) ->  List[str]:

    raw_blocks = doc.split("\n\n")
    cleaned_blocks_v1 = [block.strip() for block in raw_blocks]
    final_cleaned_blocks = [block for block in cleaned_blocks_v1 if block]

    return final_cleaned_blocks

