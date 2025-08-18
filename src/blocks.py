from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType
from markdown_to_htmlnodes import text_to_textnodes
from textnode_to_htmlnode import text_node_to_leaf_node
import re

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'
    
def block_to_block_type(block : str) -> BlockType:
    
    if re.match(r"^(#{1,6})\s", block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        # should look something like >quote thing\n> quotes
        partition, good = block.split("\n"), True
        for part in partition:
            if part == "":
                continue
            if not part.startswith(">"):
                good = False
                break
        if good:
            return BlockType.QUOTE
    elif block.startswith("- "): #unordered list
        # should look something like - list\n- of\n\- something
        partition, good = block.split("\n"), True
        for part in partition:
            if part == "":
                continue
            if not part.startswith("-"):
                good = False
                break
        if good:
            return BlockType.UNORDERED_LIST
    elif block[0:3] == "1. ":
        partition, good = block.split("\n"), True
        for count, part in enumerate(partition):
            print(count, part)
            if not part[0:3] == str(count+1) + ". ":
                good = False
                break
        if good:
            return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

        
def markdown_to_blocks(markdown: str) -> list[str]:
    
    if len(markdown) == 0:
        return []
    blocks = []
    partition = markdown.strip().split("\n\n")
    for part in partition:
        if not part.count("\n") == len(part) and part != "":
            blocks.append(part.strip())
    return blocks

#MARKDOWN TO HTMLNODE HELPER FUNCTIONS

def text_to_children(text: str) -> list[HTMLNode]:
    nodes = text_to_textnodes(text)
    return [text_node_to_leaf_node(node) for node in nodes]
    
def paragraph_to_html_node(block: str) -> HTMLNode:
    return ParentNode(tag= "p", children=text_to_children(block))

def heading_to_html_node(block: str) -> HTMLNode:
    idx = 0
    while block[idx] == "#":
        idx += 1
    if idx >= len(block):
        raise ValueError(f"invalid heading level: {idx}")
    block = block[idx + 1 : ]
    tag = "h" + str(idx)
    return ParentNode(tag = tag, children=text_to_children(block))

def code_to_html_node(block: str) -> HTMLNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalide code block in Markdown to Htmlnode")
    block = block.removeprefix("```").removesuffix("```")
    node = text_node_to_leaf_node(TextNode(text=block, text_type=TextType.CODE))
    wrapper_node = ParentNode(tag = "pre", children=[node])
    return wrapper_node

def quote_to_html_node(block: str) -> HTMLNode:
    items = block.split("\n")
    clean_block = " ".join([ item.removeprefix(">") for item in items if item != ""])
    wrapper_node = ParentNode(tag="blockquote", children=text_to_children(clean_block))
    return wrapper_node

def ul_to_html_node(block: str) -> HTMLNode:
    items = block.split("\n")
    clean_items = [ item.removeprefix("- ") for item in items if item != "" ]
    nodes = [ ParentNode(tag="li", children=text_to_children(item)) for item in clean_items ]
    wrapper_node = ParentNode(tag="ul", children=nodes)
    return wrapper_node

def ol_to_html_node(block: str) -> HTMLNode:
    items = block.split("\n")
    clean_items = [ item.removeprefix(str(idx + 1) + ". ") for idx, item in enumerate(items) if item != ""]
    nodes = [ ParentNode(tag="li", children=text_to_children(item)) for item in clean_items ]
    wrapper_node = ParentNode(tag="ol", children=nodes)
    return wrapper_node

def markdown_to_html_node(markdown: str) -> HTMLNode:
    root_html_node = ParentNode(tag = "div", children=[])
    blocks = markdown_to_blocks(markdown=markdown)
    
    for block in blocks:
        
        block_t: BlockType = block_to_block_type(block=block)
        
        match block_t:
            case BlockType.PARAGRAPH:
                root_html_node.children.append(paragraph_to_html_node(block))
            case BlockType.HEADING:
                root_html_node.children.append(heading_to_html_node(block))
            case BlockType.CODE:
                root_html_node.children.append(code_to_html_node(block))
            case BlockType.QUOTE:
                root_html_node.children.append(quote_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                root_html_node.children.append(ul_to_html_node(block))
            case BlockType.ORDERED_LIST:
                root_html_node.children.append(ol_to_html_node(block))
            case _:
                raise TypeError(f"INVALID BLOCKTYPE: Unkown BlockType in markdown_to_html_node() call")
        
    return  root_html_node