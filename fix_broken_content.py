import os
import html
import re
from pathlib import Path

MODULES_DIR = Path("site/modules")

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # Check for the IMSCC XML wrapper artifact
        # <topic xmlns=...> ... <text texttype="text/html">&lt;p&gt;...&lt;/p&gt;</text> </topic>
        
        # Regex to find the escaped text content inside the XML wrapper
        # We look for <text ...>(.*?)</text>
        match = re.search(r'<text[^>]*>(.*?)</text>', content, re.DOTALL)
        
        if match:
            print(f"Fixing XML wrapper in {filepath.name}")
            escaped_inner = match.group(1)
            unescaped_inner = html.unescape(escaped_inner)
            
            # Now replace the whole <topic>...</topic> block with the unescaped inner HTML
            # We need to find the start and end of <topic>
            topic_match = re.search(r'(<topic[^>]*>.*?</topic>)', content, re.DOTALL)
            if topic_match:
                # Does the content usually reside in an <article>?
                # Yes, usually wrapped in <article class="prose"> ... </article>
                
                # Check for BOM in unescaped content
                unescaped_inner = unescaped_inner.replace(u'\ufeff', '')
                
                # Strip artifacts from the inner content
                unescaped_inner = re.sub(r' style="[^"]*"', '', unescaped_inner)
                unescaped_inner = re.sub(r' class="[^"]*"', '', unescaped_inner)
                unescaped_inner = re.sub(r'<span>(.*?)</span>', r'\1', unescaped_inner)
                
                # Replace the entire XML block with the clean HTML
                content = content.replace(topic_match.group(1), unescaped_inner)
                
        # Also check for general escaped HTML if XML wrapper wasn't found but &lt;p&gt; exists
        elif "&lt;p&gt;" in content or "&lt;p " in content:
             print(f"Fixing escaped HTML in {filepath.name}")
             # This is riskier, let's target the article body if possible
             article_match = re.search(r'(<article class="prose">)(.*?)(</article>)', content, re.DOTALL)
             if article_match:
                 body = article_match.group(2)
                 if "&lt;p" in body:
                     unescaped_body = html.unescape(body)
                     unescaped_body = unescaped_body.replace(u'\ufeff', '')
                     unescaped_body = re.sub(r' style="[^"]*"', '', unescaped_body)
                     content = content.replace(article_match.group(0), f'{article_match.group(1)}{unescaped_body}{article_match.group(3)}')

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
    return False

def main():
    count = 0
    for root, dirs, files in os.walk(MODULES_DIR):
        for file in files:
            if file.endswith(".html"):
                if fix_file(Path(root) / file):
                    count += 1
    print(f"Fixed {count} files.")

if __name__ == "__main__":
    main()
