import xml.etree.ElementTree as ET
import os
import shutil
import re
from pathlib import Path
import urllib.parse
import sys

# Configuration
SOURCE_DIR = Path("extracted")
OUTPUT_DIR = Path("site")
MANIFEST_PATH = SOURCE_DIR / "imsmanifest.xml"
ASSETS_DIR = OUTPUT_DIR / "assets"
MODULES_DIR = OUTPUT_DIR / "modules"

# Namespaces in the XML
NS = {
    'ims': 'http://www.imsglobal.org/xsd/imsccv1p3/imscp_v1p1',
    'lom': 'http://ltsc.ieee.org/xsd/imsccv1p3/LOM/resource'
}

def clean_title(title):
    """Sanitize titles for filenames."""
    if not title:
        return "untitled"
    s = re.sub(r'[^a-zA-Z0-9\s-]', '', title).strip().lower()
    return re.sub(r'[-\s]+', '-', s)

def ensure_dirs():
    if not OUTPUT_DIR.exists():
        OUTPUT_DIR.mkdir()
    if not ASSETS_DIR.exists():
        ASSETS_DIR.mkdir()
    if not MODULES_DIR.exists():
        MODULES_DIR.mkdir()

def load_manifest():
    if not MANIFEST_PATH.exists():
        print(f"Error: Manifest not found at {MANIFEST_PATH}")
        sys.exit(1)
    tree = ET.parse(MANIFEST_PATH)
    return tree.getroot()

def get_resources(root):
    """Map identifier -> {type, href, files}"""
    resources = {}
    for res in root.findall(".//ims:resource", NS):
        ident = res.get('identifier')
        try:
            file_elem = res.find("ims:file", NS)
            href = file_elem.get('href') if file_elem is not None else None
            
            resources[ident] = {
                'type': res.get('type'),
                'href': href,
                'dependencies': [dep.get('identifierref') for dep in res.findall("ims:dependency", NS)]
            }
        except Exception as e:
            print(f"Warning processing resource {ident}: {e}")
    return resources

def process_html_content(src_path, dest_path, relative_depth):
    """
    Read HTML content, strip body, inject into our template.
    """
    try:
        with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Some files might be just text or weirdly formatted
        if not content:
            return "<p>No content found.</p>"
            
        # Clean up Microsoft Word garbage if present
        content = re.sub(r' class="[^"]*"', '', content)
        
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
        if body_match:
            body_content = body_match.group(1)
        else:
            if "<html" in content:
                # Malformed html?
                body_content = content
            else:
                # Plain text or fragment
                body_content = content
        
        def fix_link(match):
            attr = match.group(1) 
            quote = match.group(2)
            link = match.group(3)
            
            if link.startswith('http') or link.startswith('#') or link.startswith('mailto'):
                return match.group(0)
            
            # Decode URL
            link_decoded = urllib.parse.unquote(link)
            
            # Resolve absolute path of the target
            # content is in src_path.parent
            abs_target = (src_path.parent / link_decoded).resolve()
            
            if not abs_target.exists():
                # Try finding it in the root content dir if relative fail
                # Some packages are messy
                return match.group(0)

            # Copy to media
            media_dir = ASSETS_DIR / "media"
            if not media_dir.exists():
                media_dir.mkdir()
                
            new_filename = f"{src_path.stem}_{Path(link_decoded).name}"
            # Copy
            shutil.copy2(abs_target, media_dir / new_filename)
            
            return f'{attr}={quote}../../assets/media/{new_filename}{quote}'

        body_content = re.sub(r'(src|href)=("|\')([^"\']+)("|\')', fix_link, body_content)
        return body_content

    except Exception as e:
        return f"<p>Error processing content: {e}</p>"

def create_page(title, content, module_title, module_items, current_filename, prev_link=None, next_link=None):
    nav_links = ""
    if prev_link:
        nav_links += f'<a href="{prev_link}" class="nav-btn prev">← Previous</a>'
    if next_link:
        nav_links += f'<a href="{next_link}" class="nav-btn next">Next →</a>'
        
    # Build Sidebar Navigation
    sidebar_nav_html = ""
    for item in module_items:
        active_class = ' class="active-link"' if item['filename'] == current_filename else ''
        sidebar_nav_html += f'<a href="{item["filename"]}"{active_class}>{item["title"]}</a>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Ancient Literature</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../../assets/style.css">
</head>
<body>
    <div class="layout">
        <aside class="sidebar">
            <div class="brand">
                <h1>Ancient<br>Literature</h1>
            </div>
            <nav>
                <a href="../../index.html" class="home-link">← Course Home</a>
                
                <div class="current-module">
                    <h3>{module_title}</h3>
                </div>
                <div class="module-nav">
                    {sidebar_nav_html}
                </div>
                
                <div class="current-module" style="margin-top: 2rem; border-top: 1px solid #ccc; padding-top: 1rem;">
                     <h3>Resources</h3>
                </div>
                <div class="module-nav">
                    <a href="../../glossary.html">Glossary</a>
                </div>
            </nav>
        </aside>
        
        <main class="content-area">
            <header class="page-header">
                <h2>{title}</h2>
            </header>
            
            <article class="prose">
                {content}
            </article>

            <section class="discussion-prompt">
                <h3>Reflect & Discuss</h3>
                <p>Engage with the text and your peers using the reading questions above.</p>
                <div class="note-area">
                    <textarea placeholder="Write your thoughts here... (Notes are local only)"></textarea>
                </div>
            </section>
            
            <footer class="page-nav">
                {nav_links}
            </footer>
        </main>
    </div>
</body>
</html>"""
    return html

def safe_get_text(elem):
    if elem is not None and elem.text:
        return elem.text.strip()
    return "Untitled Item"

def main():
    print("Starting conversion...")
    ensure_dirs()
    root = load_manifest()
    resources = get_resources(root)
    
    orgs = root.find("ims:organizations", NS)
    if orgs is None:
        print("No organizations found.")
        return
    org = orgs[0]
    
    modules = []
    
    # Iterate to find the actual list of modules
    # Some exports wrap everything in a single root item
    top_items = org.findall("ims:item", NS)
    
    if len(top_items) == 1 and not top_items[0].find("ims:title", NS):
        print("Unwrapping root item...")
        # This is likely a wrapper
        module_items = top_items[0].findall("ims:item", NS)
    else:
        module_items = top_items

    # Blacklist of modules to exclude
    EXCLUDED_MODULES = [
        "For Instructors Only",
        "Getting Started",
        "Assignments and Engagement"
    ]

    for module_item in module_items:
        title_elem = module_item.find("ims:title", NS)
        module_title = safe_get_text(title_elem)
        
        # Check for exclusions (partial match to catch "For Instructors Only (hidden...)")
        if any(excluded in module_title for excluded in EXCLUDED_MODULES):
            print(f"Skipping excluded module: {module_title}")
            continue

        module_slug = clean_title(module_title)

        
        print(f"Processing Module: {module_title}")
        
        mod_dir = MODULES_DIR / module_slug
        if not mod_dir.exists():
            mod_dir.mkdir()
            
        items = []
        children = module_item.findall("ims:item", NS)
        
        for i, item in enumerate(children):
            item_title = safe_get_text(item.find("ims:title", NS))
            ident_ref = item.get('identifierref')
            
            if not ident_ref:
                # It might be a sub-folder/sub-header without a link
                # We can handle this, but for now let's skip or handle valid contents
                continue
                
            if ident_ref not in resources:
                print(f"  Skipping {item_title} (resource {ident_ref} not found)")
                continue

            res = resources[ident_ref]
            if not res['href']:
                continue
                
            # Handle HREF being URL-encoded in XML or not
            href_clean = urllib.parse.unquote(res['href'])
            src_file = SOURCE_DIR / href_clean
            
            if not src_file.exists():
                # Try finding it relative to content if implied?
                # Usually href is relative to package root
                print(f"  Missing file: {src_file}")
                continue
                
            page_slug = clean_title(item_title)
            page_filename = f"{i+1:02d}-{page_slug}.html"
            dest_file = mod_dir / page_filename
            
            content_html = process_html_content(src_file, dest_file, 2)
            
            items.append({
                'title': item_title,
                'path': dest_file,
                'rel_path': f"modules/{module_slug}/{page_filename}",
                'filename': page_filename,
                'content': content_html
            })
            
        # Write pages
        for i, item in enumerate(items):
            prev_link = items[i-1]['filename'] if i > 0 else None
            next_link = items[i+1]['filename'] if i < len(items)-1 else None
            
            full_html = create_page(
                item['title'], 
                item['content'], 
                module_title, 
                items, 
                item['filename'], 
                prev_link, 
                next_link
            )
            
            with open(item['path'], 'w', encoding='utf-8') as f:
                f.write(full_html)
                
        modules.append({
            'title': module_title,
            'slug': module_slug,
            'items': items
        })
        
    # Index Generation
    modules_list_html = ""
    for mod in modules:
        if not mod['items']:
            continue
        first_link = mod['items'][0]['rel_path']
        modules_list_html += f"""
        <div class="module-card">
            <h3>{mod['title']}</h3>
            <p>{len(mod['items'])} Topics</p>
            <a href="{first_link}" class="btn">Start Module</a>
        </div>
        """

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ancient World Literature</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="assets/style.css">
</head>
<body class="home-body">
    <header class="main-hero">
        <div class="hero-content">
            <h1>Early World Literature</h1>
            <p>A Journey Through the Classics</p>
            <a href="glossary.html" class="btn btn-hero">View Glossary</a>
        </div>
    </header>
    
    <main class="container">
        <div class="modules-grid">
            {modules_list_html}
        </div>
    </main>
    
    <footer>
        <p>Restored Course Content</p>
    </footer>
</body>
</html>"""

    with open(OUTPUT_DIR / "index.html", 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print("Conversion completed successfully.")

if __name__ == "__main__":
    main()
