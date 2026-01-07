
import os
import re

root_dir = r"c:\Users\rober\.gemini\antigravity\scratch\ancient-literature\modules"

# Regex to find links ending in "Professor's Analysis" with text before it
# Matches: <a href="...">Some Title: Professor's Analysis</a>
# Replaces with: <a href="...">Professor's Analysis</a>
# We must capture the opening tag to preserve href and class
pattern = re.compile(r'(<a\s+href="[^"]+"\s*[^>]*>).*?:\s*Professor\'s Analysis</a>', re.IGNORECASE)

def clean_sidebar(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check if the file needs changes
        new_content = pattern.sub(r'\1Professor\'s Analysis</a>', content)
        
        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated: {file_path}")
            return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return False

count = 0
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith(".html"):
            if clean_sidebar(os.path.join(dirpath, filename)):
                count += 1

print(f"Total files updated: {count}")
