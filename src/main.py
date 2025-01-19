from block_functions import markdown_to_html
from script import copy_files
from generate import generate_page

def main():
    copy_files()
    generate_page("./content/index.md", "template.html", "./public/index.html")

main()