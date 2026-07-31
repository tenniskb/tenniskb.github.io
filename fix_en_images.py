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
    
    # Replace all C{ch_num}-A{digit} with correct sequence C{ch_num}-A1..A5
    # The live files have weird numbering (C1-A2..A6, C2-A9..A13, etc.)
    # We need to map them to C{ch_num}-A1..A5 in order of appearance
    pattern = rf'(src="\.\./\.\./assets/images/)C{ch_num}-A\d+(\.jpg")'
    
    # Find all matches
    matches = list(re.finditer(pattern, html))
    if not matches:
        print(f"Chapter {ch_num}: no image refs found")
        continue
    
    # Replace sequentially with A1, A2, A3, A4, A5
    new_html = html
    offset = 0
    for i, m in enumerate(matches):
        correct_name = f"C{ch_num}-A{i+1}.jpg"
        old = m.group(0)
        new = f'{m.group(1)}{correct_name}{m.group(2)}'
        start = m.start() + offset
        end = m.end() + offset
        new_html = new_html[:start] + new + new_html[end:]
        offset += len(new) - len(old)
    
    if new_html != html:
        html_file.write_text(new_html, encoding="utf-8")
        print(f"Chapter {ch_num}: fixed {len(matches)} image refs")
    else:
        print(f"Chapter {ch_num}: no changes needed")

print("Done!")