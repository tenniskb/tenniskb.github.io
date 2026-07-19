#!/usr/bin/env python3
import urllib.request
import urllib.error
from urllib.parse import urljoin
import re
import os

BASE = "https://henryphamduc.github.io/tenniskb/"
VI_BASE = "https://henryphamduc.github.io/tenniskb/vi/"

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
    r'Tennis Research',
    r'Kwen-Ollama',
    r'Olama',
    r'Kinetic-Chain',
]

def check_url(url, label):
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (compatible; VerificationBot/1.0)'}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status != 200:
                return f"HTTP {response.status}"
            
            # Read and decode content
            content = response.read().decode('utf-8', errors='ignore')
            
            # Check for slop patterns
            for pattern in SLOP_PATTERNS:
                if re.search(pattern, content, re.IGNORECASE):
                    return f"SLOT: {pattern}"
            
            return "OK"
            
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return f"URL Error: {str(e)[:50]}"
    except Exception as e:
        return f"Error: {str(e)[:50]}"

def main():
    print("Verifying AI-slop removal from live tenniskb site...")
    print("=" * 60)
    
    # Test key pages
    test_pages = [
        ("EN Home", ""),
        ("VI Home", "vi/"),
        ("EN Elite Manual", "elite/basics/Elite Manual/"),
        ("VI Elite Manual", "vi/elite/basics/Elite Manual/"),
        ("EN Anti-Orthodox Manifesto", "elite/deep-dives/Anti-Orthodox Manifesto/"),
        ("VI Anti-Orthodox Manifesto", "vi/elite/deep-dives/Anti-Orthodox Manifesto/"),
        ("EN Foundation Backhand", "foundation/basics/Backhand/"),
        ("VI Foundation Backhand", "vi/foundation/basics/Backhand/"),
        ("EN Advanced Forehand", "advanced/basics/Forehand/"),
        ("VI Advanced Forehand", "vi/advanced/basics/Forehand/"),
    ]
    
    all_good = True
    for label, path in test_pages:
        url = urljoin(BASE if not path.startswith('vi/') else VI_BASE, path)
        result = check_url(url, label)
        if result == "OK":
            print(f"✓ {label:<35} OK")
        else:
            print(f"✗ {label:<35} {result}")
            all_good = False
    
    print("=" * 60)
    if all_good:
        print("✓ ALL TESTS PASSED - No AI-slop detected")
        return 0
    else:
        print("✗ Some issues found - see above")
        return 1

if __name__ == "__main__":
    exit(main())