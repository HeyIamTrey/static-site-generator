import shutil
import os

from copystatic import copy_static
from generatepage import generate_page

dir_path_static = "./static"
dir_path_public = "./public"

def main():
    if os.path.isdir(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    print("Copying static files to public directory...")
    copy_static(dir_path_static, dir_path_public)

    generate_page("content/index.md", "template.html", "public/index.html")

main()