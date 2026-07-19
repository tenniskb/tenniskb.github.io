#!/usr/bin/env python3
import os
import re

# Base path to the source docs
DOCS_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs')

# Patterns that should NOT be present after cleanup
BAD_PATTERNS = [
    # Emojis and decorative slop
    (r'[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002600-\U000027BF\U0001F1E0-\U0001F1FF]+', 'emoji'),
    # Sources sections
    (r'##\s*Sources?:?\s*', 'sources-header'),
    (r'##\s*Nguồn?:?\s*', 'nguon-header'),
    (r'\*\*Sources\s*/\s*Nguồn:?\*\*', 'bold-sources'),
    (r'\*\*Sources:?\*\*', 'bold-sources'),
    (r'\*\*Nguồn:?\*\*', 'bold-nguon'),
    # See you on the court
    (r'See you on the court', 'see-you-court'),
    (r'Hẹn gặp trên sân', 'hen-gap-san'),
    # Engineer/kỹ sư
    (r'\bengineer\b', 'engineer'),
    (r'\bkỹ sư\b', 'ky-su'),
    # Additional specific phrases we removed
    (r'Tennis Research', 'tennis-research'),
    (r'Kwen-Ollama', 'kwen-ollama'),
    (r'Olama', 'olama'),
    (r'Kinetic-Chain', 'kinetic-chain'),
]

def check_file(filepath):
    """Check a single file for bad patterns."""
    rel_path = os.path.relpath(filepath, DOCS_ROOT)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Skip binary files
        return []
    
    found = []
    for pattern, label in BAD_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            found.append((label, pattern))
    return found

def main():
    # List of files we know we cleaned (from our earlier operations)
    # We'll check a subset to verify
    files_to_check = [
        'en/index.md',
        'vi/index.md',
        'en/elite/basics/Elite Manual/index.md',
        'vi/elite/basics/Elite Manual/index.md',
        'en/elite/deep-dives/Anti-Orthodox Manifesto/index.md',
        'vi/elite/deep-dives/Anti-Orthodox Manifesto/index.md',
        'en/foundation/basics/Backhand/index.md',
        'vi/foundation/basics/Backhand/index.md',
        'en/advanced/basics/Forehand/index.md',
        'vi/advanced/basics/Forehand/index.md',
        'en/foundation/deep-dives/Elite Manual/index.md',
        'vi/foundation/deep-dives/Elite Manual/index.md',
        'en/foundation/deep-dives/Self-Coaching Discipline/index.md',
        'vi/foundation/deep-dives/Self-Coaching Discipline/index.md',
    ]
    
    any_issues = False
    for rel_file in files_to_check:
        filepath = os.path.join(DOCS_ROOT, rel_file)
        if not os.path.exists(filepath):
            print(f"⚠️  File not found: {rel_file}")
            continue
        
        issues = check_file(filepath)
        if issues:
            any_issues = True
            print(f"❌ {rel_file}")
            for label, pattern in issues:
                print(f"    - Found: {label}")
        else:
            print(f"✅ {rel_file}")
    
    print()
    if any_issues:
        print("❌ ISSUES FOUND: Some slop patterns still present in source files.")
        return 1
    else:
        print("✅ ALL CLEAR: No slop patterns detected in sampled source files.")
        return 0

if __name__ == "__main__":
    exit(main())