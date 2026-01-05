import re
import os
from pathlib import Path

# Combine parts
DUMP_FILES = ["analysis_dump_part1.txt", "analysis_dump_part2.txt", "analysis_dump_part3.txt"]
FULL_DUMP = "analysis_dump_full.txt"
MODULES_DIR = Path("site/modules")

# Mapping Title to Partial Filename matches
MAPPING = {
    "Tablet of Gilgamesh": "gilgamesh-professors-analysis",
    "Gilgamesh": "gilgamesh-professors-analysis",
    "The Inferno": "the-inferno-professors-analysis",
    "Don Quixote": "don-quixote-professors-analysis",
    "The Iliad": "the-iliad-professors-analysis",
    "The Bhagavad Gita": "bhagavad-ghita-professors-analysis",
    "Beowulf": "beowulf-professors-analysis",
    "The Song of Roland": "song-of-roland-professors-analysis",
    "Hamlet": "hamlet-professors-analysis",
    "Medea": "medea-professors-analysis",
    "One Thousand and One Nights": "one-thousand-and-one-nights",
    "The Wife of Bath's Prologue and Tale": "wife-of-bath",
    "The Book of the City of Ladies": "book-of-the-city-of-ladies",
    "Theory": "chapter-two-introduction"
}

def clean_content(text):
    image_descriptions = [
        "Picture of the outer wall",
        "Ancient clay tablet",
        "Engraving of a demon",
        "A man on horseback",
        "A Bust of Homer",
        "An illustrated manuscript",
        "A Picture of a Historical",
        "The Oldest Edition of Beowulf",
        "The Battle of Roncevaux",
        "The First Folio of Hamlet",
        "Manuscript of Medea",
        "An Arabic Manuscript",
        "A Middle English Edition",
        "An Illustrated Page"
    ]

    # Remove BOM and common artifacts
    text = text.replace(u'\ufeff', '')
    
    lines = text.split('\n')
    html = ""
    in_list = False
    in_definition_list = False
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines
        if not line:
            if in_list:
                html += "</ol>\n"
                in_list = False
            if in_definition_list:
                html += "</dl>\n"
                in_definition_list = False
            i += 1
            continue
            
        # Strip inline styles and Word artifacts
        line = re.sub(r' style="[^"]*"', '', line)
        line = re.sub(r' class="[^"]*"', '', line)
        line = re.sub(r'<span>(.*?)</span>', r'\1', line)
        
        # Filter unwanted text
        if "Broken image link" in line:
            i += 1
            continue
        if line.startswith("Separator"):
             i += 1
             continue
        if line.startswith("(this link opens"):
             i += 1
             continue

        # Video embedding
        if line.startswith("iframe") or line.startswith("<iframe"):
            html += f'<div class="video-wrapper">{line}</div>\n'
            i += 1
            continue
            
        # Meta notes
        if line == "Includes assessment.":
             html += f'<p class="meta-note"><em>{line}</em></p>\n'
             i += 1
             continue
        if line.startswith("Note:"):
             html += f'<p class="note">{line}</p>\n'
             i += 1
             continue
             
        # Image Placeholders
        is_image = False
        for desc in image_descriptions:
            if desc in line:
                html += f'<div class="image-placeholder" style="background:#f9f9f9; padding:1.5rem; text-align:center; margin:1.5rem 0; border:2px dashed #ccc; color:#666;"><em>[Image Intended: {line}]</em></div>\n'
                is_image = True
                break
        if is_image:
            i += 1
            continue
             
        # Ordered Lists (1. Item)
        if line[0].isdigit() and (line[1] == '.' or line[1] == ')'):
             if not in_list:
                 if in_definition_list:
                     html += "</dl>\n"
                     in_definition_list = False
                 html += "<ol>\n"
                 in_list = True
             html += f"<li>{line[2:].strip()}</li>\n"
             i += 1
             continue
        elif in_list:
             html += "</ol>\n"
             in_list = False

        # Definition Lists transformation
        if i + 1 < len(lines):
            next_line = lines[i+1].strip()
            if len(line.split()) < 10 and (next_line.startswith("E.g.") or next_line.startswith("e.g.")):
                if not in_definition_list:
                    html += "<dl>\n"
                    in_definition_list = True
                html += f"<dt><strong>{line}</strong></dt>\n"
                html += f"<dd>{next_line}</dd>\n"
                i += 2
                continue
        
        if in_definition_list:
             html += "</dl>\n"
             in_definition_list = False
             
        # Standard Paragraph
        if line.startswith("<p"):
            html += f"{line}\n"
        else:
            html += f"<p>{line}</p>\n"
        i += 1
             
    if in_list:
        html += "</ol>\n"
    if in_definition_list:
        html += "</dl>\n"
        
    return html

def combine_dumps():
    with open(FULL_DUMP, 'w', encoding='utf-8') as outfile:
        for fname in DUMP_FILES:
            if os.path.exists(fname):
                with open(fname, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write("\n\n")

def main():
    combine_dumps()
    
    with open(FULL_DUMP, 'r', encoding='utf-8') as f:
        data = f.read()
        
    chunks = data.split("(this link opens in a new window/tab)")
    
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
            
        lines = chunk.split('\n')
        
        # Check matching
        title = None
        target_key = None
        found_title_line = -1
        
        header_lines = lines[:20]
        
        for i, line in enumerate(header_lines):
            line = line.strip()
            for map_title in MAPPING:
                if len(line) < 100 and map_title in line:
                    title = map_title
                    target_key = MAPPING[map_title]
                    found_title_line = i
                    break
            if title:
                break
        
        if not title:
             for i, line in enumerate(header_lines):
                if "Gilgamesh" in line and "Tablet" in line:
                    title = "Tablet of Gilgamesh"
                    target_key = MAPPING["Tablet of Gilgamesh"]
                    found_title_line = i
                    break
        
        if target_key:
            pre_title_lines = lines[:found_title_line]
            post_title_lines = lines[found_title_line+1:]
            
            all_lines = pre_title_lines + post_title_lines
            filtered_lines = []
            for l in all_lines:
                s = l.strip()
                if not s: continue
                if s in ["Analysis", "Analysis:", "Professor's Analysis"]:
                    continue
                filtered_lines.append(l)

            content_text = "\n".join(filtered_lines)
            
            html_content = f"<h2>{title} Analysis</h2>\n" + clean_content(content_text)
            
            target_file = None
            for root, dirs, files in os.walk(MODULES_DIR):
                for file in files:
                    if target_key in file and file.endswith(".html"):
                        target_file = Path(root) / file
                        break
                if target_file:
                    break
                    
            if target_file:
                print(f"Injecting Analysis into {target_file}")
                with open(target_file, 'r', encoding='utf-8') as f:
                    file_html = f.read()
                
                match = re.search(r'(<article class="prose">)(.*?)(</article>)', file_html, re.DOTALL)
                if match:
                    current_body = match.group(2)
                    
                    # PREVENT DUPLICATION
                    discussion_part = ""
                    
                    if "<hr class='analysis-discussion-separator'>" in current_body:
                        parts = current_body.split("<hr class='analysis-discussion-separator'>")
                        if len(parts) > 1:
                            discussion_part = parts[1]
                    elif "<hr class='discussion-separator'>" in current_body:
                        parts = current_body.split("<hr class='discussion-separator'>")
                        if len(parts) > 1:
                            discussion_part = parts[1]
                    elif "Includes assessment." in current_body and "Reflect & Discuss" in current_body:
                        pass

                    # CHECK IF DISCUSSION IS JUST A DUPE OF ANALYSIS
                    # Use a generous slice or startswith
                    stripped_disc = discussion_part.strip()
                    if stripped_disc.startswith(f"<h2>{title} Analysis</h2>"):
                        print(f"  Detected duplicate analysis in 'discussion' section of {target_file.name}. Removing dupe.")
                        discussion_part = ""
                    elif f"<h2>{title} Analysis</h2>" in stripped_disc[:1000]:
                         print(f"  Detected duplicate analysis in 'discussion' section of {target_file.name}. Removed (embedded check).")
                         discussion_part = ""

                    new_full_body = html_content
                    if discussion_part.strip():
                         new_full_body = new_full_body + "\n<hr class='analysis-discussion-separator'>" + discussion_part
                    
                    final_html = file_html.replace(match.group(0), f'{match.group(1)}\n{new_full_body}\n{match.group(3)}')
                    
                    with open(target_file, 'w', encoding='utf-8') as f:
                        f.write(final_html)
                        
        else:
            print(f"Skipping unmapped chunk")

if __name__ == "__main__":
    main()
