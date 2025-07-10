import unittest
from generatepage import(
    extract_title,
    generate_page,
)

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        md = """
# This is the page title

This is just a paragraph under the title.
"""
        self.assertEqual(extract_title(md), "This is the page title")

    def test_extract_title_no_title(self):
        md = """
## This is not the page title

This page has no title.
"""
        with self.assertRaises(ValueError):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()
