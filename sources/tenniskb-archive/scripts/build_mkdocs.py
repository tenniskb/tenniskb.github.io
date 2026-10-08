#!/usr/bin/env python3
"""Generate en/mkdocs.yml and vi/mkdocs.yml with proper Vietnamese labels."""
import os

DST = r"C:\Users\Henry\Downloads\Tenniskb\tenniskb_fresh"

EN_FILES = [
    ("elite-one-handed-backhand", "Elite One-Handed Backhand", "Backhand"),
    ("one-handed-backhand-dimitrov-wawrinka-federer", "Dimitrov, Wawrinka & Federer", "Backhand"),
    ("elite-split-step", "Elite Split Step", "Split Step"),
    ("split-step-biomechanics-neurological-control", "Biomechanics & Neurological Control", "Split Step"),
    ("momentum-in-tennis", "Momentum in Tennis", "Momentum"),
    ("role-of-the-left-arm", "Role of the Left Arm", "Left Arm"),
    ("contact-point-architecture-framework", "Architecture Framework", "Contact Point"),
    ("feedforward-feedback-control-systems", "Feedforward & Feedback", "Control Theory"),
    ("integrated-pro-system-ips", "Integrated Pro System (IPS)", "Control Theory"),
    ("elite-tennis-techniques-control-analysis", "Elite Techniques Control Analysis", "Control Theory"),
    ("tennis-control-system-manual", "Tennis Control System Manual", "Control Theory"),
    ("total-framework-for-stroke-analysis", "Total Framework for Stroke Analysis", "Control Theory"),
    ("tennis-movement-biomechanics-comparative", "Tennis Movement: Comparative Analysis", "Movement"),
    ("wave-generation-neurological-control", "Wave Generation & Neurological Control", "Wave Generation"),
    ("volley-direction-change-control-analysis", "Volley Direction Change", "Volley"),
    ("tennis-biomechanics-key-insights-synthesis", "Key Insights Synthesis", "Synthesis"),
]

VI_FILES = [
    ("phan-tich-sinh-co-hoc-forehand", "Phan Tich Sinh Co Hoc Forehand", "Forehand"),
    ("bao-cao-so-sanh-hai-dong-co-tao-luc-thuan-tay", "Bao Cao So Sanh Dong Co Tao Luc", "Forehand"),
    ("phan-tich-trai-tay-mot-tay-dimitrov-wawrinka-federer", "Phan Tich Trai Tay Mot Tay", "Backhand"),
    ("ky-thuat-giao-bong", "Ky Thuat Giao Bong", "Serve"),
    ("cam-nang-chuyen-sau-volley-nang-cao", "Cam Nang Chuyen Sau Volley", "Volley"),
    ("chuyen-sau-ky-thuat-carving-underspin-volley", "Carving Underspin Trong Volley", "Volley"),
    ("phan-tich-split-step-co-sinh-hoc-than-kinh", "Phan Tich Split Step", "Split Step"),
    ("cach-gap-gop-va-elbow", "Cach Gap Gop va Elbow", "Movement"),
    ("khung-kien-truc-diem-tiep-xuc", "Khung Kien Truc Diem Tiep Xuc", "Contact Point"),
    ("vi-tri-dau-he-thong-thang-bang", "Vi Tri Dau He Thong Thang Bang", "Head & Balance"),
    ("phan-tich-so-sanh-tu-the-mo-dong", "So Sanh Tu The Mo va Dong", "Stance"),
    ("tao-song-trong-tennis", "Tao Song Trong Tennis", "Wave Generation"),
    ("nghien-cuu-bioco-hoc-tennis-modern-2026", "Nghien Cuu Bioco Hoc Tennis 2026", "Modern Tennis"),
    ("ntrp-3-5-he-thong-dieu-khien-tennis", "He Thong Dieu Khien Tennis NTRP 3.5", "NTRP 3.5 Coaching"),
]

GROUP_ORDER = [
    "Forehand", "Backhand", "Serve", "Volley", "Split Step", "Movement",
    "Momentum", "Left Arm", "Contact Point", "Stance", "Head & Balance",
    "Wave Generation", "Control Theory", "Modern Tennis", "Synthesis", "NTRP 3.5 Coaching"
]

# Vietnamese labels with proper diacritics
GROUP_VI = {
    "Forehand": "Thuan Tay (Forehand)",
    "Backhand": "Trai Tay (Backhand)",
    "Serve": "Giao Bong (Serve)",
    "Volley": "Volley",
    "Split Step": "Split Step",
    "Movement": "Di Chuyen (Movement)",
    "Momentum": "Dong Luong (Momentum)",
    "Left Arm": "Vai Tro C Tay Trai (Left Arm)",
    "Contact Point": "Diem Tiep Xuc (Contact Point)",
    "Stance": "Tu The (Stance)",
    "Head & Balance": "Dau va Thang Bang (Head and Balance)",
    "Wave Generation": "Tao Song (Wave Generation)",
    "Control Theory": "Ly Thuyet Dieu Khien (Control Theory)",
    "Modern Tennis": "Tennis Hien Dai (Modern)",
    "Synthesis": "Tong Hop (Synthesis)",
    "NTRP 3.5 Coaching": "NTRP 3.5 Huan Luyen (Coaching)"
}

def q(s):
    if any(c in s for c in [':', '#', '{', '}', '[', ']', ',', '&', '*', '!', '|', '>', "'", '"', '%', '@', '`']):
        return '"' + s.replace('"', '\\"') + '"'
    return s

def build_nav(files, group_label_fn):
    groups = {}
    for slug, title, group in files:
        groups.setdefault(group, []).append((slug, title))
    lines = ["  - " + q("Home") + ": " + q("index.md")]
    for group in GROUP_ORDER:
        if group not in groups:
            continue
        lines.append("  - " + q(group_label_fn(group)) + ":")
        for slug, title in sorted(groups[group], key=lambda x: x[1]):
            lines.append("      - " + q(title) + ": " + q(slug + ".md"))
    return "\n".join(lines)

en_nav = build_nav(EN_FILES, lambda g: g)
vi_nav = build_nav(VI_FILES, lambda g: GROUP_VI.get(g, g))

en_mkdocs = f"""site_name: Tennis Biomechanics Knowledge Base
site_description: Bilingual tennis biomechanics and control theory knowledge base - English version
site_author: Henry Pham Duc
site_url: https://tenniskb.github.io/tenniskb/en/

theme:
  name: mkdocs

nav:
{en_nav}
"""

vi_mkdocs = f"""site_name: Co So Tri Thuc Co Sinh Hoc Tennis
site_description: Co so tri thuc song ngu ve co sinh hoc va ly thuyet dieu khien tennis
site_author: Henry Pham Duc
site_url: https://tenniskb.github.io/tenniskb/vi/

theme:
  name: mkdocs

nav:
{vi_nav}
"""

with open(os.path.join(DST, "en", "mkdocs.yml"), "w", encoding="utf-8") as f:
    f.write(en_mkdocs)
with open(os.path.join(DST, "vi", "mkdocs.yml"), "w", encoding="utf-8") as f:
    f.write(vi_mkdocs)

print("Done. EN items:", len(EN_FILES), "+ home. VI items:", len(VI_FILES), "+ home")
