import os
import glob
import re

def remove_agendas():
    base_dir = r"C:\Users\rober\.gemini\antigravity\scratch\ancient-literature\modules"
    agenda_files = []
    
    # 1. Identify all agenda files
    print("Scanning for agenda files...")
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if "agenda" in file.lower() and file.endswith(".html"):
                full_path = os.path.join(root, file)
                agenda_files.append(full_path)
                print(f"Found agenda: {file}")

    if not agenda_files:
        print("No agenda files found.")
        return

    # Set of filenames to key off for link removal
    agenda_filenames = set(os.path.basename(f) for f in agenda_files)

    # 2. Process all other HTML files to remove links
    print("\nProcessing modules to remove links...")
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".html") and os.path.join(root, file) not in agenda_files:
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                for agenda_name in agenda_filenames:
                    # Sidebar link removal
                    pattern = r'<a\s+[^>]*href=["\'][^"\']*' + re.escape(agenda_name) + r'["\'][^>]*>.*?</a>'
                    content = re.sub(pattern, '', content, flags=re.IGNORECASE | re.DOTALL)
                    
                    # Footer 'Previous' link removal
                    footer_pattern = r'<a\s+[^>]*href=["\'][^"\']*' + re.escape(agenda_name) + r'["\'][^>]*class=["\']nav-btn prev["\'][^>]*>.*?</a>'
                    content = re.sub(footer_pattern, '', content, flags=re.IGNORECASE | re.DOTALL)

                if content != original_content:
                    print(f"Updating links in: {file}")
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)

    # 3. Delete agenda files
    print("\nDeleting agenda files...")
    for file_path in agenda_files:
        try:
            os.remove(file_path)
            print(f"Deleted: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

if __name__ == "__main__":
    remove_agendas()
