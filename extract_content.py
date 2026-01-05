import re
import os
import shutil
from pathlib import Path

# Paths
XML_PATH = Path("text_summary_extracted/word/document.xml")
MEDIA_SRC_DIR = Path("text_summary_extracted/word/media")
SITE_MEDIA_DIR = Path("site/assets/media")
OUTPUT_DIR = Path("extracted_pages")

def clean_xml_tag(text):
    # Remove all tags except maybe bold/italic if we were fancy, but for now strip all
    # actually we want to keep some formatting if possible.
    # But simple regex strip is safer for now.
    return re.sub(r'<[^>]+>', '', text)

def process_text_run(run_xml):
    # Check for bold, italic
    text = "".join(re.findall(r'<w:t[^>]*>(.*?)</w:t>', run_xml))
    if not text:
        return ""
    
    # Very basic styling
    if '<w:b/>' in run_xml:
        text = f"<strong>{text}</strong>"
    if '<w:i/>' in run_xml:
        text = f"<em>{text}</em>"
        
    return text

def main():
    if not SITE_MEDIA_DIR.exists():
        SITE_MEDIA_DIR.mkdir(parents=True)
    if not OUTPUT_DIR.exists():
        OUTPUT_DIR.mkdir()

    with open(XML_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split paragraphs
    # <w:p> ... </w:p>
    paragraphs = re.findall(r'<w:p .*?>(.*?)</w:p>', content)
    
    current_section_title = "Unknown"
    current_content = ""
    sections = {}
    
    image_counter = 0

    for p in paragraphs:
        # Check for headers
        is_h1 = 'w:val="Heading1"' in p
        is_h2 = 'w:val="Heading2"' in p
        
        # Extract text components (runs)
        # We need to preserve order of runs
        # Use a more comprehensive regex to find text <w:t ...>...</w:t> inside runs
        
        # Get all runs
        runs = re.findall(r'<w:r[ >].*?</w:r>', p)
        para_text = ""
        full_text_only = ""
        
        for r in runs:
             t = process_text_run(r)
             para_text += t
             full_text_only += clean_xml_tag(t)
        
        full_text_only = full_text_only.strip()
        
        # Handle images
        drawings = re.findall(r'<w:drawing>(.*?)</w:drawing>', p)
        for d in drawings:
            # We don't have the relationship map, but we can look for the descriptive text or just a placeholder
            para_text += "<!-- [IMAGE INTENDED HERE] -->"

        if is_h1:
            # Save previous section
            if current_content.strip():
                sections[current_section_title] = current_content
            
            # Start new section
            # Normalize title
            if full_text_only:
                current_section_title = full_text_only
                # Handle special case where title might be split or partial
                # Manual fixes for known weird titles
                if "Introduction" in current_section_title and "Text" in current_section_title:
                   current_section_title = "Introduction to the Text"
                
                current_content = f"<h1>{current_section_title}</h1>\n"
                print(f"Found Section: {current_section_title}")
            
        elif is_h2:
            if full_text_only:
                 current_content += f"<h2>{full_text_only}</h2>\n"
        else:
            if para_text.strip():
                current_content += f"<p>{para_text}</p>\n"

    # Save last
    if current_content.strip():
        sections[current_section_title] = current_content
        
    # Write to files
    for title, html in sections.items():
        # Clean filename
        safe_title = "".join([c if c.isalnum() else "_" for c in title])
        file_path = OUTPUT_DIR / f"{safe_title}.html"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
            
    print(f"Extracted {len(sections)} sections.")

if __name__ == "__main__":
    main()
