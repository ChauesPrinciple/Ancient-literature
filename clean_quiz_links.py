import os
import re
from pathlib import Path

def clean_navigation(file_path):
    """Remove links to deleted quiz/test files from navigation"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Patterns to remove from navigation
    patterns_to_remove = [
        # Quiz/test links in sidebar nav
        r'<a href="[^"]*syllabus-quiz\.html"[^>]*>[^<]*</a>',
        r'<a href="[^"]*formative-quiz\.html"[^>]*>[^<]*</a>',
        r'<a href="[^"]*end-of-chapter-test\.html"[^>]*>[^<]*</a>',
        r'<a href="[^"]*chapter-quizzes\.html"[^>]*>[^<]*</a>',
        # Footer nav links to these files
        r'<a href="[^"]*syllabus-quiz\.html" class="nav-btn[^"]*">[^<]*</a>',
        r'<a href="[^"]*formative-quiz\.html" class="nav-btn[^"]*">[^<]*</a>',
        r'<a href="[^"]*end-of-chapter-test\.html" class="nav-btn[^"]*">[^<]*</a>',
    ]
    
    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    
    # Clean up any double spaces or empty lines
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned: {file_path}")
        return True
    return False

def main():
    modules_dir = Path("modules")
    count = 0
    
    for html_file in modules_dir.rglob("*.html"):
        if clean_navigation(html_file):
            count += 1
    
    print(f"\nCleaned {count} files")

if __name__ == "__main__":
    main()
