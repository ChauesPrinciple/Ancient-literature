
import os

root_dir = r"c:\Users\rober\.gemini\antigravity\scratch\ancient-literature"

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith(".html"):
            file_path = os.path.join(dirpath, filename)
            
            # Read file content
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Check if Video Gallery link exists and References link doesn't
            if "video_gallery.html" in content and "references.html" not in content and "References" not in content:
                print(f"Updating {file_path}")
                
                # Determine relative path prefix
                # If file is 'references.html', don't link to itself self-referentially or careful with path
                if filename == "references.html":
                    continue # Skip the references file itself or handle specifically? It lists itself in active link?
                             # The newly created references.html already has the link hardcoded active.
                
                # We search for the line with Video Gallery
                # <a href="../../video_gallery.html">Video Gallery</a>
                # or <a href="video_gallery.html">Video Gallery</a>
                
                # Let's find the closing of Video Gallery link or just append after it
                # Logic: Find 'Video Gallery</a>' and append '\n                    <a href="{prefix}references.html">References</a>'
                
                # Determining prefix based on file depth relative to root
                rel_path = os.path.relpath(file_path, root_dir)
                depth = rel_path.count(os.sep)
                
                if depth == 0:
                    prefix = ""
                else:
                    prefix = "../" * depth
                
                # Finding insertion point
                target_str = "Video Gallery</a>"
                insertion_point = content.find(target_str)
                
                if insertion_point != -1:
                    insert_idx = insertion_point + len(target_str)
                    new_link = f'\n                    <a href="{prefix}references.html">References</a>'
                    
                    new_content = content[:insert_idx] + new_link + content[insert_idx:]
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                else:
                    print(f"Warning: 'Video Gallery' link not found in {filename}")

print("Global sidebar update complete.")
