
import os
import re

root_dir = r"c:\Users\rober\.gemini\antigravity\scratch\ancient-literature"

youtube_regex = re.compile(r'(youtube\.com/embed/[\w-]+|youtu\.be/[\w-]+|youtube\.com/watch\?v=[\w-]+)')
citation_regex = re.compile(r'(Work\s+Cited|Bibliography|References|Cited)', re.IGNORECASE)

video_links = set()
potential_citations = []

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith(".html"):
            file_path = os.path.join(dirpath, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                    # Find Videos
                    matches = youtube_regex.findall(content)
                    for match in matches:
                        video_links.add(match)
                        
                    # Find potential Citation Context (naive check)
                    # We might just look for lines that look like citations later, 
                    # but knowing which files have "Works Cited" sections is helpful.
                    if citation_regex.search(content):
                        potential_citations.append(file_path)

            except Exception as e:
                print(f"Error reading {file_path}: {e}")

print("--- FOUND VIDEOS ---")
for link in sorted(video_links):
    print(link)

print("\n--- FILES WITH POTENTIAL CITATIONS ---")
for path in sorted(potential_citations):
    print(path)
