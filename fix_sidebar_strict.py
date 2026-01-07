
import os
import re

root_dir = r"c:\Users\rober\.gemini\antigravity\scratch\ancient-literature\modules"

# This regex is aggressive: it finds any link that ends with "Analysis</a>" 
# and replaces the inner text with "Professor's Analysis" matches:
# <a href="...">Medea: Professor's Analysis</a>
# <a href="...">Don Quixote Analysis</a>
# <a href="...">Professor's Analysis</a>
#
# It preserves the opening tag attributes.
pattern = re.compile(r'(<a\s+href="[^"]+"\s*[^>]*>).*?[Aa]nalysis.*?</a>', re.IGNORECASE)

def fix_sidebar(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Don't change the "Literary Analysis Essay" link in Module 15
        # We can exclude that specific file or pattern if needed, but the regex above 
        # might catch "Literary Analysis Topic Proposal" or "Literary Analysis Essay".
        # We must be careful!
        
        # Refined strategy: Only target the "Professor's Analysis" links which usually point to specific files
        # or are the FIRST link in the nav often.
        # SAFEGUARD: The user specifically complained about "Title: Professor's Analysis" or "Title Analysis".
        # Let's iterate line by line or match specific known bad patterns if possible?
        # No, a regex replace is best but we need to EXCLUDE valid other analysis links.
        
        # Valid exclusions:
        # "Literary Analysis Essay" (Module 15)
        # "Literary Analysis Topic Proposal" (Module 11 - deleted now)
        
        # Let's use a callback to check the content before replacing
        def replace_callback(match):
            full_match = match.group(0)
            opening_tag = match.group(1)
            inner_text = match.group(0).replace(opening_tag, "").replace("</a>", "")
            
            if "Literary Analysis" in inner_text:
                return full_match # Skip these
            
            return f"{opening_tag}Professor's Analysis</a>"

        new_content = pattern.sub(replace_callback, content)

        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Fixed: {os.path.basename(file_path)}")
            return True
    except Exception as e:
        print(f"Error {file_path}: {e}")
    return False

count = 0
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith(".html"):
            if fix_sidebar(os.path.join(dirpath, filename)):
                count += 1

print(f"Total files fixed: {count}")
