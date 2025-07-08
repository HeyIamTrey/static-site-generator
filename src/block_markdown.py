def markdown_to_blocks(markdown):
    new_blocks = []
    split_text = markdown.split("\n\n")
    for text in split_text:
        text = text.strip()
        if text == "":
            continue
        new_blocks.append(text)
    return new_blocks