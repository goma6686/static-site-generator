import os
from block_functions import markdown_to_html


def extract_title(markdown):
    #pulls h1 from markdown. If there is no h1, raises an error
    try:
        #find a line that starts with a single hash
        title = [line for line in markdown.split("\n") if line.startswith("# ")][0]
        title = title[2:]
    except:
        raise Exception("No title found in markdown file.")
    return title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    title = extract_title(markdown)

    html_string = markdown_to_html(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string.to_html())

    #Write the new full HTML page to a file at dest_path
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(content_dir, template_file, output_dir):
    #get full tree of files
    tree = os.listdir(content_dir)
    for entry in tree:
        #get full path
        entry_path = os.path.join(content_dir, entry)
        print(f"Processing {entry_path}")

        if os.path.isdir(entry_path):
            new_output_dir = os.path.join(output_dir, entry)
            print(f"Creating directory {new_output_dir}")
            generate_pages_recursive(entry_path, template_file, new_output_dir)

        elif os.path.isfile(entry_path) and entry.endswith(".md"):
            output_file = os.path.join(output_dir, "index.html")
            print(f"Generating {output_file}")
            generate_page(entry_path, template_file, output_file)
