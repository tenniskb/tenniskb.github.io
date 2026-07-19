"""
Smart bilingual split: read each .md file under docs/foundation/{basics,deep-dives}/
and produce two files (en/ and vi/) per input. Per user's "Smart split" choice:

  SPLIT (write to BOTH files, take the relevant half):
    - Tables:        `| EN | VI |` -> 1-column tables, EN col 1, VI col 2
    - Headings:      `## Foo | Bar` -> EN gets "Foo", VI gets "Bar"
    - Italics:       `*Foo | Bar*`  -> EN/VI
    - Blockquote:    `> Foo | Bar` -> EN/VI (preserve "> " prefix)

  KEEP BILINGUAL (write the same line to BOTH files):
    - Plain paragraphs (no `|`)
    - Code blocks, images, dividers (`---`)
    - Lists (numbered or bulleted, including ones with `|` in them? NO, lists
      with `|` are blockquote-style callouts. We split callout-style lists
      too IF they have the `|` separator.)
    - Frontmatter
    - Empty lines

Special case: lines that look like list items but contain `|` (e.g. `- Foo | Bar`).
Treat them as a split: write `- EN half` to EN, `- VI half` to VI.

Idempotency: refuses to run if tenniskb-new/en/foundation/ already exists.
"""
import os
import re
import shutil
import sys

# Source (tenniskb-foundation/docs) and destination (tenniskb-new) roots
SRC_BASE = r"C:\Users\Henry\GITHUB\tenniskb-foundation\docs"
SRC = os.path.join(SRC_BASE, "foundation")  # default, overridden per subsite
DST = r"C:\Users\Henry\GITHUB\tenniskb-new"

# Subsites to split. Add new ones here as needed.
# Each: (subsite_name, source_subdir_in_tenniskb-foundation, sub_trees)
# sub_trees: list of sub-directory names to recurse into, or None for flat
# (flat = all .md files are at the subsite root, no nested sub-trees)
SUBSITES = [
    ("foundation",   "foundation",   ["basics", "deep-dives"]),
    ("advanced",     "advanced",     ["basics", "deep-dives"]),
    ("elite",        "elite",        ["basics", "deep-dives"]),
    ("anatomy-lab",  "anatomy-lab",  None),  # flat
    ("angle-atlas",  "angle-atlas",  None),  # flat
]


# (kept for backward compat — the first subsite, used by some test scripts)
SUBSITE = SUBSITES[0][0]

def info(msg): print(f"  • {msg}")
def ok(msg):   print(f"  ✓ {msg}")
def warn(msg): print(f"  ! WARNING: {msg}")
def die(msg):
    print(f"  ✗ ABORT: {msg}", file=sys.stderr)
    sys.exit(1)


def split_pipe_segment(text):
    """
    Split a single line / cell on the FIRST ' | ' (space-pipe-space) separator.
    Returns (left, right). If no separator, returns (text, text) — i.e., the
    line is bilingual-equivalent and we keep it in both.

    For HEADING lines (starting with #), preserve the leading "#" / "##" / etc.
    marker in BOTH outputs so the heading structure is preserved.
    """
    m = re.search(r' \| ', text)
    if m:
        left = text[:m.start()].rstrip()
        right = text[m.end():].lstrip()
        # Preserve heading marker in both
        h_match = re.match(r'^(#{1,6}\s+)(.*)$', left)
        if h_match:
            marker = h_match.group(1)
            rest_en = h_match.group(2)
            # For VI: prepend the marker (the VI text doesn't have one)
            return left, f"{marker}{right}" if not right.startswith("#") else right
        return left, right
    return text, text


def is_table_separator(line):
    """`| --- | --- |` or `|---|---|` — the markdown table separator row."""
    s = line.strip()
    if not s.startswith("|") or not s.endswith("|"):
        return False
    cells = [c.strip() for c in s.strip("|").split("|")]
    return all(re.fullmatch(r":?-{3,}:?", c) for c in cells)


def is_table_row(line):
    """A markdown table row: starts with `|`, has at least one more `|`."""
    s = line.lstrip()
    return s.startswith("|") and s.count("|") >= 2


def is_en_vi_header(line):
    """
    Detect a 2-col EN-VI table header: contains both an English marker AND a
    Vietnamese marker in adjacent cells. Markers:
      - English: "English", "🇺🇸"
      - Vietnamese: "Tiếng Việt", "Vietnamese", "🇻🇳"
    Returns True if the line is a 2-col table with both markers present.
    """
    s = line.strip()
    if not s.startswith("|") or not s.endswith("|"):
        return False
    cells = [c.strip() for c in s.strip("|").split("|")]
    if len(cells) != 2:
        return False
    en_markers = ("english", "🇺🇸")
    vi_markers = ("tiếng việt", "vietnamese", "🇻🇳")
    has_en = any(m in cells[0].lower() or m in cells[1].lower() for m in en_markers)
    has_vi = any(m in cells[0].lower() or m in cells[1].lower() for m in vi_markers)
    return has_en and has_vi


def split_table_row(line, split_2col=True):
    """
    Split a table row like `| EN | VI |` into 1-column rows.
    EN version: `| EN |`, VI version: `| VI |`.
    If split_2col is False, keep the row as-is in BOTH files (used for
    3+ col tables that are not EN-VI translations).
    """
    s = line.strip()
    if not s.startswith("|") or not s.endswith("|"):
        return line, line
    cells = [c.strip() for c in s.strip("|").split("|")]
    if len(cells) < 2:
        return line, line
    if not split_2col:
        return line, line
    # 2-col: EN gets col 0, VI gets col 1
    if len(cells) == 2:
        return f"| {cells[0]} |", f"| {cells[1]} |"
    # 3+ col without EN-VI marker: keep as-is in both
    return line, line


def make_table_separator_one_col(line):
    """Convert `| --- | --- |` to `| --- |` (1-column)."""
    s = line.strip()
    if not s.startswith("|") or not s.endswith("|"):
        return line
    cells = [c.strip() for c in s.strip("|").split("|")]
    if len(cells) != 2:
        return line
    first = cells[0] if cells[0] else "---"
    return f"| {first} |"


def is_list_item(line):
    """`- foo`, `* foo`, `1. foo`, `#### foo` (used as a 4-level sub-heading)."""
    return bool(re.match(r'^\s*([-*]|\d+\.)\s', line))


def is_horizontal_rule(line):
    return line.strip() in ("---", "***", "___")


def is_code_fence(line):
    return line.strip().startswith("```")


def split_file(text):
    """
    Main split logic. Iterate line by line, tracking whether we're inside:
      - a code block (preserve verbatim)
      - a table (split per-row, with a 1-column separator)

    For non-table, non-code lines:
      - lines with ` | ` get split (headings, blockquotes, italics, etc.)
      - lines without ` | ` are kept bilingual (copied verbatim to both)
    """
    en_lines = []
    vi_lines = []
    in_code = False
    in_table = False
    table_is_en_vi = False  # is the current table a 2-col EN-VI parallel?

    for raw_line in text.split("\n"):
        # Code block: pass through verbatim, toggle state
        if is_code_fence(raw_line):
            in_code = not in_code
            in_table = False
            table_is_en_vi = False
            en_lines.append(raw_line)
            vi_lines.append(raw_line)
            continue

        if in_code:
            en_lines.append(raw_line)
            vi_lines.append(raw_line)
            continue

        # Table region handling
        if is_table_row(raw_line):
            # If this is the FIRST row of a table, check if it's a 2-col EN-VI
            if not in_table:
                table_is_en_vi = is_en_vi_header(raw_line)
            en_row, vi_row = split_table_row(raw_line, split_2col=table_is_en_vi)
            en_lines.append(en_row)
            vi_lines.append(vi_row)
            in_table = True
            continue
        elif in_table and not raw_line.strip():
            # Blank line ends the table
            en_lines.append(raw_line)
            vi_lines.append(raw_line)
            in_table = False
            table_is_en_vi = False
            continue
        elif in_table and is_table_separator(raw_line):
            # Convert 2-col separator to 1-col (same for both files)
            if table_is_en_vi:
                sep = make_table_separator_one_col(raw_line)
            else:
                sep = raw_line  # keep 3+ col separator as-is
            en_lines.append(sep)
            vi_lines.append(sep)
            continue
        else:
            in_table = False
            table_is_en_vi = False

        # Now: non-table, non-code line.
        # Decide if it's a "split" line (has " | " separator) or "keep" line.
        if " | " in raw_line:
            # Handle list items: `- Foo | Bar` -> `- EN half`, `- VI half`
            m = re.match(r'^(\s*[-*]|\s*\d+\.)\s+(.*)$', raw_line)
            if m:
                prefix = m.group(1)  # e.g. "- "
                rest = m.group(2)
                left, right = split_pipe_segment(rest)
                en_lines.append(f"{prefix}{left}")
                vi_lines.append(f"{prefix}{right}")
                continue
            # Headings (`# ... | ...`), blockquotes (`> ... | ...`), italics
            # (`*... | ...*`), plain text with ` | ` — all split the same way.
            left, right = split_pipe_segment(raw_line)
            en_lines.append(left)
            vi_lines.append(right)
            continue
        # Lines WITHOUT ` | ` separator
        # Special case: heading marker must be preserved in BOTH files
        # Special case: blockquote lines — we need to detect "this block is a
        # 2-paragraph callout: EN paragraph then blank then VI paragraph" and
        # split those into EN-only and VI-only files. But this requires
        # looking ahead, which is harder. Skip for now: keep blockquotes
        # bilingual (same content in both files).
        else:
            # No separator — keep bilingual
            en_lines.append(raw_line)
            vi_lines.append(raw_line)

    return "\n".join(en_lines), "\n".join(vi_lines)


def split_subsite(src_root, dst_root, subsite, src_subdir, sub_trees):
    """
    Walk src_root/<sub_trees>*/<module>/<file>.md, split each,
    write to dst_root/{en,vi}/<subsite>/<sub>/<module>/<file>.md

    If sub_trees is None, the subsite is FLAT: .md files are at the root of
    src_root/. In that case, we copy each .md file directly to the lang dir.
    """
    files_split = 0
    bytes_en = 0
    bytes_vi = 0

    if sub_trees is None:
        # FLAT subsite: .md files at the root
        for fname in sorted(os.listdir(src_root)):
            if not fname.endswith(".md"):
                continue
            src_path = os.path.join(src_root, fname)
            en_path = os.path.join(dst_root, "en", subsite, fname)
            vi_path = os.path.join(dst_root, "vi", subsite, fname)

            with open(src_path, "r", encoding="utf-8") as f:
                text = f.read()
            en_text, vi_text = split_file(text)

            os.makedirs(os.path.dirname(en_path), exist_ok=True)
            os.makedirs(os.path.dirname(vi_path), exist_ok=True)
            with open(en_path, "w", encoding="utf-8") as f:
                f.write(en_text)
            with open(vi_path, "w", encoding="utf-8") as f:
                f.write(vi_text)

            files_split += 1
            bytes_en += len(en_text)
            bytes_vi += len(vi_text)
            info(f"split (flat) {fname}  ({len(text):,} -> EN: {len(en_text):,}, VI: {len(vi_text):,})")
        return files_split, bytes_en, bytes_vi

    # NESTED subsite: <sub_trees>/<module>/<file>.md
    for sub in sub_trees:
        src_dir = os.path.join(src_root, sub)
        if not os.path.isdir(src_dir):
            info(f"skip {sub}/: not found in source")
            continue
        for module in sorted(os.listdir(src_dir)):
            src_mod = os.path.join(src_dir, module)
            if not os.path.isdir(src_mod):
                continue
            for fname in sorted(os.listdir(src_mod)):
                if not fname.endswith(".md"):
                    continue
                src_path = os.path.join(src_mod, fname)
                en_path = os.path.join(dst_root, "en", subsite, sub, module, fname)
                vi_path = os.path.join(dst_root, "vi", subsite, sub, module, fname)

                with open(src_path, "r", encoding="utf-8") as f:
                    text = f.read()
                en_text, vi_text = split_file(text)

                os.makedirs(os.path.dirname(en_path), exist_ok=True)
                os.makedirs(os.path.dirname(vi_path), exist_ok=True)
                with open(en_path, "w", encoding="utf-8") as f:
                    f.write(en_text)
                with open(vi_path, "w", encoding="utf-8") as f:
                    f.write(vi_text)

                files_split += 1
                bytes_en += len(en_text)
                bytes_vi += len(vi_text)
                info(f"split {sub}/{module}/{fname}  ({len(text):,} -> EN: {len(en_text):,}, VI: {len(vi_text):,})")
    return files_split, bytes_en, bytes_vi


def main():
    if not os.path.isdir(SRC_BASE):
        die(f"source not found: {SRC_BASE}")
    if not os.path.isdir(DST):
        die(f"destination not found: {DST}")

    total_files = 0
    total_en = 0
    total_vi = 0

    for subsite, src_subdir, sub_trees in SUBSITES:
        subsite_src = os.path.join(SRC_BASE, src_subdir)
        if not os.path.isdir(subsite_src):
            warn(f"skip {subsite}: source not found at {subsite_src}")
            continue
        print(f"\n=== Smart bilingual split: {subsite} ===")
        print(f"    Source: {subsite_src}/")
        print(f"    Dest:   {DST}/{{en,vi}}/{subsite}/")
        print()

        en_dst = os.path.join(DST, "en", subsite)
        vi_dst = os.path.join(DST, "vi", subsite)
        if os.path.isdir(en_dst):
            warn(f"skip {subsite}: {en_dst} already exists (already split)")
            continue
        if os.path.isdir(vi_dst):
            warn(f"skip {subsite}: {vi_dst} already exists (already split)")
            continue

        files, en_bytes, vi_bytes = split_subsite(subsite_src, DST, subsite, src_subdir, sub_trees)
        ok(f"  {subsite}: split {files} files (EN: {en_bytes/1024:.0f} KB, VI: {vi_bytes/1024:.0f} KB)")
        total_files += files
        total_en += en_bytes
        total_vi += vi_bytes

        # Copy images/ and assets/ sidecar folders so image references resolve.
        # Only the EN side gets the actual files; VI gets a copy too (images are
        # language-neutral — both EN and VI HTMLs reference the same image).
        for sidecar in ("images", "assets"):
            src_sidecar = os.path.join(subsite_src, sidecar)
            if not os.path.isdir(src_sidecar):
                continue
            for lang in ("en", "vi"):
                dst_sidecar = os.path.join(DST, lang, subsite, sidecar)
                if os.path.isdir(dst_sidecar):
                    continue  # already copied
                shutil.copytree(src_sidecar, dst_sidecar)
                n = sum(len(files) for _, _, files in os.walk(dst_sidecar))
                size_mb = sum(os.path.getsize(os.path.join(r, f)) for r, _, files in os.walk(dst_sidecar) for f in files) / 1024 / 1024
                ok(f"    {lang}/{subsite}/{sidecar}/: {n} files, {size_mb:.1f} MB")

    print()
    ok(f"=== TOTAL: split {total_files} files across {len(SUBSITES)} subsites")
    ok(f"  EN grand total: {total_en:,} bytes ({total_en/1024:.0f} KB)")
    ok(f"  VI grand total: {total_vi:,} bytes ({total_vi/1024:.0f} KB)")
    print()
    print("=== Done. Next: write a small mkdocs.yml and build a single sub-site to verify. ===")

if __name__ == "__main__":
    main()
