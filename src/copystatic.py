import os
import shutil

def copy_static(src, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)

    for file in os.listdir(src):
        src_path = os.path.join(src, file)
        dest_path = os.path.join(dest, file)
        print(f" * {src_path} -> {dest_path}")
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            copy_static(src_path, dest_path)