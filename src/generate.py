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
    with open(dest_path, "w") as f:
        f.write(template)

    