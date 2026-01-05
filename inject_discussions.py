import re
import os
from pathlib import Path

DUMP_PATH = Path("discussion_dump.txt")
MODULES_DIR = Path("site/modules")

# Mapping Title to Partial Filename matches
MAPPING = {
    "Introductions!": "ice-breaker-discussion", # Actually "Ice Breaker" is separate below?
    # Wait, the dump has "Introductions!" AND "Ice Breaker Discussion".
    # Introductions! is likely 04-ice-breaker... or maybe introduced in 01?
    # Let's map "Ice Breaker Discussion" to 04-ice-breaker
    # And "Introductions!" might be part of it or another file.
    # checking file list: 04-ice-breaker-discussion.html is the only likely candidate in Module 1.
    # Maybe "Introductions!" is the prompt for the forum, and Ice Breaker is another.
    # Let's try to find if there is another file.
    # convert_course.py generated: 04-ice-breaker-discussion.html
    # content likely combines them.
   
    "Ice Breaker Discussion": "ice-breaker-discussion",
    "Hero Systems": "hero-systems", # 05-hero-systems.html
    "Betrayal and Rage": "the-iliad-professors-analysis", # This is Iliad analysis? 
    # User said: "In the introduction to chapter two... I attempt to provide a representation... Greek tragedy, like the **Iliad**"
    # But Iliad is module 6?
    # "Betrayal and Rage" might be the TITLE of the analysis for Iliad.
    # Let's map it to Iliad.
    
    "Credit to the Women": "medea", # Medea? Or maybe unrelated. Mentions "Birka Viking...". 
    # "In our analysis of **Medea**..." is in a DIFFERENT section later.
    # "Credit to the Women" might be "The Woman" chapter intro?
    # Or maybe "Book of the City of Ladies"?
    # Wait, look at "Book of the City of Ladies" section.
    # "Credit to the Women" discusses "prominent women".
    # This might be Module 3? "The Woman" chapter.
    
    "Creation and Cosmos Quick Take": "creation-and-cosmos-quick-take",
    "Gilgamesh": "gilgamesh-professors-analysis",
    "The Inferno": "the-inferno-professors-analysis",
    "Don Quixote": "don-quixote-professors-analysis",
    "The Iliad": "the-iliad-professors-analysis", # Wait, is Betrayal and Rage different? 
    # "The Iliad" section explicitly says "The Iliad... Includes assessment".
    # "Betrayal and Rage" says "includes assessment".
    # Maybe "Betrayal and Rage" is Chapter 2 Intro?
    # Chapter 2 is "The Warrior".
    
    "Bhagavad Ghita": "bhagavad-ghita-professors-analysis", 
    "Beowulf": "beowulf-professors-analysis",
    "Song of Roland": "song-of-roland-professors-analysis",
    "Hamlet": "hamlet-professors-analysis",
    "Medea": "medea-professors-analysis",
    "One Thousand and One Nights": "one-thousand-and-one-nights", # finding distinct file might be tricky
    # File list: 04-one-thousand-and-one-nights.html ? No, let's search.
    
    "Wife of Bath": "wife-of-bath", # 04-wife-of-bath...
    "Book of the City of Ladies": "book-of-the-city-of-ladies"
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
            
        if line.startswith("iframe"):
            # It's an iframe tag (I stripped brackets in the dump? No, I added them in the dump file write)
            # Wait, the dump file write had <iframe ...> 
            # so it should come through.
            html += line + "\n"
        elif line.startswith("<iframe"):
            html += f'<div class="video-wrapper">{line}</div>\n'
        elif line.startswith("Separator"):
            continue
        elif line == "Includes assessment.":
             html += f'<p class="meta-note"><em>{line}</em></p>\n'
        elif line.startswith("Note:"):
             html += f'<p class="note">{line}</p>\n'
        elif line[0].isdigit() and (line[1] == '.' or line[1] == ')'):
             # Ordered list
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

def inject_content(target_key, content):
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
        print(f"Could not find file for {target_key}")
        return

    print(f"Injecting into {target_file}")
    
    with open(target_file, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Replace Prose
    # Note: We want to keep the Title header usually inside main but outside article?
    # The convert script put <h2>Title</h2> inside header.
    # The article has the content.
    
    pattern = r'(<article class="prose">)(.*?)(</article>)'
    
    def replacer(match):
        return f'{match.group(1)}\n{content}\n{match.group(3)}'
    
    new_html = re.sub(pattern, replacer, html, flags=re.DOTALL)
    
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(new_html)

def main():
    with open(DUMP_PATH, 'r', encoding='utf-8') as f:
        data = f.read()
        
    # Split by "Separator"
    chunks = data.split("Separator")
    
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
            
        lines = chunk.split('\n')
        title = lines[0].strip()
        
        # Check mapping
        if title in MAPPING:
            # content is the rest
            content_text = "\n".join(lines[1:])
            html_content = clean_content(content_text)
            
            # Additional HTML Formatting for specific things
            inject_content(MAPPING[title], html_content)
        else:
            print(f"Unmapped Title: {title}")

if __name__ == "__main__":
    main()
