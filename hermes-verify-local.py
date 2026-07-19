#!/usr/bin/env python3
"""Verify local site build for AI-slop removal."""
import os, re, subprocess
from pathlib import Path

# Check the built site in _site directory (or site/)
SITE_DIR = Path("_site")  # mkdocs default
if not SITE_DIR.exists():
    SITE_DIR = Path("site")  # our worktree location

if not SITE_DIR.exists():
    print("ERROR: Site directory not found. Run 'mkdocs build' first.")
    exit(1)

# Patterns that indicate remaining AI-slop
SLOP_PATTERNS = [
    r'##\s*Sources?:?\s*',
    r'##\s*Nguồn?:?\s*',
    r'\*\*Sources\s*/\s*Nguồn:?\*\*',
    r'\*\*Sources:?\*\*',
    r'\*\*Nguồn:?\*\*',
    r'See you on the court',
    r'Hẹn gặp trên sân',
    r'\bengineer\b',
    r'\bkỹ sư\b',
    # Emoji ranges
    r'[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002600-\U000027BF\U0001F1E0-\U0001F1FF]',
]

def check_file(filepath):
    """Check a single HTML file for slop."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        for pattern in SLOP_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE | re.UNICODE):
                # Get first match for reporting
                match = re.search(pattern, content, re.IGNORECASE | re.UNICODE)
                if match:
                    # Extract context around the match
                    start = max(0, match.start() - 50)
                    end = min(len(content), match.end() + 50)
                    context = repr(content[start:end])
                    issues.append(f"{pattern}: {context}")
        
        return issues
    except Exception as e:
        return [f"Error reading file: {e}"]

def main():
    print("Checking built site for AI-slop...")
    print("=" * 60)
    
    html_files = list(SITE_DIR.rglob("*.html"))
    if not html_files:
        print("ERROR: No HTML files found in", SITE_DIR)
        return 1
    
    total_issues = 0
    files_with_issues = 0
    
    # Check a sample of pages to avoid too much output
    sample_files = [
        "index.html",
        "en/index.html", 
        "vi/index.html",
        "elite/basics/Elite Manual/index.html",
        "vi/elite/basics/Elite Manual/index.html",
        "elite/deep-dives/Anti-Orthodox Manifesto/index.html",
        "vi/elite/deep-dives/Anti-Orthodox Manifesto/index.html",
        "foundation/basics/Backhand/index.html",
        "vi/foundation/basics/Backhand/index.html",
        "advanced/basics/Forehand/index.html",
        "vi/advanced/basics/Forehand/index.html",
    ]
    
    # Filter to only existing files
    existing_samples = [f for f in sample_files if (SITE_DIR / f).exists()]
    
    if not existing_samples:
        # Fallback: check first 10 files
        existing_samples = [str(f.relative_to(SITE_DIR)) for f in html_files[:10]]
    
    print(f"Checking {len(existing_samples)} sample files...")
    print()
    
    for rel_path in existing_samples:
        filepath = SITE_DIR / rel_path
        issues = check_file(filepath)
        if issues:
            print(f"✗ {rel_path}")
            for issue in issues[:2]:  # Show max 2 issues per file
                print(f"    {issue}")
            total_issues += len(issues)
            files_with_issues += 1
        else:
            print(f"✓ {rel_path}")
    
    print()
    print("=" * 60)
    print(f"Summary: {files_with_issues}/{len(existing_samples)} files have issues")
    print(f"Total issues found: {total_issues}")
    
    if total_issues == 0:
        print("✓ NO AI-SLOP DETECTED IN SAMPLE")
        return 0
    else:
        print("✗ ISSUES FOUND - See details above")
        return 1

if __name__ == "__main__":
    exit(main())