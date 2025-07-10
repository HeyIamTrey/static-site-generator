import os
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n\n")
    for line in lines:
        line = line.strip()
        if line.startswith("#") and not line[1:].startswith("#"):
            return line.lstrip("#").strip()
    raise ValueError("Syntax Error: There is no page title (no h1/# header)")

def generate_page(src_path, template_path, dest_path):
    print(f"Generating page from {src_path} to {dest_path} using {template_path}.")
    
    # Reading the markdown file to a variable
    with open(src_path, "r") as f:
        md = f.read()
        f.close()

    # Reading the template file to a variable
    with open(template_path, "r") as f:
        template = f.read()
        f.close()

    # Turning the Markdown into HTML and extracting the title from the Markdown
    node = markdown_to_html_node(md)
    html = node.to_html()
    title = extract_title(md)

    # Replacing the Title and Content in the Template with the Title and Content in the Source
    new_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    # Check if the destination path exists, creating it if it doesn't and, writing the new page to the destination file
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(new_page)
