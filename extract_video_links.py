
import re

with open(r"c:\Users\rober\.gemini\antigravity\scratch\ancient-literature\video_gallery.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find all youtube links (embeds and watch links)
# We want the ID to construct a reliable list
ids = set()
matches = re.findall(r'(?:youtube\.com/embed/|youtu\.be/|youtube\.com/watch\?v=)([\w-]+)', content)
for m in matches:
    ids.add(m)

print(f"Found {len(ids)} unique video IDs.")
for vid_id in ids:
    print(f"https://www.youtube.com/watch?v={vid_id}")
