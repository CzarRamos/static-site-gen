from textnode import TextNode
from textnode import TextType
import os
import re
import shutil
from generatepage import generate_pages_recursive

STATIC_FOLDER_PATH = "./static"
PUBLIC_FOLDER_PATH = "./public"
MARKDOWN_CONTENT_PATH = "content"
HTML_TEMPLATE_PATH = "./template.html"

def copy_static_to_public_folder(path):
    current_path = path
    # get all items in current path
    with os.scandir(path) as it:
        for entry in it:
            # create equivalent version of static in public
            public_equivalent = re.sub(rf'^{STATIC_FOLDER_PATH}', PUBLIC_FOLDER_PATH, current_path)
            if not os.path.exists(public_equivalent):
                os.mkdir(public_equivalent)

            # Checks for any child directories
            if not entry.name.startswith('.') and entry.is_dir():
                next_path = f"{current_path}/{entry.name}"
                copy_static_to_public_folder(next_path)
            elif entry.is_file(): # checks for the file themselves
                src = f"{current_path}/{entry.name}"
                # make a copy of the item in the public folder equivalent
                dst = re.sub(rf'^{STATIC_FOLDER_PATH}', PUBLIC_FOLDER_PATH, src)
                shutil.copy(src, dst)

def main():
    # recreate public folder
    if os.path.exists(PUBLIC_FOLDER_PATH):
        # delete public folder for regeneration
        shutil.rmtree(PUBLIC_FOLDER_PATH)
        
    os.mkdir(PUBLIC_FOLDER_PATH)
    
    # copies all items to public folder
    copy_static_to_public_folder(STATIC_FOLDER_PATH)

    # The line below has the same functionality as above
    # But I wanted to familiarize myself with the os and shutils library
    #shutil.copytree(STATIC_FOLDER_PATH, PUBLIC_FOLDER_PATH)
    
    generate_pages_recursive("./content", HTML_TEMPLATE_PATH, PUBLIC_FOLDER_PATH)
    

if __name__ == "__main__":
    main()