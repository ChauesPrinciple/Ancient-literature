import re
import os
from pathlib import Path

XML_PATH = Path("video_supp_extracted/word/document.xml")
OUTPUT_PATH = Path("site/video_gallery.html")

def main():
    if not XML_PATH.exists():
        print(f"Error: {XML_PATH} not found.")
        return

    with open(XML_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # The DOCX seems to have text followed by hyperlinks.
    # Pattern: Text description ... <w:hyperlink ...><w:t>URL</w:t></w:hyperlink>
    # or just paragraphs with links.
    
    # Let's extract all paragraphs
    paragraphs = re.findall(r'<w:p .*?>(.*?)</w:p>', content)
    
    videos = []
    current_category = "General"
    
    for p in paragraphs:
        # Get text
        text_nodes = re.findall(r'<w:t[^>]*>(.*?)</w:t>', p)
        full_text = "".join(text_nodes).strip()
        
        # Check for hyperlink
        # Hyperlinks are usually in <w:hyperlink ...> <w:r> <w:t>url</w:t> ...
        # But sometimes the relationship ID is used.
        # However, the previous view_file showed the URL literally in the text node often, or in r:id lookup.
        # But wait, lines 37+: <w:hyperlink r:id="rId4" ...><w:t>https://www.youtube.com...</w:t>
        # So the URL IS in the text node inside the hyperlink tag.
        
        # Extract URL
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', full_text)
        
        if urls:
            url = urls[0]
            # Clean text (remove URL from description)
            description = full_text.replace(url, "").replace("Link", "").strip()
            if not description:
                description = "Video Resource"
            
            # YouTube embed
            # convert watch?v=ID to embed/ID
            if "youtube.com/watch?v=" in url:
                vid_id = url.split("v=")[1].split("&")[0]
                embed_url = f"https://www.youtube.com/embed/{vid_id}"
                videos.append({
                    "type": "video",
                    "url": embed_url,
                    "link": url,
                    "desc": description,
                    "category": current_category
                })
        else:
            # Maybe it's a category header?
            if len(full_text) < 50 and full_text.strip():
                current_category = full_text.strip(": ")

    # Generate HTML
    gallery_html = ""
    last_cat = ""
    
    for v in videos:
        if v['category'] != last_cat:
            gallery_html += f'<h2 class="video-category">{v["category"]}</h2>'
            last_cat = v['category']
            
        gallery_html += f"""
        <div class="video-card">
            <h3>{v['desc']}</h3>
            <div class="video-wrapper">
                <iframe src="{v['url']}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
            </div>
            <p><a href="{v['link']}" target="_blank">Watch on YouTube</a></p>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Gallery | Ancient Literature</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="assets/style.css">
    <style>
        .video-category {{
            margin-top: 3rem;
            margin-bottom: 1.5rem;
            border-bottom: 1px solid var(--accent-gold);
            padding-bottom: 0.5rem;
        }}
        .video-card {{
            background: #fff;
            padding: 1.5rem;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            margin-bottom: 2rem;
        }}
        .video-wrapper {{
            position: relative;
            padding-bottom: 56.25%; /* 16:9 */
            height: 0;
            overflow: hidden;
            margin: 1rem 0;
        }}
        .video-wrapper iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }}
    </style>
</head>
<body>
    <div class="layout">
        <aside class="sidebar">
            <div class="brand">
                <h1>Ancient<br>Literature</h1>
            </div>
            <nav>
                <a href="index.html" class="home-link">← Course Home</a>
                <div class="current-module">
                    <h3>Resources</h3>
                </div>
                <div class="module-nav">
                    <a href="glossary.html">Glossary</a>
                    <a href="video_gallery.html" class="active-link">Video Gallery</a>
                </div>
            </nav>
        </aside>
        
        <main class="content-area">
            <header class="page-header">
                <h2>Video Gallery</h2>
            </header>
            
            <article class="prose">
                {gallery_html}
            </article>
        </main>
    </div>
</body>
</html>"""

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Video gallery generated with {len(videos)} videos.")

if __name__ == "__main__":
    main()
