import os
import re
from pathlib import Path

EXTRACTED_DIR = Path("extracted_pages")
MODULES_DIR = Path("site/modules")

# Mapping: Extracted Filename -> Partial Target Filename (to find it)
MAPPING = {
    "Introduction_to_the_Text.html": "introduction-to-the-textbook",
    "Chapter_One__The_Drive.html": "chapter-one-introduction",
    "Hesiod__Works__and_Days.html": "hesiod-works-and-days-background-and-summary",
    "Popol_Vuh.html": "popol-vuh-background-and-summary",
    "Gilgamesh.html": "gilgamesh-background-and-summary",
    "The_Inferno.html": "the-inferno-background-and-summary",
    "Don_Quixote.html": "don-quixote-background-and-summary",
    "The_Iliad.html": "the-iliad-background-and-summary",
    "Bhagavad_Gita.html": "the-bhagavad-gita-background-and-summary",
    "Beowulf.html": "beowulf-background-and-summary",
    "Song_of_Roland.html": "song-of-roland-background-and-summary",
    "Hamlet.html": "hamlet-background-and-summary"
}

def inject_content(target_path, new_content):
    with open(target_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Check if we have the structure
    if '<article class="prose">' not in html:
        print(f"Skipping {target_path} - no prose article found")
        return False

    # Regex to replace content inside <article class="prose">...</article>
    # We want to keep the surrounding divs if possible, but the current content is messy <div> hell.
    # The new content is clean <p>s.
    # Let's replace the innerHTML of article.prose entirely.
    
    pattern = r'(<article class="prose">)(.*?)(</article>)'
    
    # We want to preserve the sidebar, header, footer.
    # The regex dot does not match newlines by default, so use re.DOTALL
    
    def replacer(match):
        return f'{match.group(1)}\n{new_content}\n{match.group(3)}'
    
    new_html = re.sub(pattern, replacer, html, flags=re.DOTALL)
    
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    return True

def main():
    if not EXTRACTED_DIR.exists():
        print("Extracted dir not found")
        return

    count = 0
    for extracted_file in EXTRACTED_DIR.glob("*.html"):
        filename = extracted_file.name
        if filename in MAPPING:
            target_key = MAPPING[filename]
            
            # Find the actual target file in site/modules/
            # It could be in any subdirectory
            target_file_path = None
            for root, dirs, files in os.walk(MODULES_DIR):
                for file in files:
                    if target_key in file:
                        target_file_path = Path(root) / file
                        break
                if target_file_path:
                    break
            
            if target_file_path:
                print(f"Injecting {filename} -> {target_file_path}")
                with open(extracted_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if inject_content(target_file_path, content):
                    count += 1
            else:
                print(f"Target file not found for {target_key}")
        else:
            print(f"No mapping for {filename}")

    print(f"Injected {count} pages.")

if __name__ == "__main__":
    main()
