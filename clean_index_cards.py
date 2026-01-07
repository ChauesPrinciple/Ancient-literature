
import re

index_path = r"c:\Users\rober\.gemini\antigravity\scratch\ancient-literature\index.html"

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# Pattern to find module cards and strip the <p>X Topics</p>
# We also want to ensure the button text is strictly "Start Module" or "Enter"
# Matches:
# <div class="module-card">
#     <h3>...</h3>
#     <p>6 Topics</p>
#     <a ...>...</a>
# </div>

def restructure_card(match):
    full_card = match.group(0)
    
    # 1. Remove the <p>X Topics</p> line
    full_card = re.sub(r'<p>\d+ Topics</p>\s*', '', full_card)
    
    # 2. Add a description placeholder or keep it clean? 
    # User said "Just remove number of topics". 
    # If we remove the P, the card might look empty. 
    # Let's add a decorative element or just leave it clean and let the H3 shine.
    # The new CSS handles spacing. 
    
    # Optional: We could wrap "Module X" in a span for styling if we wanted, but let's stick to clean HTML first.
    
    return full_card

# Regex to find the div.module-card blocks
pattern = re.compile(r'<div class="module-card">.*?</div>', re.DOTALL)

new_content = pattern.sub(restructure_card, content)

# Check if anything changed
if new_content != content:
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated index.html: Removed topic counts.")
else:
    print("No changes needed or regex mismatch.")
