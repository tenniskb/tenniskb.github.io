#!/usr/bin/env python3
"""Remove Chapter 1 header text block from multiple files - flexible patterns."""

import re
from pathlib import Path

base = Path(r"C:\Users\Henry\Documents\Github Repos\tenniskb.github.io")

# Files to process
target_files = [
    "en/handbooks/Advanced_Tennis_Training_Manual/Advanced_Tennis_Training_Manual_Chapter_01.html",
    "en/handbooks/Advanced_Tennis_Training_Manual_chapters/Advanced_Tennis_Training_Manual_Chapter_01.html",
    "en/handbooks/Tennis_Training_Manual_Advanced/Tennis_Training_Manual_Advanced_Chapter_01.html",
    "en/handbooks/Tennis_Training_Manual_Advanced/Tennis_Training_Manual_Complete_11_Chapters.html",
    "en/handbooks/The_Art_of_Modern_Tennis/The_Art_of_Modern_Tennis.html",
    "en/handbooks/The_Art_of_Modern_Tennis_Complete/The_Art_of_Modern_Tennis_Complete_Chapter_01.html",
    "en/handbooks/The_Neuro-Motor_Manual_of_Tennis_Mastery/The_Neuro-Motor_Manual_of_Tennis_Mastery_Chapter_01.html",
    "en/handbooks/The_Neuro-Motor_Manual_of_Tennis_Mastery_Professional/The_Neuro-Motor_Manual_of_Tennis_Mastery_Professional_Chapter_01.html",
    "vi/cam-nang/tfl/The_Art_of_Modern_Tennis_Polished.html",
]

# Multiple pattern variants for the header block
patterns = [
    # Standard format with <p> wrappers
    re.compile(
        r'<p>The Kinetic Chain &</p>\s*'
        r'<p><strong>Biomechanical Foundations</strong></p>\s*'
        r'<p>Every shot in tennis — from a 230 km/h serve to a delicate drop volley — is powered by the same underlying system: a chain of forces that begins at the ground and ends at the strings\. Understanding this chain is not optional for elite performance\.</p>\s*'
        r'<p><strong>Section 1\.1</strong></p>\s*'
        r'<p><strong>The Genesis of Power:</strong></p>\s*'
        r'<p><strong>Ground Reaction Forces</strong></p>',
        re.DOTALL
    ),
    # H2 variant - inline (no <p>)
    re.compile(
        r'<h2>Chapter 1 The Kinetic Chain &amp;</h2>\s*'
        r'<p>Biomechanical Foundations Every shot in tennis — from a 230 km/h serve to a delicate drop volley — is powered by the same underlying system: a chain of forces that begins at the ground and ends at the strings\. Understanding this chain is not optional for elite performance\. Section 1\.1 The Genesis of Power: Ground Reaction\s*</p>\s*'
        r'<p><strong>Forces</strong></p>',
        re.DOTALL
    ),
]

total_fixed = 0
files_fixed = []

for rel in target_files:
    f = base / rel
    if not f.exists():
        print(f"SKIP: {rel} (not found)")
        continue
    
    content = f.read_text(encoding='utf-8')
    original_size = len(content)
    
    new_content = content
    matches_total = 0
    
    for pattern in patterns:
        matches = list(pattern.finditer(new_content))
        if matches:
            for match in reversed(matches):
                new_content = new_content[:match.start()] + new_content[match.end():]
            matches_total += len(matches)
    
    if matches_total > 0:
        f.write_text(new_content, encoding='utf-8')
        removed = original_size - len(new_content)
        total_fixed += matches_total
        files_fixed.append((rel, matches_total, removed))
        print(f"✓ {rel}: removed {matches_total} block(s), {removed:,} chars")
    else:
        print(f"  (no match) {rel}")

print(f"\n=== Summary ===")
print(f"Total blocks removed: {total_fixed}")
print(f"Files modified: {len(files_fixed)}")