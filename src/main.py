import os
import shutil
from htmlnode import ParentNode, LeafNode
from markdown_blocks import markdown_to_html_node


def copy_files(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    # Ensure source exists
    if not os.path.exists(src):
        raise ValueError(f"Source directory '{src}' does not exist.")

    # Create the destination directory
    os.makedirs(dest, exist_ok=True)

    # Iterate over each item in the source directory
    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dest_item = os.path.join(dest, item)
        if os.path.isdir(src_item):
            # Recursively copy subdirectory
            copy_files(src_item, dest_item)
        else:
            # Copy the file
            shutil.copy2(src_item, dest_item)


def extract_title(markdown: str):
    title_pos = markdown.find("# ")
    if title_pos == -1:
        raise ValueError("This markdown doesn't contain a header.")
    title = markdown[title_pos:].split("\n")[0]
    return title.replace("# ", "").strip()


def generate_page(from_path, template_path, dest_path):
    dest_path = dest_path.replace(".md", ".html")
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        content_text = file.read()
    with open(template_path, "r") as file:
        template_text = file.read()
    content = markdown_to_html_node(content_text)
    content = content.to_html()
    title = extract_title(content_text)
    html_output = template_text.replace("{{ Title }}", title)
    html_output = html_output.replace("{{ Content }}", content)
    with open(dest_path, "w") as output:
        output.write(html_output)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise ValueError(f"Source directory '{dir_path_content}' does not exist.")
    os.makedirs(dest_dir_path, exist_ok=True)
    # Iterate over each item in the source directory
    for item in os.listdir(dir_path_content):
        src_item = os.path.join(dir_path_content, item)
        dest_item = os.path.join(dest_dir_path, item)
        if os.path.isdir(src_item):
            # Recursively Generate HTML Files
            generate_pages_recursive(src_item, template_path, dest_item)
        else:
            # Generate HTML File
            generate_page(src_item, template_path, dest_item)


def main():
    src = "/home/jsolt/StaticSiteGenerator/static"
    dst = "/home/jsolt/StaticSiteGenerator/public"
    copy_files(src, dst)

    from_path = "/home/jsolt/StaticSiteGenerator/content/"
    template_path = "/home/jsolt/StaticSiteGenerator/template.html"
    dest_path = "/home/jsolt/StaticSiteGenerator/public/"
    generate_pages_recursive(from_path, template_path, dest_path)


main()
