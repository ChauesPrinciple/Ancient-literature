import os
import re
from pathlib import Path

# Base directory for the site
SITE_DIR = Path(r"C:\Users\rober\.gemini\antigravity\scratch\ancient-literature\site")
MODULES_DIR = SITE_DIR / "modules"

def get_modules():
    """Returns a sorted list of module directories."""
    modules = []
    if not MODULES_DIR.exists():
        return modules
    
    for item in MODULES_DIR.iterdir():
        if item.is_dir() and item.name.startswith("module-"):
            try:
                parts = item.name.split("-")
                num = int(parts[1])
                modules.append((num, item))
            except (IndexError, ValueError):
                continue
    
    modules.sort(key=lambda x: x[0])
    return [m[1] for m in modules]

def get_pages_in_module(module_dir):
    """Returns a sorted list of content HTML files in a module."""
    pages = []
    for item in module_dir.iterdir():
        if item.is_file() and item.suffix == ".html":
            pages.append(item)
    
    pages.sort(key=lambda x: x.name)
    return pages

def build_course_map():
    all_pages = []
    modules = get_modules()
    for mod in modules:
        pages = get_pages_in_module(mod)
        all_pages.extend(pages)
    return all_pages

def update_page_navigation(current_page, prev_page, next_page):
    try:
        with open(current_page, 'r', encoding='utf-8') as f:
            content = f.read()
            
        prev_link_html = ""
        next_link_html = ""
        
        if prev_page:
            if prev_page.name == "index.html":
                # To index.html from module subdir (e.g. site/modules/mod1/01.html)
                # rel path from current_page.parent to prev_page
                rel_path = os.path.relpath(prev_page, current_page.parent)
                rel_path = rel_path.replace("\\", "/")
                prev_link_html = f'<a href="{rel_path}" class="nav-btn prev">← Course Home</a>'
            else:
                rel_path = os.path.relpath(prev_page, current_page.parent)
                rel_path = rel_path.replace("\\", "/")
                prev_link_html = f'<a href="{rel_path}" class="nav-btn prev">← Previous</a>'
        
        if next_page:
            if next_page.name == "index.html":
                rel_path = os.path.relpath(next_page, current_page.parent)
                rel_path = rel_path.replace("\\", "/")
                next_link_html = f'<a href="{rel_path}" class="nav-btn next">Course Home →</a>'
            else:
                rel_path = os.path.relpath(next_page, current_page.parent)
                rel_path = rel_path.replace("\\", "/")
                next_link_html = f'<a href="{rel_path}" class="nav-btn next">Next →</a>'
        
        new_footer_inner = f"{prev_link_html}{next_link_html}"
        new_footer = f'<footer class="page-nav">\n                {new_footer_inner}\n            </footer>'
        
        # Regex replacement
        # Look for <footer class="page-nav">...</footer>
        # We need to be careful with whitespace
        pattern = r'<footer class="page-nav">.*?</footer>'
        
        if re.search(pattern, content, re.DOTALL):
            new_content = re.sub(pattern, new_footer, content, flags=re.DOTALL)
            
            with open(current_page, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated: {current_page.name}")
        else:
            print(f"Warning: Footer not found in {current_page.name}")

    except Exception as e:
        print(f"Error updating {current_page.name}: {e}")

def main():
    print("Building course map...")
    all_pages = build_course_map()
    print(f"Found {len(all_pages)} content pages.")
    
    course_home = SITE_DIR / "index.html"
    
    for i, page in enumerate(all_pages):
        prev_page = None
        next_page = None
        
        if i == 0:
            prev_page = course_home
        else:
            prev_page = all_pages[i-1]
            
        if i < len(all_pages) - 1:
            next_page = all_pages[i+1]
        else:
            next_page = course_home
            
        update_page_navigation(page, prev_page, next_page)
        
    print("Navigation update complete.")

if __name__ == "__main__":
    main()
