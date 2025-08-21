import os
import shutil
from sys import argv
from static_to_public import copy_files_recursive
from extract_elem import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_docs = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def main():

    basepath = argv[1] if len(argv) > 1 else "/"
    print(basepath)  
    
    print("Deleting Public directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)
    
    print("Copying static files to public directory")        
    copy_files_recursive(src_rel_path=dir_path_static, dest_rel_path=dir_path_docs)
    
    print("Generating pages...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_docs, basepath=basepath)
    
if __name__ == "__main__":
    main()
    
