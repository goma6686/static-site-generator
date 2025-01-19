import unittest

from block_functions import *


class TestBlock(unittest.TestCase):
    def test_simple_markdown(self):
        markdown = """
            # This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is the first list item in a list block
            * This is a list item
            * This is another list item"""
        result = markdown_to_blocks(markdown)
        
        self.assertEqual(result[0], "# This is a heading")
        self.assertEqual(result[1], "This is a paragraph of text. It has some **bold** and *italic* words inside of it.")
        self.assertEqual(result[2], "* This is the first list item in a list block\n* This is a list item\n* This is another list item")

    def test_newlines_markdown(self):
        markdown = "# heading\n\n\n\ntext"
        result = markdown_to_blocks(markdown)

        self.assertEqual(result[0], "# heading")
        self.assertEqual(result[1], "text")


    def test_spaces_markdown(self):
        markdown = """# heading\n\n\n\nsome text  \n  with spaces"""
        result = markdown_to_blocks(markdown)

        self.assertEqual(result[0], "# heading")
        self.assertEqual(result[1], "some text\nwith spaces")

    def test_block_to_block_type(self):
        # Test heading
        assert block_to_block_type("# Heading") == "heading"
        assert block_to_block_type("###### Heading") == "heading"
        
        # Test code block
        assert block_to_block_type("```\ncode\n```") == "code"
        
        # Test quote
        assert block_to_block_type(">line1\n>line2") == "quote"
        
        # Test unordered list
        assert block_to_block_type("* item1\n* item2") == "unordered_list"
        assert block_to_block_type("- item1\n- item2") == "unordered_list"
        
        # Test ordered list
        assert block_to_block_type("1. item1\n2. item2") == "ordered_list"
        
        # Test paragraph
        assert block_to_block_type("Just a normal paragraph") == "paragraph"

    def test_empty_markdown(self):
        markdown = ""
        expected_html = "<div></div>"
        self.assertEqual(markdown_to_html(markdown), expected_html)

    def test_single_heading(self):
        markdown = "# Heading"
        expected_html = "<div><h1>Heading</h1></div>"
        self.assertEqual(markdown_to_html(markdown), expected_html)

    def test_multiple_blocks(self):
        markdown = """
        # Heading

        This is a paragraph of text.

        ```Code block```
        """
        expected_html = """<div><h1>Heading</h1><p>This is a paragraph of text.</p><pre><code>Code block</code></pre></div>"""
        self.assertEqual(markdown_to_html(markdown), expected_html.strip())
