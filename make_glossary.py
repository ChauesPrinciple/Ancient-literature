import re
import os
from pathlib import Path

# Input file
XML_PATH = Path("terms_extracted/word/document.xml")
OUTPUT_PATH = Path("site/glossary.html")

def clean_xml_tag(text):
    return re.sub(r'<[^>]+>', '', text)

def main():
    if not XML_PATH.exists():
        print(f"Error: {XML_PATH} not found.")
        return

    with open(XML_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # The XML structure for paragraphs is <w:p> ... </w:p>
    # Inside we have runs <w:r> ... </w:r> and text <w:t>Text</w:t>
    # We will try to extract all text from each paragraph and see if it looks like a term.
    
    # Split by paragraphs
    paragraphs = re.findall(r'<w:p.*?>(.*?)</w:p>', content)
    
    terms = []
    
    for p in paragraphs:
        # Extract all text nodes
        text_nodes = re.findall(r'<w:t[^>]*>(.*?)</w:t>', p)
        full_text = "".join(text_nodes).strip()
        
        # skip empty or boring lines
        if not full_text or "Work Cited" in full_text or "Literary Terms" == full_text:
            continue
            
        # Heuristic: Terms usually start with the term name followed by ":" or just the description
        # In the file viewed, it looks like: "Abject: Abject is defined as..."
        # or "Allegory: A literary mode..."
        
        # Let's try to split by colon
        if ":" in full_text:
            parts = full_text.split(":", 1)
            term = parts[0].strip()
            definition = parts[1].strip()
            
            # Filter out things that are likely citations or noise
            if len(term) > 50: 
                continue
                
            terms.append((term, definition))
    
    # Generate HTML
    terms_html = ""
    for term, definition in sorted(terms, key=lambda x: x[0]):
        terms_html += f"""
        <div class="glossary-item">
            <dt>{term}</dt>
            <dd>{definition}</dd>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Glossary | Ancient Literature</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="assets/style.css">
    <style>
        .search-container {{
            margin-bottom: 2rem;
            position: relative;
        }}
        #termSearch {{
            width: 100%;
            padding: 1rem;
            font-size: 1.1rem;
            font-family: var(--font-body);
            border: 2px solid var(--border-color);
            border-radius: 4px;
            background: #fff;
            color: var(--text-primary);
        }}
        #termSearch:focus {{
            outline: none;
            border-color: var(--accent-red);
            box-shadow: 0 0 0 3px rgba(139,0,0,0.1);
        }}
        .no-results {{
            display: none;
            font-style: italic;
            color: var(--text-secondary);
            margin-top: 1rem;
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
                    <a href="glossary.html" class="active-link">Glossary</a>
                </div>
            </nav>
        </aside>
        
        <main class="content-area">
            <header class="page-header">
                <h2>Literary Terms Glossary</h2>
                <div class="search-container">
                    <input type="text" id="termSearch" placeholder="Search for a term or definition...">
                </div>
            </header>
            
            <article class="prose glossary-list">
                <p class="no-results">No terms found matching your search.</p>
                <dl id="glossaryDl">
                    {terms_html}
                </dl>
            </article>
        </main>
    </div>
    
    <script>
        document.getElementById('termSearch').addEventListener('keyup', function() {{
            const filter = this.value.toLowerCase();
            const items = document.querySelectorAll('.glossary-item');
            let hasVisible = false;
            
            items.forEach(item => {{
                const term = item.querySelector('dt').textContent.toLowerCase();
                const def = item.querySelector('dd').textContent.toLowerCase();
                
                if (term.includes(filter) || def.includes(filter)) {{
                    item.style.display = "";
                    hasVisible = true;
                }} else {{
                    item.style.display = "none";
                }}
            }});
            
            document.querySelector('.no-results').style.display = hasVisible ? "none" : "block";
        }});
    </script>
</body>
</html>"""

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Glossary generated with {len(terms)} terms.")

if __name__ == "__main__":
    main()
