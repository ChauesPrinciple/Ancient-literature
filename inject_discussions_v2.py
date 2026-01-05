import re
import os
from pathlib import Path

DUMP_PATH = Path("discussion_dump.txt")
MODULES_DIR = Path("site/modules")

# Mapping Title to Partial Filename matches
MAPPING = {
    "Introductions!": "ice-breaker-discussion",
    "Ice Breaker Discussion": "ice-breaker-discussion",
    "Hero Systems": "hero-systems", 
    "Betrayal and Rage": "chapter-two-introduction", # Corrected to Intro
    "Credit to the Women": "chapter-three-introduction", # Corrected to Intro
    "The Final Chapter": "the-final-chapter",
    "Creation and Cosmos Quick Take": "creation-and-cosmos-quick-take",
    "Gilgamesh": "gilgamesh-professors-analysis",
    "The Inferno": "the-inferno-professors-analysis",
    "Don Quixote": "don-quixote-professors-analysis",
    "The Iliad": "the-iliad-professors-analysis",
    "Bhagavad Ghita": "bhagavad-ghita-professors-analysis",
    "Beowulf": "beowulf-professors-analysis",
    "Song of Roland": "song-of-roland-professors-analysis",
    "Hamlet": "hamlet-professors-analysis",
    "Medea": "medea-professors-analysis",
    "One Thousand and One Nights": "one-thousand-and-one-nights", # Partial match
    "Wife of Bath": "wife-of-bath",
    "Book of the City of Ladies": "book-of-the-city-of-ladies",
    "Anthology Project": "anthology-project" # User mentioned peer work?
}

def clean_content(text):
    # Convert text to HTML paragraphs
    lines = text.split('\n')
    html = ""
    in_list = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith("iframe") or line.startswith("<iframe"):
            html += f'<div class="video-wrapper">{line}</div>\n'
        elif line.startswith("Separator"):
            continue
        elif line == "Includes assessment.":
             html += f'<p class="meta-note"><em>{line}</em></p>\n'
        elif line.startswith("Note:"):
             html += f'<p class="note">{line}</p>\n'
        elif line[0].isdigit() and (line[1] == '.' or line[1] == ')'):
             if not in_list:
                 html += "<ol>\n"
                 in_list = True
             html += f"<li>{line[2:].strip()}</li>\n"
        elif in_list and not (line[0].isdigit() and (line[1] == '.' or line[1] == ')')):
             html += "</ol>\n"
             in_list = False
             html += f"<p>{line}</p>\n"
        else:
             html += f"<p>{line}</p>\n"
             
    if in_list:
        html += "</ol>\n"
    return html

def main():
    with open(DUMP_PATH, 'r', encoding='utf-8') as f:
        data = f.read()
        
    chunks = data.split("Separator")
    
    # Aggregate content by Target Key
    content_map = {}
    
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
            
        lines = chunk.split('\n')
        title = lines[0].strip()
        
        target_key = None
        # Find mapping
        if title in MAPPING:
            target_key = MAPPING[title]
        else:
            # Maybe partial matching?
            pass
            
        if target_key:
            content_text = "\n".join(lines[1:])
            html_content = f"<h2>{title}</h2>\n" + clean_content(content_text)
            
            if target_key not in content_map:
                content_map[target_key] = []
            content_map[target_key].append(html_content)
        else:
            print(f"Skipping unmapped title: {title}")

    # Inject
    for target_key, content_list in content_map.items():
        # Find file
        target_file = None
        for root, dirs, files in os.walk(MODULES_DIR):
            for file in files:
                if target_key in file and file.endswith(".html"):
                    target_file = Path(root) / file
                    break
            if target_file:
                break
                
        if not target_file:
            print(f"File not found for key: {target_key}")
            continue
            
        full_content = "\n<hr class='discussion-separator'>\n".join(content_list)
        
        print(f"Injecting into {target_file}")
        with open(target_file, 'r', encoding='utf-8') as f:
            html = f.read()
            
        pattern = r'(<article class="prose">)(.*?)(</article>)'
        def replacer(match):
            return f'{match.group(1)}\n{full_content}\n{match.group(3)}'
        
        new_html = re.sub(pattern, replacer, html, flags=re.DOTALL)
        
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(new_html)

if __name__ == "__main__":
    main()
