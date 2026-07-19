"""
Generate mkdocs.yml for tenniskb-foundation.

Approach: walk docs/<section>/ and for each .md file, compute its display
breadcrumb (Foundation: read from basics/ or directly; others: read from
section/<Module>/). Emit a nav structure that:
  - Lists all top-level sub-folders (and ReadMe.md files) under a section
  - For Foundation only, groups the basics/ sub-tree as one nested block
  - For other sections, just nests Module/ as a child
  - Inside a Module/, lists .md files with ReadMe.md first

Output: ../mkdocs.yml (relative to the script's location)

Run: python _gen_mkdocs.py
"""
import os
import re
import sys

DOCS = r"C:\Users\Henry\GITHUB\tenniskb-foundation\docs"
OUT  = r"C:\Users\Henry\GITHUB\tenniskb-foundation\mkdocs.yml"

# (nav section title, folder name in docs/, emoji, optional sub-trees spec)
# A sub-trees spec is a list of (label, sub_dir_name) tuples. If a section has a
# sub-trees spec, the nav builder will look in <section>/<sub_dir_name>/ instead
# of walking <section>/ top level. If the spec is empty/None, the section is
# treated as flat (each top-level subdir becomes a module).
#
# NOTE (2026-06-17):
#   - "foundation" was split into basics/ + deep-dives/ (Step 5 of tracking log).
#   - "advanced" was split into basics/ + deep-dives/ (Step 6 of tracking log).
#   - "elite" was split into basics/ + deep-dives/ (Step 7 of tracking log).
#   - "deep-dives" (the old 6th subsite) was consolidated into "foundation" earlier.
# Net effect: 5 subsites, with 3 of them (foundation, advanced, elite) using sub-trees.
SECTIONS = [
    ("🎾 Foundation — Basics & Deep Dives",        "foundation",  "🎾",
        [("📘 Basics (19 modules)",               "basics"),
         ("🌊 Deep Dives (master + 21 modules)",  "deep-dives")]),
    ("🧠 Advanced — Neurology & Anatomy",         "advanced",    "🧠",
        [("📘 Basics (Advanced Manual)",          "basics"),
         ("🧪 Deep Dives (8 numbered modules)",  "deep-dives")]),
    ("🏆 Elite — Break-Free Methodology",         "elite",       "🏆",
        [("📘 Basics (Elite Manual)",             "basics"),
         ("🧪 Deep Dives (13 numbered modules)",  "deep-dives")]),
    ("🦴 Anatomy Lab — Joints & Connective Tissue", "anatomy-lab", "🦴", None),
    ("📐 Angle Atlas — Body Geometry & 50+",       "angle-atlas", "📐", None),
]

def titleize(filename):
    """Convert a .md filename to a nav label by stripping .md and trimming."""
    name = filename[:-3] if filename.endswith(".md") else filename
    if name.lower() == "readme":
        return "ReadMe"
    if name.lower() == "index":
        return "Library Home"
    return name

def relativize(path):
    """Make path relative to mkdocs.yml location with forward slashes."""
    return os.path.relpath(path, os.path.dirname(OUT)).replace(os.sep, "/")

def yaml_quote(s):
    if re.search(r'[:#&*?|<>=!%@`\[\]{}\'"]', s) or s != s.strip() or s == "":
        s_escaped = s.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{s_escaped}"'
    return s

def list_md(folder):
    """Return all .md files in `folder` (top level), sorted with ReadMe first."""
    if not os.path.isdir(folder):
        return []
    files = [f for f in os.listdir(folder) if f.endswith(".md")]
    files.sort(key=lambda f: (f.lower() != "readme.md", f.lower()))
    return files

def list_subdirs(folder, skip_hidden=True):
    """Return all subdirs in `folder`, sorted alphabetically, optionally skipping hidden."""
    if not os.path.isdir(folder):
        return []
    return sorted(
        e.name for e in os.scandir(folder)
        if e.is_dir() and (not skip_hidden or not e.name.startswith("."))
    )

def collect_module_children(module_path):
    """
    Collect children for one module (a folder under a section).
    Returns list of (nav_title, file_path) — the .md files in this module.
    """
    out = []
    for f in list_md(module_path):
        if f.lower() == "readme.md":
            continue  # ReadMe is handled specially (listed as 'ReadMe' as the first entry)
        out.append((titleize(f), os.path.join(module_path, f)))
    # Always include ReadMe first if it exists
    if os.path.isfile(os.path.join(module_path, "ReadMe.md")):
        out.insert(0, ("ReadMe", os.path.join(module_path, "ReadMe.md")))
    return out

def build_subdivided_section_nav(section_dir, sub_trees):
    """
    Build the nav for a section that is split into multiple sub-trees
    (e.g., Foundation = basics/ + deep-dives/, Advanced = basics/ + deep-dives/).
    `sub_trees` is a list of (nav_label, sub_dir_name) tuples; each becomes a
    nested block in the section nav. Modules inside each sub_dir are listed
    in alphabetical order with their .md children.
    """
    lines = []
    for label, sub_dir in sub_trees:
        sub_path = os.path.join(section_dir, sub_dir)
        if not os.path.isdir(sub_path):
            continue
        lines.append(f"      - {label}:")
        modules = list_subdirs(sub_path)
        for mod in modules:
            mod_path = os.path.join(sub_path, mod)
            children = collect_module_children(mod_path)
            if not children:
                continue
            lines.append(f"          - {yaml_quote(mod)}:")
            for nav_title, fp in children:
                rel = relativize(fp)
                lines.append(f"              - {yaml_quote(nav_title)}: {rel}")
    return lines


def build_section_nav(section_dir):
    """
    Build the nav for a non-Foundation section. Lists each top-level subdir
    as a module, with its .md children nested inside.
    """
    lines = []
    # Top-level .md files (excluding ReadMe.md)
    for f in list_md(section_dir):
        if f.lower() == "readme.md":
            continue
        rel = relativize(os.path.join(section_dir, f))
        lines.append(f"      - {yaml_quote(titleize(f))}: {rel}")
    # Top-level subdirs
    modules = list_subdirs(section_dir)
    for mod in modules:
        mod_path = os.path.join(section_dir, mod)
        children = collect_module_children(mod_path)
        if not children:
            continue
        lines.append(f"      - {yaml_quote(mod)}:")
        for nav_title, fp in children:
            rel = relativize(fp)
            lines.append(f"          - {yaml_quote(nav_title)}: {rel}")
    return lines

def build_nav():
    lines = []
    lines.append("  - Home: index.md")
    for entry in SECTIONS:
        sec_title, folder, _, sub_trees = entry
        section_dir = os.path.join(DOCS, folder)
        lines.append(f"  - {yaml_quote(sec_title)}:")
        if sub_trees:
            sub_lines = build_subdivided_section_nav(section_dir, sub_trees)
        else:
            sub_lines = build_section_nav(section_dir)
        lines.extend(sub_lines)
    return "\n".join(lines)

TEMPLATE = """site_name: 🎾 Tennis Knowledge Base — Foundation
site_description: "A bilingual (EN-VI) tennis coaching library for the 3.5 player at 50+ — 5 subsites: Foundation (basics + deep dives), Advanced (neurology), Elite (methodology), Anatomy Lab (joints), Angle Atlas (geometry)."
site_author: Henry Pham Duc
site_url: https://henryphamduc.github.io/tenniskb-foundation/

docs_dir: docs
site_dir: site

theme:
  name: material
  language: en
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.indexes
    - navigation.top
    - navigation.tracking
    - search.suggest
    - search.highlight
    - search.share
    - content.code.copy
    - content.tabs.link
    - toc.follow
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: green
      accent: green
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: green
      accent: green
  icon:
    repo: fontawesome/brands/github
    logo: material/tennis

extra_css:
  - assets/expand-sidebar.css
  - assets/sidebar-nav.css

extra_javascript:
  - assets/open-external-links.js
  - assets/sidebar-nav.js
  - assets/floating-nav.js

markdown_extensions:
  - admonition
  - attr_list
  - def_list
  - footnotes
  - md_in_html
  - meta
  - tables
  - toc:
      permalink: true
      toc_depth: 3
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
  - pymdownx.inlinehilite
  - pymdownx.tasklist:
      custom_checkbox: true

plugins:
  - search:
      lang: en

extra:
  generator: false

nav:
{NAV}
"""

def main():
    nav = build_nav()
    out = TEMPLATE.format(NAV=nav)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Written: {OUT}")
    print(f"   size: {os.path.getsize(OUT):,} bytes")
    nav_line_count = nav.count("\n") + 1
    print(f"   nav lines: {nav_line_count}")

if __name__ == "__main__":
    main()
