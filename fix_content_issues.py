import os
import re

def fix_content_issues():
    base_dir = r"C:\Users\rober\.gemini\antigravity\scratch\ancient-literature\modules"
    
    # --- Module 1: Remove Ice Breaker ---
    mod1_dir = os.path.join(base_dir, "module-1-introductions")
    ice_breaker_file = os.path.join(mod1_dir, "04-ice-breaker-discussion.html")
    
    if os.path.exists(ice_breaker_file):
        print(f"Deleting {ice_breaker_file}...")
        os.remove(ice_breaker_file)
    else:
        print("Ice Breaker file not found (already deleted?)")

    # Update Module 1 links
    print("Updating Module 1 links...")
    for root, dirs, files in os.walk(mod1_dir):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                orig_content = content
                
                # 1. Remove Sidebar Link
                # <a href="04-ice-breaker-discussion.html">Ice Breaker Discussion</a>
                content = re.sub(r'<a\s+href="04-ice-breaker-discussion\.html">[^<]*Ice Breaker[^<]*</a>', '', content, flags=re.IGNORECASE)
                
                # 2. Fix Footer in 03 (Next -> 05)
                if file == "03-chapter-one-introduction-the-drive.html":
                     content = re.sub(r'<a\s+href="04-ice-breaker-discussion\.html"\s+class="nav-btn next">[^<]*Next[^<]*</a>', 
                                      '<a href="05-hero-systems.html" class="nav-btn next">Next →</a>', content)

                # 3. Fix Footer in 05 (Prev -> 03)
                if file == "05-hero-systems.html":
                     content = re.sub(r'<a\s+href="04-ice-breaker-discussion\.html"\s+class="nav-btn prev">[^<]*Previous[^<]*</a>', 
                                      '<a href="03-chapter-one-introduction-the-drive.html" class="nav-btn prev">← Previous</a>', content)

                if content != orig_content:
                    print(f"Updated {file}")
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)

    # --- Module 6: Rename and Fix Iliad ---
    mod6_dir = os.path.join(base_dir, "module-6-the-iliad")
    old_iliad_path = os.path.join(mod6_dir, "06-the-iliad.html")
    new_iliad_path = os.path.join(mod6_dir, "06-poem-of-force.html")
    
    if os.path.exists(old_iliad_path):
        print(f"Renaming {old_iliad_path} to {new_iliad_path}...")
        os.rename(old_iliad_path, new_iliad_path)
    
    # Update Module 6 links (including in the newly renamed file)
    print("Updating Module 6 links...")
    # Need to re-scan directory since we renamed a file
    for root, dirs, files in os.walk(mod6_dir):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                orig_content = content
                
                # 1. Update Sidebar Link
                # <a href="06-the-iliad.html">The Iliad</a> -> <a href="06-poem-of-force.html">Perspectives on Force</a>
                # Using broad regex to catch active state too
                
                # Pattern: <a href="06-the-iliad.html" (opt class)>The Iliad</a>
                # Replacement: <a href="06-poem-of-force.html" (opt class)>Perspectives on Force</a>
                
                # We do this in two steps to preserve class="active-link" if present
                
                # Step A: Replace href
                content = content.replace('href="06-the-iliad.html"', 'href="06-poem-of-force.html"')
                
                # Step B: Replace Link Text (specifically for this file's link)
                # This is tricky because "The Iliad" is used for 04 as well.
                # We need to target the link that points to 06-poem-of-force.html (which we just updated)
                
                # Find: <a href="06-poem-of-force.html"(.*?)>The Iliad</a>
                # Sub: <a href="06-poem-of-force.html"\1>Perspectives on Force</a>
                content = re.sub(r'(<a\s+href="06-poem-of-force\.html"[^>]*>)The Iliad</a>', r'\1Perspectives on Force</a>', content)

                # 2. Fix Page Title/Header if we are processing the renamed file itself
                if file == "06-poem-of-force.html":
                    content = content.replace('<title>The Iliad | Ancient Literature</title>', '<title>Perspectives on Force | Ancient Literature</title>')
                    content = content.replace('<h2>The Iliad</h2>', '<h2>Perspectives on Force</h2>')

                if content != orig_content:
                    print(f"Updated {file}")
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)

if __name__ == "__main__":
    fix_content_issues()
