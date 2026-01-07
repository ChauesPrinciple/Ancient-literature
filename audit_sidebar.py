
import os
import re

root_dir = r"c:\Users\rober\.gemini\antigravity\scratch\ancient-literature\modules"

# Regex to capture the text content of links that *might* be the analysis page
# We look for "Analysis" in the link text
pattern = re.compile(r'<a\s+href="[^"]+"\s*[^>]*>(.*?[Aa]nalysis.*?)</a>', re.IGNORECASE)

print("Scanning for sidebar links containing 'Analysis'...")
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith(".html"):
            file_path = os.path.join(dirpath, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    matches = pattern.findall(content)
                    for match in matches:
                        # Print occurrences that are NOT just "Professor's Analysis"
                        if match.strip() != "Professor's Analysis":
                            print(f"{os.path.basename(dirpath)}/{filename}: '{match.strip()}'")
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
