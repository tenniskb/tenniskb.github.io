"""
Build C:\\Users\\Henry\\GITHUB\\tenniskb-foundation from:
  - tennis/docs/  (Foundation content — 19 unique folders, skip facebook/1-Page/4 subsite dups)
  - Documents/    (4 source-of-truth subsite folders + Foundation/Deep Dives)

Per user directive: COPY only (preserve originals), do NOT touch C:\\Users\\Henry\\GITHUB\\tenniskb (live site).
Target is local-only — no git init, no remote, no commit.
"""
import os
import shutil
import sys

# --- Sources ---
TENNIS_DOCS  = r"C:\Users\Henry\GITHUB\tennis\docs"
TENNIS_ROOT  = r"C:\Users\Henry\GITHUB\tennis"
DOCS_BASE    = r"C:\Users\Henry\Documents\New Tennis Knowledge"

# --- Target (will be created) ---
TARGET       = r"C:\Users\Henry\GITHUB\tenniskb-foundation"
TARGET_DOCS  = os.path.join(TARGET, "docs")

# --- Foundation content folders (kept from tennis/docs/) ---
# Skipped per user: 1-Page Pocket Card, facebook, Advanced, Anatomy_Lab, Elite, Tuyen_Tap
# NOTE: 1-Page Pocket Card is now sourced from Documents/.../Foundation/Deep Dives/
# (moved into foundation/ on 2026-06-17 along with the other deep-dive folders).
# It is no longer in this list because the canonical source is now DEEP_DIVES_SOURCE.
FOUNDATION_FOLDERS = [
    "Backhand",
    "Continental Grip",
    "Doubles Patterns",
    "Doubles Serves",
    "Doubles Tactics",
    "Eastern Semi-Western Grip",
    "Footwork",
    "Forehand",
    "Foundations and Grip",
    "Grip Change Map",
    "Grip Pressure",
    "Lob and Overhead",
    "Mental Game",
    "Return of Serve",
    "Serve",
    "Slice Approach",
    "Slice Family Doubles",
    "Slice Variations",
    "Volley",
]

# --- Deep-dive folders (consolidated into foundation/deep-dives/ on 2026-06-17) ---
# These are sourced from Documents/.../Foundation/Deep Dives/ and copied
# into docs/foundation/deep-dives/ (a wrapper subdir added to keep the
# Foundation top-level tidy).
DEEP_DIVES_SOURCE = os.path.join(DOCS_BASE, "Foundation", "Deep Dives")

# --- The other 4 subsites (copied from Documents/) ---
# (label_in_nav, source_path)
# NOTE: "deep-dives" was consolidated INTO "foundation" (2026-06-17). Its content
# now lives at docs/foundation/<deep-dive folders>/, with the original 19
# modules renamed to docs/foundation/basics/. The upstream source for the
# deep-dive folders remains Documents/.../Foundation/Deep Dives/.
SUBSITE_SOURCES = [
    ("advanced",     os.path.join(DOCS_BASE, "Advanced")),
    ("elite",        os.path.join(DOCS_BASE, "Elite")),
    ("anatomy-lab",  os.path.join(DOCS_BASE, "Anatomy_Lab")),
    ("angle-atlas",  os.path.join(DOCS_BASE, "Tuyen_Tap")),  # Tuyen_Tap = Vietnamese for "Angle Atlas"
]

# --- Root-level assets copied from tennis/ ---
ROOT_ASSETS_FROM_TENNIS = [
    # (source, dest_name)
    (os.path.join(TENNIS_DOCS, "assets"), "assets"),
    (os.path.join(TENNIS_DOCS, "images"), "images"),
]

def sizeof_mb(path):
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total / (1024 * 1024)

def copy_tree(src, dst, label):
    if not os.path.exists(src):
        print(f"  ✗ MISSING: {src}")
        return False
    os.makedirs(dst, exist_ok=True)
    print(f"  → copying {label}")
    print(f"      {src}")
    print(f"    → {dst}  ({sizeof_mb(src):.1f} MB)")
    shutil.copytree(src, dst, dirs_exist_ok=True)
    return True

def main():
    # 0. Refuse to touch the live site
    LIVE = r"C:\Users\Henry\GITHUB\tenniskb"
    if os.path.exists(LIVE) and os.path.normpath(TARGET).lower() == os.path.normpath(LIVE).lower():
        print("ERROR: target is the live tenniskb. Aborting.")
        sys.exit(1)

    # 1. Create target skeleton
    print(f"\n[1] Creating target: {TARGET}")
    os.makedirs(TARGET_DOCS, exist_ok=True)
    print(f"    {TARGET_DOCS}  (created)")

    # 2. Foundation basics = 19 folders from tennis/docs/ → docs/foundation/basics/
    print(f"\n[2] Copying Foundation basics from tennis/docs/ (19 folders)")
    foundation_dst = os.path.join(TARGET_DOCS, "foundation", "basics")
    os.makedirs(foundation_dst, exist_ok=True)
    for folder in FOUNDATION_FOLDERS:
        src = os.path.join(TENNIS_DOCS, folder)
        dst = os.path.join(foundation_dst, folder)
        ok = copy_tree(src, dst, folder)
        if not ok:
            print(f"    ! skipped: {folder}")

    # 2b. Foundation deep-dives = full content of Documents/.../Foundation/Deep Dives/
    #     copied into docs/foundation/deep-dives/ (NOT docs/foundation/ — the deep-dive
    #     subdirectory is a wrapper added 2026-06-17 to keep Foundation top-level tidy).
    print(f"\n[2b] Copying Foundation deep-dives from Documents/.../Deep Dives/ (into deep-dives/ wrapper)")
    if os.path.isdir(DEEP_DIVES_SOURCE):
        deep_dives_root = os.path.join(TARGET_DOCS, "foundation", "deep-dives")
        # Copy each top-level item inside DEEP_DIVES_SOURCE into deep-dives_root
        for entry in os.listdir(DEEP_DIVES_SOURCE):
            src = os.path.join(DEEP_DIVES_SOURCE, entry)
            dst = os.path.join(deep_dives_root, entry)
            if not os.path.exists(src):
                continue
            if os.path.isdir(src):
                copy_tree(src, dst, f"deep-dives/{entry}")
            else:
                # Copy single files too (e.g. README.md at the root of Deep Dives)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                print(f"    • copied file: {entry}")
    else:
        print(f"    ! WARNING: deep-dives source not found: {DEEP_DIVES_SOURCE}")

    # 3. Copy assets/ and images/ to docs/ (MkDocs serves from docs/ root)
    print(f"\n[3] Copying root assets (assets/, images/) from tennis/docs/")
    for src, name in ROOT_ASSETS_FROM_TENNIS:
        dst = os.path.join(TARGET_DOCS, name)
        copy_tree(src, dst, name)

    # 4 subsites: elite, anatomy-lab, angle-atlas
    print(f"\n[4] Copying 4 subsites from Documents/New Tennis Knowledge/")

    # 4a. Advanced: split into basics/ (Advanced Manual) + deep-dives/ (8 numbered modules)
    #     The Advanced source is a flat folder; the destination has the new 2026-06-17
    #     basics/ + deep-dives/ sub-structure.
    ADVANCED_BASICS_NAMES = ["Advanced Manual"]
    ADVANCED_DEEP_DIVES_NAMES = [
        "01 Embodied Cognition",
        "02 Two Engines",
        "03 Proprioception",
        "04 Reflex Arcs",
        "05 Tensegrity Body",
        "06 Fascia Spiral",
        "07 X-Factor Anatomy",
        "08 Head Position and Vestibular",
    ]
    advanced_src = os.path.join(DOCS_BASE, "Advanced")
    if os.path.isdir(advanced_src):
        print(f"\n[4a] Copying Advanced with basics/deep-dives split")
        advanced_dst = os.path.join(TARGET_DOCS, "advanced")
        os.makedirs(advanced_dst, exist_ok=True)
        # basics/
        for name in ADVANCED_BASICS_NAMES:
            src = os.path.join(advanced_src, name)
            dst = os.path.join(advanced_dst, "basics", name)
            if os.path.isdir(src):
                copy_tree(src, dst, f"advanced/basics/{name}")
        # deep-dives/
        for name in ADVANCED_DEEP_DIVES_NAMES:
            src = os.path.join(advanced_src, name)
            dst = os.path.join(advanced_dst, "deep-dives", name)
            if os.path.isdir(src):
                copy_tree(src, dst, f"advanced/deep-dives/{name}")
        # Loose .md files at the source root stay at the destination root
        # (index.md, ReadMe.md). For index.md, rewrite relative links to add
        # basics/ or deep-dives/ prefix — the source index.md was written before
        # the wrap and still points to the old paths.
        for entry in os.listdir(advanced_src):
            src = os.path.join(advanced_src, entry)
            dst = os.path.join(advanced_dst, entry)
            if os.path.isfile(src) and entry.endswith(".md"):
                shutil.copy2(src, dst)
                print(f"    • copied file: advanced/{entry}")
                if entry.lower() == "index.md":
                    # Rewrite relative .md links in the index to add basics/ or
                    # deep-dives/ prefix. URL-encoded paths (e.g. 01%20...) need
                    # special handling because the space-in-folder-name is encoded.
                    import re
                    def _fix(href):
                        if href.startswith("Advanced%20Manual/"):
                            return "basics/" + href
                        parts = href.split("/", 1)
                        if len(parts) == 2 and re.match(r"^0[0-9]%20", parts[0]):
                            return "deep-dives/" + href
                        return href
                    txt = open(dst, "r", encoding="utf-8").read()
                    new = re.sub(r"\]\(([^)]+\.md)\)", lambda m: "](" + _fix(m.group(1)) + ")", txt)
                    if new != txt:
                        open(dst, "w", encoding="utf-8").write(new)
                        print(f"      • rewrote relative links in index.md")
    else:
        print(f"    ! WARNING: Advanced source not found: {advanced_src}")

    # 4b. Elite: split into basics/ (Elite Manual) + deep-dives/ (13 numbered modules)
    #     Mirrors the Advanced split above but with the Elite folder names.
    ELITE_BASICS_NAMES = ["Elite Manual"]
    ELITE_DEEP_DIVES_NAMES = [
        "01 The Anti-Orthodox Manifesto",
        "02 Trương Lực",
        "03 Myelination",
        "04 The Three Models",
        "05 Pressure Inoculation",
        "06 Kình and Mushin",
        "07 Constraint-Led Self-Discovery",
        "08 Hidden Speed",
        "09 Decision Latency",
        "10 Self-Coaching Discipline",
        "11 HRV Dashboard",
        "12 Choking and Amygdala",
        "13 The Dream Library",
    ]
    elite_src = os.path.join(DOCS_BASE, "Elite")
    if os.path.isdir(elite_src):
        print(f"\n[4b] Copying Elite with basics/deep-dives split")
        elite_dst = os.path.join(TARGET_DOCS, "elite")
        os.makedirs(elite_dst, exist_ok=True)
        # basics/
        for name in ELITE_BASICS_NAMES:
            src = os.path.join(elite_src, name)
            dst = os.path.join(elite_dst, "basics", name)
            if os.path.isdir(src):
                copy_tree(src, dst, f"elite/basics/{name}")
        # deep-dives/
        for name in ELITE_DEEP_DIVES_NAMES:
            src = os.path.join(elite_src, name)
            dst = os.path.join(elite_dst, "deep-dives", name)
            if os.path.isdir(src):
                copy_tree(src, dst, f"elite/deep-dives/{name}")
        # Loose .md / .html files at the source root stay at the destination root
        # (index.md, Readme.html, ReadMe.md). For .md files with relative links,
        # rewrite them to add basics/ or deep-dives/ prefix.
        for entry in os.listdir(elite_src):
            src = os.path.join(elite_src, entry)
            dst = os.path.join(elite_dst, entry)
            if not os.path.isfile(src):
                continue
            shutil.copy2(src, dst)
            print(f"    • copied file: elite/{entry}")
            if entry.lower() == "index.md" or entry.lower() == "readme.md":
                import re
                def _fix(href):
                    if href.startswith("Elite%20Manual/"):
                        return "basics/" + href
                    parts = href.split("/", 1)
                    # Elite uses 01-13 (not 01-08 like Advanced)
                    if len(parts) == 2 and re.match(r"^[0-9]{2}%20", parts[0]):
                        return "deep-dives/" + href
                    return href
                txt = open(dst, "r", encoding="utf-8").read()
                new = re.sub(r"\]\(([^)]+)\)", lambda m: "](" + _fix(m.group(1)) + ")", txt)
                if new != txt:
                    open(dst, "w", encoding="utf-8").write(new)
                    print(f"      • rewrote relative links in {entry}")
    else:
        print(f"    ! WARNING: Elite source not found: {elite_src}")

    # 4c. The remaining 2 subsites (anatomy-lab, angle-atlas) are flat → flat.
    for label, src in SUBSITE_SOURCES:
        if label in ("advanced", "elite"):
            continue  # already handled in 4a / 4b
        dst = os.path.join(TARGET_DOCS, label)
        copy_tree(src, dst, label)

    # 5. Summary
    print(f"\n[5] Summary")
    total_size = sizeof_mb(TARGET)
    print(f"    Total target size: {total_size:.1f} MB")
    # Advanced now has basics/ + deep-dives/ sub-tree
    p = os.path.join(TARGET_DOCS, "advanced")
    if os.path.exists(p):
        files = sum(len(files) for _, _, files in os.walk(p))
        basics = os.path.join(p, "basics")
        basics_files = sum(len(files) for _, _, files in os.walk(basics)) if os.path.isdir(basics) else 0
        deep = os.path.join(p, "deep-dives")
        deep_files = sum(len(files) for _, _, files in os.walk(deep)) if os.path.isdir(deep) else 0
        print(f"    advanced       : {sizeof_mb(p):6.1f} MB, {files:4d} files (basics: {basics_files}, deep-dives: {deep_files})")
    for sub in ["anatomy-lab", "angle-atlas"]:
        p = os.path.join(TARGET_DOCS, sub)
        if os.path.exists(p):
            files = sum(len(files) for _, _, files in os.walk(p))
            print(f"    {sub:15s}: {sizeof_mb(p):6.1f} MB, {files:4d} files")
    # Elite now has basics/ + deep-dives/ sub-tree
    p = os.path.join(TARGET_DOCS, "elite")
    if os.path.exists(p):
        files = sum(len(files) for _, _, files in os.walk(p))
        basics = os.path.join(p, "basics")
        basics_files = sum(len(files) for _, _, files in os.walk(basics)) if os.path.isdir(basics) else 0
        deep = os.path.join(p, "deep-dives")
        deep_files = sum(len(files) for _, _, files in os.walk(deep)) if os.path.isdir(deep) else 0
        print(f"    elite          : {sizeof_mb(p):6.1f} MB, {files:4d} files (basics: {basics_files}, deep-dives: {deep_files})")
    # Foundation now has basics/ + deep-dives/ sub-tree
    p = os.path.join(TARGET_DOCS, "foundation")
    if os.path.exists(p):
        files = sum(len(files) for _, _, files in os.walk(p))
        basics = os.path.join(p, "basics")
        basics_files = sum(len(files) for _, _, files in os.walk(basics)) if os.path.isdir(basics) else 0
        deep = os.path.join(p, "deep-dives")
        deep_files = sum(len(files) for _, _, files in os.walk(deep)) if os.path.isdir(deep) else 0
        print(f"    foundation     : {sizeof_mb(p):6.1f} MB, {files:4d} files (basics: {basics_files}, deep-dives: {deep_files})")
    print(f"\nDone. Target: {TARGET}")
    print("Next steps: regenerate mkdocs.yml (python _gen_mkdocs.py), then mkdocs build.")

if __name__ == "__main__":
    main()
