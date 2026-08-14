#!/usr/bin/env python3
from pathlib import Path
import re

base = Path(r"C:\Users\Henry\Documents\Github Repos\tenniskb.github.io")
original = base / "en/handbooks/KyThuat_TraiTay_MotTay_Clean.html.bak"
reformatted = base / "en/handbooks/KyThuat_TraiTay_MotTay_Clean.html"

orig_html = original.read_text(encoding="utf-8")
new_html = reformatted.read_text(encoding="utf-8")

ENTITY_MAP = {
    "&": "&",
    "<": "<",
    ">": ">",
    chr(8220) + chr(8221): '"',
    "&apos;": "'",
    "&nbsp;": " ",
    "&mdash;": "\u2014",
    "&ndash;": "\u2013",
    "&middot;": "\u00b7",
}

def visible_text(html):
    no_tags = re.sub(r"<[^>]+>", " ", html)
    for entity, char in ENTITY_MAP.items():
        no_tags = no_tags.replace(entity, char)
    return re.sub(r"\s+", " ", no_tags).strip()

o_text = visible_text(orig_html)
n_text = visible_text(new_html)

print("Orig: {} chars".format(len(o_text)))
print("New: {} chars".format(len(n_text)))

if n_text in o_text:
    print("New text IS subset of original")
else:
    print("\n=== In original but not new (last 300) ===")
    print(repr(o_text[-300:]))
    print("\n=== In new but not original (last 300) ===")
    print(repr(n_text[-300:]))

print("\n=== <strong> tags in new ===")
for m in re.finditer(r"<strong[^>]*>(.*?)</strong>", new_html, re.DOTALL | re.IGNORECASE):
    print("  " + m.group(0)[:100])

print("\n=== <footer> tags in new ===")
for m in re.finditer(r"<footer[^>]*>(.*?)</footer>", new_html, re.DOTALL | re.IGNORECASE):
    print("  " + m.group(0)[:200])

print("\n=== <p> count ===")
print("  Orig:", len(re.findall(r"<p\b", orig_html, re.IGNORECASE)))
print("  New:", len(re.findall(r"<p\b", new_html, re.IGNORECASE)))