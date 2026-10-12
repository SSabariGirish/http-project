import os
import shutil
from markdown_to_html_node import markdown_to_html_node

def copy_static(source: str, destination: str) -> None:
    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)

    _copy_contents(source, destination)


def _copy_contents(source: str, destination: str) -> None:
    for name in os.listdir(source):
        source_path = os.path.join(source, name)
        destination_path = os.path.join(destination, name)

        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
            print(f"Copied file: {source_path} -> {destination_path}")

        else:
            os.mkdir(destination_path)
            _copy_contents(source_path, destination_path)


def extract_title(markdown):
    for line in markdown.splitlines():
        stripped_line = line.strip()

        if stripped_line.startswith("# ") and not stripped_line.startswith("## "):
            return stripped_line[2:].strip()

    raise Exception("No H1 heading found")



def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} to {dest_path} "
        f"using {template_path}"
    )

    with open(from_path, "r", encoding="utf-8") as file:
        markdown = file.read()

    with open(template_path, "r", encoding="utf-8") as file:
        template = file.read()

    html_content = markdown_to_html_node(markdown).to_html()

    title = extract_title(markdown)

    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(full_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    os.makedirs(dest_dir_path, exist_ok=True)

    for entry in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(source_path):
            if entry.endswith(".md"):
                dest_path = dest_path.removesuffix(".md") + ".html"
                generate_page(source_path, template_path, dest_path)

        else:
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(
                source_path,
                template_path,
                dest_path,
            )
    

def main():
    copy_static("static", "public")

    generate_pages_recursive(
        "content",
        "template.html",
        "public",
    )
    
if __name__ == "__main__":
    main()