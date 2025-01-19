from block_functions import markdown_to_html
from script import copy_files
from generate import generate_pages_recursive

def main():
    copy_files()
    generate_pages_recursive("./content/", "template.html", "./public/")

main()