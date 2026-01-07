
import os
import re

directory = r"c:\Users\rober\.gemini\antigravity\scratch\ancient-literature\modules\module-11-medea"

# Regex patterns to remove the specific links
# Matches <a href="filename.html"...>Text</a>
# We need to be careful about whitespace
patterns = [
    re.compile(r'<a href="07-anthology-project-point-of-interest\.html"[^>]*>.*?</a>', re.DOTALL),
    re.compile(r'<a href="10-literary-analysis-topic-proposal\.html"[^>]*>.*?</a>', re.DOTALL)
]

def clean_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = content
        for pattern in patterns:
            new_content = pattern.sub("", new_content)

        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Cleaned: {os.path.basename(file_path)}")
    except Exception as e:
        print(f"Error: {e}")

for filename in os.listdir(directory):
    if filename.endswith(".html"):
        clean_file(os.path.join(directory, filename))
