"""Generate mkdocs.yml for tenniskb-new (two-pass bilingual build).

Reads the en/{foundation,advanced,elite}/ and vi/{foundation,advanced,elite}/
trees, emits a single mkdocs.yml that uses two passes (one for en, one for
vi). For each pass:
  - docs_dir = en/<subsite>/  (then vi/<subsite>/)
  - site_dir = site/en/        (then site/vi/)
  - nav = folder structure of the language tree
"""
import os
import sys

ROOT = r"C:\Users\Henry\GITHUB\tenniskb-new"
LANGS = ["en", "vi"]
SUBSITES = ["foundation", "advanced", "elite", "anatomy-lab", "angle-atlas"]
# Subsites that have basics/ + deep-dives/ sub-trees. Others (anatomy-lab,
# angle-atlas) are flat — .md files are at the subsite root.
NESTED_SUBSITES = {"foundation", "advanced", "elite"}


def yaml_quote(s):
    """Quote a string for safe YAML inclusion."""
    if not s:
        return '""'
    needs_quote = any(c in s for c in ':#{}[]&*!|>%\'"`,?')
    if needs_quote or '"' in s:
        return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'
    return s


def build_nav(docs_dir):
    """
    Walk docs_dir recursively. Returns a YAML nav string.
    """
    lines = []
    # First check for any "loose" .md files at the top level
    loose = sorted(f for f in os.listdir(docs_dir) if f.endswith(".md") and os.path.isfile(os.path.join(docs_dir, f)))
    for f in loose:
        rel = f
        title = f.rsplit(".", 1)[0]
        lines.append(f"  - {yaml_quote(title)}: {rel}")
    # Then walk each subdir (basics, deep-dives, or just direct sub-folders)
    subdirs = sorted(e.name for e in os.scandir(docs_dir) if e.is_dir() and not e.name.startswith("."))
    for sub in subdirs:
        sub_path = os.path.join(docs_dir, sub)
        n_mods = sum(1 for e in os.scandir(sub_path) if e.is_dir())
        n_files = sum(1 for _, _, files in os.walk(sub_path) for f in files if f.endswith(".md"))
        lines.append(f"  - {sub} ({n_mods} modules, {n_files} files):")
        for module in sorted(os.listdir(sub_path)):
            mod_path = os.path.join(sub_path, module)
            if not os.path.isdir(mod_path):
                continue
            lines.append(f"      - {yaml_quote(module)}:")
            for fname in sorted(os.listdir(mod_path)):
                if not fname.endswith(".md"):
                    continue
                rel = f"{sub}/{module}/{fname}"
                title = fname.rsplit(".", 1)[0]
                lines.append(f"          - {yaml_quote(title)}: {rel}")
    return "\n".join(lines)


MKDOCS_TEMPLATE = """site_name: Tennis Knowledge Base (Bilingual)
site_description: EN/VI bilingual tennis knowledge base
site_url: https://example.com/

theme:
  name: material
  language: {lang}
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.indexes
    - toc.follow

nav:
{nav}

markdown_extensions:
  - admonition
  - attr_list
  - def_list
  - footnotes
  - md_in_html
  - tables
  - toc:
      permalink: true

plugins:
  - search

docs_dir: {lang}
site_dir: site/{lang}
"""


def main():
    if len(sys.argv) > 1:
        lang = sys.argv[1]
    else:
        lang = "en"

    lang_root = os.path.join(ROOT, lang)
    if not os.path.isdir(lang_root):
        print(f"FAIL: {lang_root} does not exist")
        sys.exit(1)

    # Build a single nav covering all subsites present under en/ or vi/
    nav_lines = []
    for subsite in SUBSITES:
        subsite_dir = os.path.join(lang_root, subsite)
        if not os.path.isdir(subsite_dir):
            continue
        nav_lines.append(f"  - {subsite.title()} subsite:")
        if subsite in NESTED_SUBSITES:
            # Nested: basics/ + deep-dives/ sub-trees
            subdirs = sorted(e.name for e in os.scandir(subsite_dir) if e.is_dir() and not e.name.startswith("."))
            for sub in subdirs:
                sub_path = os.path.join(subsite_dir, sub)
                n_mods = sum(1 for e in os.scandir(sub_path) if e.is_dir())
                n_files = sum(1 for _, _, files in os.walk(sub_path) for f in files if f.endswith(".md"))
                nav_lines.append(f"      - {sub} ({n_mods} modules, {n_files} files):")
                for module in sorted(os.listdir(sub_path)):
                    mod_path = os.path.join(sub_path, module)
                    if not os.path.isdir(mod_path):
                        continue
                    nav_lines.append(f"          - {yaml_quote(module)}:")
                    for fname in sorted(os.listdir(mod_path)):
                        if not fname.endswith(".md"):
                            continue
                        rel = f"{subsite}/{sub}/{module}/{fname}"
                        title = fname.rsplit(".", 1)[0]
                        nav_lines.append(f"              - {yaml_quote(title)}: {rel}")
        else:
            # Flat: .md files at the subsite root
            loose = sorted(f for f in os.listdir(subsite_dir) if f.endswith(".md") and os.path.isfile(os.path.join(subsite_dir, f)))
            for fname in loose:
                rel = f"{subsite}/{fname}"
                title = fname.rsplit(".", 1)[0]
                nav_lines.append(f"      - {yaml_quote(title)}: {rel}")
    nav = "\n".join(nav_lines) if nav_lines else "  - (no subsites)"

    yml = MKDOCS_TEMPLATE.format(lang=lang, nav=nav)
    out = os.path.join(ROOT, "mkdocs.yml")
    with open(out, "w", encoding="utf-8") as f:
        f.write(yml)
    print(f"  wrote {out} ({len(yml)} bytes, lang={lang}, subsites={[s for s in SUBSITES if os.path.isdir(os.path.join(lang_root, s))]})")


if __name__ == "__main__":
    main()
