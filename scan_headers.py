import re
from pathlib import Path

XML_PATH = Path("text_summary_extracted/word/document.xml")

def main():
    with open(XML_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find headers (w:pStyle w:val="Heading1" or "Heading2")
    # Structure in XML: <w:p ...><w:pPr><w:pStyle w:val="Heading1"/>...</w:pPr><w:r><w:t>Header Text</w:t></w:r></w:p>
    
    # We'll just look for Heading1 and Heading2 styles and extract valid text near them
    # This is a bit rough RegEx for XML but sufficient for scanning structure
    
    # Split by paragraphs
    paragraphs = re.findall(r'<w:p .*?>(.*?)</w:p>', content)
    
    for p in paragraphs:
        is_h1 = 'w:val="Heading1"' in p
        is_h2 = 'w:val="Heading2"' in p
        
        if is_h1 or is_h2:
            # Extract text
            text = "".join(re.findall(r'<w:t[^>]*>(.*?)</w:t>', p))
            level = "H1" if is_h1 else "H2"
            print(f"{level}: {text}")

if __name__ == "__main__":
    main()
