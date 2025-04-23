import os
from markdown_to_html import markdown_to_html_node


def extract_title(markdown: str) -> str:
    lines = [line.strip() for line in markdown.split("\n")]
    for line in lines:
        if line.startswith("# "):
            return line.split("# ")[1]
    raise ValueError("markdown content must contain a title")


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file = open(from_path)
    markdown = markdown_file.read()

    template_file = open(template_path)
    template = template_file.read()

    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()

    generated_page = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html
    )

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    dest_file = open(dest_path, "w")
    _ = dest_file.write(generated_page)

    template_file.close()
    markdown_file.close()


def generate_pages_recursive(
    source_path: str, template_path: str, destination_path: str
):
    children = os.listdir(source_path)

    for child in children:
        new_source_path = f"{source_path}/{child}"
        new_destination_path = f"{destination_path}/{child.replace(".md", ".html")}"
        if os.path.isfile(new_source_path):
            generate_page(new_source_path, template_path, new_destination_path)
        elif os.path.isdir(new_source_path):
            generate_pages_recursive(
                new_source_path, template_path, new_destination_path
            )
