import re
from textnode import TextNode, TextType

def extract_markdown_images(text : str) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_delimiter(old_nodes : list[TextNode], delimiter : str, text_type : TextType) -> list:
    new_nodes = []
    for node in old_nodes: 
        if node.text_type != TextType.TEXT: 
            new_nodes.append(node)
            continue

        parsed = []
        temp = node.text.split(delimiter)
        #check that delimiters are matched, follows same logic as ensuring even number of delimiters in string
        if len(temp) % 2 == 0:
            raise ValueError(f"Un-matched Delimiters of type: {text_type} in TextNode: {repr(node)}")        
        
        for idx, elem in enumerate(temp):
            if elem == "":
                continue
            
            if idx % 2 == 0:
                parsed.append(TextNode(text=elem, text_type=TextType.TEXT))
            else:
                parsed.append(TextNode(text=elem, text_type=text_type))

        new_nodes.extend(parsed)
                
    return new_nodes 

def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        content = node.text
        matches = extract_markdown_images(content)
        split_items = [ f"![{alt}]({url})" for alt,url in matches]
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        
        temp = []
        for idx, item in enumerate(split_items):
            partition = content.split(item, 1)
            
            if len(partition) != 2:
                raise ValueError("invalid markdown, image section not closed")

            if partition[0] != "":
                temp.append(TextNode(partition[0], TextType.TEXT))

            temp.append(TextNode(text=matches[idx][0], text_type=TextType.IMAGE, url=matches[idx][1]))
            content = partition[1]

        new_nodes.extend(temp)
        if content != "":
            new_nodes.append(TextNode(text=content, text_type=TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        content = node.text
        matches = extract_markdown_links(content)
        split_items = [ f"[{alt}]({url})" for alt,url in matches]
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        """
        find matches (preserves ordering)=> map them to how they appear in the string (split_item) 
        iterate through split_items
            split once (max_splits = 1) on split_item_n, convert left partition to textnode if not "" and append
            create link/image node on split_item_n and append
            remove left partition from original node text (content)
        return
        """
        temp = []
        for idx, item in enumerate(split_items):
            partition = content.split(item, 1)
            if len(partition) != 2:
                raise ValueError("invalid markdown, link section not closed")
            
            if partition[0] != "":
                temp.append(TextNode(partition[0], TextType.TEXT))

            temp.append(TextNode(text=matches[idx][0], text_type=TextType.LINK, url=matches[idx][1]))
            content = partition[1]

        new_nodes.extend(temp)
        if content != "":
            new_nodes.append(TextNode(text=content, text_type=TextType.TEXT)) 
    
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text=text, text_type=TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", text_type=TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", text_type=TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", text_type=TextType.CODE)
    nodes = split_nodes_image(nodes)
    # print(nodes)
    nodes = split_nodes_link(nodes)
    return nodes