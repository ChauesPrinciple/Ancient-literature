import zipfile
import xml.etree.ElementTree as ET
import sys
import os

def extract_docx_text(docx_path):
    try:
        with zipfile.ZipFile(docx_path) as z:
            xml_content = z.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            
            namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            text = []
            
            for p in tree.findall('.//w:p', namespaces):
                p_text = []
                for t in p.findall('.//w:t', namespaces):
                    if t.text:
                        p_text.append(t.text)
                if p_text:
                    text.append(''.join(p_text))
            
            return '\n'.join(text)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    file_path = "Source citation.docx"
    print(extract_docx_text(file_path))
