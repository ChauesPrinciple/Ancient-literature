import os
import re
from pathlib import Path

SITE_DIR = Path("site")

def main():
    count = 0
    for root, dirs, files in os.walk(SITE_DIR):
        for file in files:
            if file.endswith(".html"):
                file_path = Path(root) / file
                
                # Determine relative path back to site root
                # root is e.g. site/modules/module-1
                # relative_to site: modules/module-1
                rel_parts = file_path.parent.relative_to(SITE_DIR).parts
                depth = len(rel_parts)
                
                if depth == 0:
                    link_target = "video_gallery.html"
                else:
                    link_target = "../" * depth + "video_gallery.html"
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if already added
                if "Video Gallery" in content:
                    continue
                
                # Find Glossary link
                # We look for <a href="...glossary.html...">Glossary</a>
                # And inject after it closing </a>
                
                pattern = r'(<a href="[^"]*glossary.html"[^>]*>Glossary</a>)'
                replacement = f'\\1\n                    <a href="{link_target}">Video Gallery</a>'
                
                new_content = re.sub(pattern, replacement, content)
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    count += 1
                    
    print(f"Updated {count} files with Video Gallery link.")

if __name__ == "__main__":
    main()
