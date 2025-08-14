import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_text_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a somewhat different node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_type_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, url="https://www.penus")
        node2 = TextNode("This is a text node", TextType.BOLD, url="https://www.penus")
        self.assertEqual(node, node2)
    
    def test_url_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, url="https://www.penus")
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_both_url_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, url="https://www.penus")
        node2 = TextNode("This is a text node", TextType.CODE, url="https://www.PENUS")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, url="https://www.penus") 
        self.assertEqual(
            "TextNode(This is a text node, bold, https://www.penus)", repr(node)
        )

if __name__ == "__main__":
    unittest.main()
