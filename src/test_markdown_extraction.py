import unittest
from extract_elem import extract_title


class TestHTMLNode(unittest.TestCase):
    
    
    def test_extract_h1_simple(self):
        extract = extract_title("./test_content/test_1.md")
        self.assertEqual(extract, "Heading and other stuff")
        
    def test_extract_h1_tolkien(self):
        extract = extract_title("./test_content/test_2.md")
        self.assertEqual(extract, "Tolkien Fan Club") 

if __name__ == "__main__":
    unittest.main()