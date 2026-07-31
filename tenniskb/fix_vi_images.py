import re
from pathlib import Path

vi_chuong_dir = Path(r"C:\Users\Henry\Documents\Github Repos\tenniskb.github.io\tenniskb\vi\chuong")

# Pattern: src="../hinh-anh/C1-A1.jpg" -> src="../../assets/images/C1-A1.jpg"
pattern = re.compile(r'src="\.\./hinh-anh/(C\d+-A\d+\.jpg)"')

for chapter_dir in sorted(vi_chuong_dir.iterdir()):
    if chapter_dir.is_dir():
        html_file = chapter_dir / "index.html"
        if html_file.exists():
            content = html_file.read_text(encoding="utf-8")
            new_content = pattern.sub(r'src="../../assets/images/\1"', content)
            if new_content != content:
                html_file.write_text(new_content, encoding="utf-8")
                print(f"Fixed: {chapter_dir.name}")
            else:
                print(f"No change: {chapter_dir.name}")

print("\nDone!")