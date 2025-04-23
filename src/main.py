import os
import shutil

from generate_pages import generate_pages_recursive
from htmlnode import HTMLNode
from markdown_to_html import markdown_to_html_node


def copy_dir(source_path: str, destination_path: str):
    if os.path.exists(destination_path):
        print(f"removing directory {destination_path}")
        shutil.rmtree(destination_path)

    print(f"creating directory {destination_path}")
    os.mkdir(destination_path)

    children = os.listdir(source_path)

    for child in children:
        new_source_path = f"{source_path}/{child}"
        new_destination_path = f"{destination_path}/{child}"
        if os.path.isfile(new_source_path):
            print(f"copying {new_source_path} to {new_destination_path}")
            _ = shutil.copy(new_source_path, new_destination_path)
        elif os.path.isdir(new_source_path):
            copy_dir(new_source_path, new_destination_path)


def main():
    copy_dir("./static", "./public")
    generate_pages_recursive("./content", "./template.html", "./public")


main()
