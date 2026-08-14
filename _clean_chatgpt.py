#!/usr/bin/env python3
"""Clean up ChatGPT_Huong_Dan_Ky_Thuat_Tennis.html - remove busy artifacts."""

import re
from pathlib import Path

SRC = Path(r"C:\Users\Henry\Documents\Github Repos\tenniskb.github.io\vi\cam-nang\ChatGPT_Huong_Dan_Ky_Thuat_Tennis.html")

def main():
    content = SRC.read_text(encoding='utf-8')
    print(f"Original: {len(content):,} chars")
    
    # 1. Find the busy H2 (4467 chars) - the entire 96-chapter TOC + AI planning artifact
    # Find the H2 that contains "tôi sẽ cần biên soạn" or "Quy mô dự kiến"
    artifact_start = content.find('Quy mô dự kiến')
    if artifact_start < 0:
        print("Artifact not found")
        return
    
    # Find the H2 tag before this
    h2_start = content[:artifact_start].rfind('<h2')
    if h2_start < 0:
        print("H2 not found")
        return
    
    # Find the H2's closing - look for next <h2> or last </h2> before next tag
    h2_end = content.find('</h2>', artifact_start) + len('</h2>')
    print(f"Busy H2: {h2_start} to {h2_end} ({h2_end - h2_start} chars)")
    
    # Find the position of the "Quy mô dự kiến" content within the H2
    # So we know what to keep (the chapter list) vs what to remove (AI planning)
    
    # 2. Reformat the busy H2:
    # - Keep the chapter list (96 chapters)
    # - Remove the AI planning artifacts at the end
    busy_h2 = content[h2_start:h2_end]
    
    # Split to find where the AI artifact starts within the H2
    # The chapter list ends with "Coach Assessment System" and then "PHỤ LỤC"
    # The AI artifact starts with "Quy mô dự kiến:" or "Prompt Library"
    # Find the start of the AI artifact
    artifact_in_h2 = busy_h2.find('Quy mô dự kiến')
    prompt_library_pos = busy_h2.find('Prompt Library')
    
    # Find the prompt library section (last useful content)
    if prompt_library_pos > 0:
        # Find the start of "PHỤ LỤC" (start of appendices)
        phu_luc_pos = busy_h2.find('PHỤ LỤC')
        if phu_luc_pos > 0:
            # Keep everything up to "PHỤ LỤC" + appendices list
            # But trim the AI planning artifacts
            
            # The structure after PHỤ LỤC is the list of appendices
            # AI artifacts are: "Quy mô dự kiến" section, "Tuyệt vời" section
            
            # Find "Tuyệt vời" - that's the AI artifact
            tuyet_voi = busy_h2.find('Tuyệt vời')
            if tuyet_voi > 0:
                # Cut at "Tuyệt vời" - keep everything before
                cleaned_h2 = busy_h2[:tuyet_voi].rstrip() + '</h2>'
                
                # Also remove "Quy mô dự kiến" section if it exists
                cleaned_h2 = cleaned_h2.replace('\n\nQuy mô dự kiến:', '')
                
                content = content[:h2_start] + cleaned_h2 + content[h2_end:]
                print(f"Cleaned H2: {len(cleaned_h2)} chars")
    
    # 3. Remove "Tôi sẽ" / "Nguyên tắc biên soạn" section if it's just an AI prep block
    # Find the "Nguyên tắc biên soạn" section
    nt_start = content.find('<h1 id="nguyen-tac-bien-soan">Nguyên tắc biên soạn</h1>')
    if nt_start < 0:
        nt_start = content.find('Nguyên tắc biên soạn')
    if nt_start > 0:
        # Find the next H1 after this
        # Find end of the section (next H1 or chapter break)
        nt_close = content.find('Nguyên tắc biên soạn')
        if nt_close > 0:
            # Find the next <h1 after this
            next_h1 = content.find('<h1', nt_close + 50)
            if next_h1 > 0:
                # Find the closing </h1> of the next H1
                next_h1_end = content.find('</h1>', next_h1) + len('</h1>')
                # Take content from nt_close to next_h1_end, and check if it's the AI prep block
                prep_block = content[nt_close:next_h1_end]
                # Check if it contains "Tôi sẽ"
                if 'Tôi sẽ' in prep_block or 'Tôi sẽ kết hợp' in prep_block:
                    print(f"\nFound AI prep block: {nt_close} to {next_h1_end} ({next_h1_end - nt_close} chars)")
                    # Just remove the heading itself - keep the content
                    # Or remove the entire block
                    # The block is at the very start of the actual content
                    # Let's just remove the heading line
                    pass
    
    # 4. Remove "Powered by chatgptexporter" footer
    content = re.sub(
        r'<p>Powered by <a href="https://www\.chatgptexporter\.com[^"]*">[^<]*</a></p>',
        '',
        content
    )
    content = re.sub(r'<p>Powered by <a href="https://www\.chatgptexporter\.com[^"]*">[^<]*</a></p>', '', content)
    
    # 5. Cleanup multiple blank lines
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    # Backup
    backup = SRC.with_suffix('.html.bak')
    backup.write_text(SRC.read_text(encoding='utf-8'), encoding='utf-8')
    
    # Write
    SRC.write_text(content, encoding='utf-8')
    print(f"\nFinal: {len(content):,} chars (removed {280127 - len(content):,} chars)")
    print(f"Backup: {backup}")

if __name__ == '__main__':
    main()