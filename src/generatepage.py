import os
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n\n")
    for line in lines:
        line = line.strip()
        if line.startswith("#") and not line[1:].startswith("#"):
            return line.lstrip("#").strip()
    raise ValueError("Syntax Error: There is no page title (no h1/# header)")

def generate_page(src_path, template_path, dest_path, basepath):
    dest_path = dest_path.replace(".md", ".html")
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
    new_page = new_page.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    # Check if the destination path exists, creating it if it doesn't and, writing the new page to the destination file
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(new_page)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for file in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(src_path):
            if src_path.endswith(".md"):
                generate_page(src_path, template_path, dest_path, basepath)
        else:
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            generate_page_recursive(src_path, template_path, dest_path, basepath)