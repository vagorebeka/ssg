import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    # count: 4, total: 15
    def test1(self):
        testprops = {"href": "https://google.com", "target": "_blank"}
        node = HTMLNode("a", None, None, testprops)
        self.assertEqual(node.props_to_html(), ' href="https://google.com" target="_blank"')
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.children, None)
        
    def test2(self):
        testprops = {"href": "https://boot.dev", "target": "_blank"}
        node = HTMLNode(tag="a", value="random text", props=testprops)
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.children, None)
        self.assertEqual(node.value, "random text")

    def test3(self):
        testprops = {"href": "https://google.com"}
        test_children = [HTMLNode(tag="a", props=testprops), HTMLNode(tag="b", value="bold text")]
        node = HTMLNode(tag="p", value="a paragraph of text", children=test_children)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.children, test_children)
        self.assertEqual(node.value, "a paragraph of text")
        
    def test4(self):
        with self.assertRaises(NotImplementedError) as error:
            HTMLNode().to_html()
        self.assertEqual(str(error.exception), "to_html method not implemented")

    # LeafNode tests
    # count: 5
    def test_leaf1(self):
        node = LeafNode("p", "text content")
        self.assertEqual(node.to_html(), "<p>text content</p>")

    def test_leaf2(self):
        testprops = {"href": "https://google.com"}
        node = LeafNode(tag="a", value="test", props=testprops)
        self.assertEqual(node.props_to_html(), ' href="https://google.com"')

    def test_leaf3(self):
        node = LeafNode(None, "test text")
        self.assertEqual(node.to_html(), "test text")
    
    def test_leaf4_no_value(self):
        with self.assertRaises(ValueError) as error:
            LeafNode("a", None).to_html()
        self.assertEqual(str(error.exception), "Invalid HTML: value must be provided")
    
    def test_leaf5(self):
        with self.assertRaises(TypeError):
            LeafNode()

    # ParentNode tests
    # count: 6
    # Test all the edge cases you can think of, including nesting ParentNode objects inside of one
    # another, multiple children, and no children.
    def test_parent1(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parent2_parent_in_parent(self):
        node = ParentNode(
            "p", 
            [
                ParentNode("b", 
                           [LeafNode("i", "bold italic text")]),
                LeafNode(None, "normal text")
            ]
        )

        self.assertEqual(type(node.children[0]), ParentNode)
        self.assertEqual(node.children[1].to_html(), "normal text")

    def test_parent3_no_children(self):
        with self.assertRaises(ValueError) as error:
            ParentNode("a", None).to_html()
        self.assertEqual(str(error.exception), "Invalid HTML: children must be provided")

    def test_parent4_no_tag(self):
        with self.assertRaises(ValueError) as error:
            ParentNode(None, [LeafNode(None, "text")]).to_html()
        self.assertEqual(str(error.exception), "Invalid HTML: tag must be provided")

    def test_parent5(self):
        node = ParentNode(
            "p",
            [
                ParentNode("b",
                           [
                                ParentNode("i",
                                          [LeafNode("u", "underlined italic bold text"),
                                           LeafNode(None, "italic bold text")]),
                                LeafNode(None, "bold text")
                           ]),
                LeafNode(None, "normal text")
            ]
        )
        self.assertIsInstance(node, ParentNode)
        self.assertIsInstance(node.children[0], ParentNode)
        self.assertIsInstance(node.children[0].children[0], ParentNode)
        self.assertIsInstance(node.children[0].children[0].children[0], LeafNode)

    def test_parent6(self):
        with self.assertRaises(TypeError):
            ParentNode()


if __name__ == "__main__":
    unittest.main()