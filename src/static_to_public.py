import os
import shutil
        
def copy_files_recursive(src_rel_path: str, dest_rel_path: str):
    if not os.path.exists(dest_rel_path):
        os.mkdir(dest_rel_path)
    
    for file in os.listdir(src_rel_path):
        src_path = os.path.join(src_rel_path, file)
        dest_path = os.path.join(dest_rel_path, file)
        
        if os.path.isfile(src_path):
            print(f"Copying: {src_path} -> {dest_path}")
            shutil.copyfile(src_path, dest_path)
        else:
            copy_files_recursive(src_path, dest_path)