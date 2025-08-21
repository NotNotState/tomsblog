import os
from blocks import markdown_to_html_node


def extract_title(markdown: str) -> str:
    try:
        with open(markdown, "r") as file:
            # may need to file.read() and split on \n\n
            lines = file.readlines()
            file.close()
            for line in lines:
                if line.startswith("# "):
                    return line.strip("#").strip()
            
    except FileNotFoundError as e:
        print(e)
        return 
        
    raise ValueError(f"No h1 tag found in {markdown} file")

def read_from_path(from_path: str) -> str:
    content = ""
    try:
        with open(from_path, "r") as file:
            content = file.read()
            file.close()
    except FileNotFoundError as e:
        print(e)

    return content

def write_to_dest(dest_path: str, content: str):
    dirs, _ = os.path.split(dest_path)
    os.makedirs(dirs, exist_ok=True) #will create dirs if not present
    try:
        with open(dest_path, "w") as file:
            content = file.write(content)            
            print("Successful Write!!")
            file.close()
    except FileNotFoundError as e:
        print(e)


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    dest_path = dest_path.replace(".md", ".html")
    print(f'Generating page from {from_path} -> {dest_path}...')
    title = extract_title(from_path)
    content_md = read_from_path(from_path)
    content_template = read_from_path(template_path)
    content_html = markdown_to_html_node(content_md).to_html()
    page = content_template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", content_html)
    page = page.replace("href=\"/", f"href=\"{basepath}")
    page = page.replace("src=\"/", f"src=\"{basepath}")
    write_to_dest(dest_path, page) 
    

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str):
    
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
        
    for file in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        
        if os.path.isfile(content_path):
            generate_page(from_path=content_path, template_path=template_path, dest_path=dest_path, basepath=basepath)
        else:
            generate_pages_recursive(content_path, template_path, dest_path, basepath=basepath)
            
