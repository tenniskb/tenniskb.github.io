#!/usr/bin/env python3
"""Replace Tennis_Đẳng_Cấp_Cao_20_Chương.html with new content in Tennis_Backhand_Techniques.html format."""

from pathlib import Path
import re

# Source file (attached - new content)
SRC_FILE = Path(r"C:\Users\Henry\Downloads\to be corrected\Tennis_Đẳng_Cấp_Cao_20_Chương.html")
# Target file (online)
TARGET_FILE = Path(r"C:\Users\Henry\Documents\Github Repos\tenniskb.github.io\vi\cam-nang\Tennis_Đẳng_Cấp_Cao_20_Chương.html")
# Template file
TEMPLATE = Path(r"C:\Users\Henry\Documents\Github Repos\tenniskb.github.io\en\handbooks\Tennis_Backhand_Techniques.html")

def main():
    # Read all files
    src_html = SRC_FILE.read_text(encoding='utf-8')
    target_html = TARGET_FILE.read_text(encoding='utf-8')
    tpl_html = TEMPLATE.read_text(encoding='utf-8')
    
    print(f"Source: {len(src_html):,} chars")
    print(f"Target (current): {len(target_html):,} chars")
    print(f"Template: {len(tpl_html):,} chars")
    
    # ========== EXTRACT SOURCE CONTENT ==========
    # Get body content
    src_body_start = src_html.find('<body>')
    src_body_end = src_html.rfind('</body>')
    src_body = src_html[src_body_start:src_body_end]
    
    # Get source masthead
    src_masthead_start = src_body.find('<div class="masthead">')
    src_masthead_end = src_body.find('</div>', src_masthead_start) + len('</div>')
    src_masthead = src_body[src_masthead_start:src_masthead_end]
    print(f"Source masthead: {src_masthead[:200]}")
    
    # Get source content-wrap inner content
    src_cw_start = src_body.find('<div class="content-wrap">')
    src_cw_end = src_body.rfind('</div>')  # closing of content-wrap
    src_content_inner = src_body[src_cw_start + len('<div class="content-wrap">'):src_cw_end]
    print(f"Source content inner: {len(src_content_inner):,} chars")
    
    # ========== EXTRACT TEMPLATE PARTS ==========
    # Template head (CSS)
    tpl_head_start = tpl_html.find('<head>') + len('<head>')
    tpl_head_end = tpl_html.find('</head>')
    tpl_head = tpl_html[tpl_head_start:tpl_head_end]
    
    # Template body structure
    tpl_body_start = tpl_html.find('<body>') + len('<body>')
    tpl_body_end = tpl_html.rfind('</body>')
    tpl_body = tpl_html[tpl_body_start:tpl_body_end]
    
    # Template content-wrap inner (to understand structure)
    tpl_cw_start = tpl_body.find('<div class="content-wrap">')
    tpl_cw_end = tpl_body.find('</div>', tpl_cw_start)
    tpl_content_inner = tpl_body[tpl_cw_start + len('<div class="content-wrap">'):tpl_cw_end]
    print(f"Template content inner: {len(tpl_content_inner):,} chars")
    
    # ========== BUILD NEW HTML ==========
    # 1. Build new <head> using template CSS but with Vietnamese lang/title
    new_head = tpl_head
    
    # Update title in head
    title_match = re.search(r'<title>.*?</title>', new_head)
    if title_match:
        new_head = new_head[:title_match.start()] + '<title>Tennis Đẳng Cấp Cao: Huấn Luyện Tim Mạch VO2 Max & Zone Training</title>' + new_head[title_match.end():]
    
    # Update lang to vi
    new_html = '<!DOCTYPE html>\n<html lang="vi">\n<head>' + new_head + '</head>\n<body>\n'
    
    # 2. Masthead - use source's masthead content but with template styling structure
    # Extract title and subtitle from source masthead
    src_tag_match = re.search(r'<span class="tag">(.*?)</span>', src_masthead)
    src_h1_match = re.search(r'<h1>(.*?)</h1>', src_masthead)
    src_subtitle_match = re.search(r'<p class="subtitle">(.*?)</p>', src_masthead)
    
    tag_text = src_tag_match.group(1) if src_tag_match else 'Đẳng Cấp Cao'
    h1_text = src_h1_match.group(1) if src_h1_match else 'Tennis Đẳng Cấp Cao'
    subtitle_text = src_subtitle_match.group(1) if src_subtitle_match else 'Tennis Future Lab · Cẩm nang kỹ thuật chuyên sâu'
    
    # Build masthead matching template structure
    new_html += f'''<div class="masthead">
<span class="tag">{tag_text}</span>
<h1>{h1_text}</h1>
<p class="subtitle">{subtitle_text}</p>
</div>
'''
    
    # 3. Content-wrap with source content
    new_html += '<div class="content-wrap">\n'
    new_html += src_content_inner
    new_html += '</div>\n'
    
    # 4. Page-nav (from template, translated to Vietnamese)
    new_html += '''<nav class="page-nav">
  <a href="index.html" class="nav-btn prev">← Trang Trước</a>
  <a href="index.html" class="nav-btn toc">≡ Mục Lục</a>
  <a href="index.html" class="nav-btn next">Trang Sau →</a>
</nav>

    <hr class="footer-divider">

    <footer>© 2026 Henry Pham Duc · Tennis Future Lab · All contents are for educational purposes only.</footer>
</body>
</html>'''
    
    # Backup target
    backup = TARGET_FILE.with_suffix('.html.bak')
    backup.write_text(target_html, encoding='utf-8')
    print(f"\nBackup created: {backup}")
    
    # Write new content
    TARGET_FILE.write_text(new_html, encoding='utf-8')
    print(f"✓ Written: {len(new_html):,} chars")

if __name__ == '__main__':
    main()