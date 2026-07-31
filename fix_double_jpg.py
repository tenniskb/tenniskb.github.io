import re
from pathlib import Path

chapters_dir = Path("tenniskb/en/chuong")

for ch_num in range(1, 31):
    # Find the chapter folder
    folders = list(chapters_dir.glob(f"chapter-{ch_num:02d}-*/index.html"))
    if not folders:
        print(f"Chapter {ch_num}: NOT FOUND")
        continue
    
    html_file = folders[0]
    html = html_file.read_text(encoding="utf-8")
    
    # Fix double .jpg.jpg
    html = html.replace('.jpg.jpg"', '.jpg"')
    html = html.replace('.jpg.jpg\'', '.jpg\'')
    
    html_file.write_text(html, encoding="utf-8")
    print(f"Chapter {ch_num}: fixed double .jpg")

print("Done!")