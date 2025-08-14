import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from textnode_to_htmlnode import text_node_to_leaf_node


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        node = HTMLNode(tag = "div", value = "penus", children=None, props={"href": "https://www.google.com", "target": "_blank"})

        self.assertEqual(" href=\"https://www.google.com\" target=\"_blank\"", node.props_to_html())
    
    def test_values(self):
        node = HTMLNode(tag = "div", value = "ancient roman penus")

        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "ancient roman penus")    
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HTMLNode(
            "p", 
            "None of the following count as gooning",
            None,
            {"class": "primary"}
        )
        valid = "(HTMLNode) TAG: p, VALUE: None of the following count as gooning, CHILDREN: None, PROPS: {'class': 'primary'}"
        self.assertEqual(repr(node), valid)
    
    #Testing leaf nodes
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello World!")
        self.assertEqual(node.to_html(), "<p>Hello World!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello World!")
        self.assertEqual(node.to_html(), "Hello World!")

    def test_leaf_repr(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(repr(node), "(LeafNode) TAG: a, VALUE: Click me!, CHILDREN: None, PROPS: {'href': 'https://www.google.com'}")

    #testing parent nodes + leaf nodes
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node]) 
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_mult_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node_two = LeafNode("i", "grandchild two")
        child_node = ParentNode("span", [grandchild_node]) 
        child_node_two = ParentNode("span", [grandchild_node_two])
        parent_node = ParentNode("div", [child_node, child_node_two])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span><span><i>grandchild two</i></span></div>")

    def test_to_html_link_child(self):
       child_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
       parent_node = ParentNode("div", [child_node])
       self.assertEqual(parent_node.to_html(), "<div><a href=\"https://www.google.com\">Click me!</a></div>")

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

    def test_parent_repr(self):
        child_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child_node]) 
        #repr() calls act on pointers to objects within the outer class as well
        self.assertEqual(repr(parent_node), "(ParentNode) TAG: div, VALUE: None, CHILDREN: [(LeafNode) TAG: a, VALUE: Click me!, CHILDREN: None, PROPS: {'href': 'https://www.google.com'}], PROPS: None")
    
    #TESTING TEXTNODE TO HTML NODE

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_leaf_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_leaf_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node") 

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_leaf_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code_node(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_leaf_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node") 

    def test_link_node(self):
        node = TextNode("This is a link node", TextType.LINK, url="https://www.google.com")
        html_node = text_node_to_leaf_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props["href"], "https://www.google.com")
        self.assertEqual(html_node.value, "This is a link node") 

    def test_image_node(self):
        node = TextNode("This is an image node", TextType.IMAGE, url="https://www.google.com")
        html_node = text_node_to_leaf_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["src"], "https://www.google.com")
        self.assertEqual(html_node.props["alt"], "This is an image node")  

    def test_single_to_html_from_text_node(self):
        node = TextNode("Click me!", TextType.LINK, url="https://www.google.com")
        html_node = text_node_to_leaf_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props["href"], "https://www.google.com")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

if __name__ == "__main__":
    unittest.main()