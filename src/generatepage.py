import re
import os
from extractmarkdown import get_html_string_from_markdown

def extract_title(markdown):
    title = re.findall(r'^(#(?!#){1}.+)', markdown)
    if len(title) > 0:
        return title[0].strip("#").strip()
    raise Exception("Missing title! Please add header 1 text at the beginning of the page.")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # grab markdown
    markdown_file = open(f"{from_path}/index.md", "r").read()
    #grab html template
    template_file = open(template_path, "r").read()
    # convert markdown to html
    html_contents = get_html_string_from_markdown(markdown_file)
    # grab the title
    title = extract_title(markdown_file)
    # add title and contents to the html template
    template_file = re.sub(r'{{ Title }}', title, template_file)
    template_file = re.sub(r'{{ Content }}', html_contents, template_file)

    # Make sure dest path exists:
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    open(f"{dest_path}/index.html", "w").write(template_file)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    with os.scandir(dir_path_content) as it:
        for entry in it:
            current_path = f"{dir_path_content}/{entry.name}"
            dest_path = f"{dest_dir_path}/{entry.name}"
            
            # Checks for any child directories
            if not entry.name.startswith('.') and entry.is_dir():
                if not os.path.exists(dest_path):
                    os.mkdir(dest_path)
                generate_pages_recursive(current_path, template_path, dest_path)
            elif entry.is_file(): # checks for the file themselves
                #print(f"generate page from {current_path} to {dir_path_content}")
                generate_page(dir_path_content, template_path, dest_dir_path)