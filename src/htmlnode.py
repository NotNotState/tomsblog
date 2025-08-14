class HTMLNode():

    def __init__(self, tag : str = None, value : str = None, children : list = None, props : dict = None):
       self.tag = tag
       self.value = value
       self.children = children
       self.props = props 

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self) -> str:
        if not self.props:
            return ""
        res = ""
        for key, value in self.props.items():
            res += f" {key}=\"{value}\""
        return res

    def __repr__(self) -> str:
        return f"(HTMLNode) TAG: {self.tag}, VALUE: {self.value}, CHILDREN: {self.children}, PROPS: {self.props}" 
    

class LeafNode(HTMLNode):

    def __init__(self, tag : str, value : str, props : dict = None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:

        if not self.value:
            raise ValueError("LeafNode Requires Value Field")
        
        if not self.tag:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"(LeafNode) TAG: {self.tag}, VALUE: {self.value}, CHILDREN: {self.children}, PROPS: {self.props}"


class ParentNode(HTMLNode):
    #note the lack of a value argument
    def __init__(self, tag : str, children : list, props : dict = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode Requires Tag")
        
        if not self.children:
            raise ValueError("ParentNode requires Children Nodes")
    
        inner_html = ""
        for child in self.children:
            inner_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{inner_html}</{self.tag}>"
    
    def __repr__(self):
        return f"(ParentNode) TAG: {self.tag}, VALUE: {self.value}, CHILDREN: {self.children}, PROPS: {self.props}"

    
