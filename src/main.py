import shutil
import os
import sys

from copystatic import copy_static
from generatepage import generate_page_recursive

dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    command = sys.argv
    if len(command) > 1:
        basepath = command[1]
    else:
        basepath = "/"

    if os.path.isdir(dir_path_docs):
        shutil.rmtree(dir_path_docs)
    
    print("Copying static files to public directory...")
    copy_static(dir_path_static, dir_path_docs)

    generate_page_recursive(dir_path_content, template_path, dir_path_docs, basepath)

main()