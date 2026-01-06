import os
import re

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the regex to find the brand section
    # tailored to the specific formatting seen in the file
    brand_pattern = re.compile(r'(<div class="brand">\s*<h1>Ancient<br>Literature</h1>)(\s*</div>)', re.DOTALL)
    
    dropdown_html = """
    <div class="dropdown-menu">
        <a href="https://chauesprinciple.github.io/Ancient-literature/" class="dropdown-item current">Ancient Literature</a>
        <a href="https://chauesprinciple.github.io/Tokyo-in-Film/" class="dropdown-item">Tokyo in Film</a>
    </div>"""

    if brand_pattern.search(content):
        # Insert the dropdown before the closing div of .brand
        new_content = brand_pattern.sub(r'\1' + dropdown_html + r'\2', content)
        
        # Only write if changes were made (redundancy check not strictly needed if regex matched, but good practice)
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated: {filepath}")
        else:
            print(f"No changes made to (content match issue?): {filepath}")
    else:
        print(f"Pattern not found in: {filepath}")

def main():
    root_dir = "C:/Users/rober/.gemini/antigravity/scratch/ancient-literature/modules"
    
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(subdir, file)
                update_file(filepath)

if __name__ == "__main__":
    main()
