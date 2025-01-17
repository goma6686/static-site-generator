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
