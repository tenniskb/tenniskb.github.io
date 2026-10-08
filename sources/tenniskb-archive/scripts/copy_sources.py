#!/usr/bin/env python3
"""Copy 30 .md files from Manus Papers source to en/docs/ and vi/docs/ with clean English slugs."""
import os
import shutil
import unicodedata
import re

SRC = r"C:\Users\Henry\Documents\MY VAULT\Documents\New Tennis Knowledge\Manus Papers"
DST = r"C:\Users\Henry\Downloads\Tenniskb\tenniskb_fresh"

# Map each source filename to (language, slug, topic_group, title)
# topic_group values: forehand, backhand, serve, volley, split-step, movement, contact, control-theory, momentum, left-arm, head-balance, stance, wave, modern, synthesis, coaching
FILES = [
    # === ENGLISH (17 files) ===
    ("Eliteonehandedbackhand.md", "en", "Elite-One-Handed-Backhand", "backhand", "Elite One-Handed Backhand"),
    ("Biomechanical Analysis of the One-Handed Backhand in Elite Tennis_ Dimitrov, Wawrinka, and Federer.md", "en", "One-Handed-Backhand-Dimitrov-Wawrinka-Federer", "backhand", "One-Handed Backhand: Dimitrov, Wawrinka, Federer"),
    ("Elite splitstep.md", "en", "Elite-Split-Step", "split-step", "Elite Split Step"),
    ("The Biomechanics and Neurological Control of the Tennis Split Step.md", "en", "Split-Step-Biomechanics-Neurological-Control", "split-step", "Split Step: Biomechanics & Neurological Control"),
    ("Momentum in tennis.md", "en", "Momentum-in-Tennis", "momentum", "Momentum in Tennis"),
    ("The role of left arm in tennis.md", "en", "Role-of-the-Left-Arm", "left-arm", "Role of the Left Arm in Tennis"),
    ("The Contact Point Architecture Framework in Tennis_ A Neurological Control Perspective.md", "en", "Contact-Point-Architecture-Framework", "contact", "Contact Point Architecture Framework"),
    ("Comprehensive Analysis_ Feedforward and Feedback Control Systems in Tennis Biomechanics.md", "en", "Feedforward-Feedback-Control-Systems", "control-theory", "Feedforward & Feedback Control Systems"),
    ("Comprehensive Analysis_ Integrated Pro System (IPS) Tennis Techniques through the Lens of Industrial Control Systems.md", "en", "Integrated-Pro-System-IPS", "control-theory", "Integrated Pro System (IPS)"),
    ("Biomechanics of Tennis Movement_ A Neurological and Comparative Analysis.md", "en", "Tennis-Movement-Biomechanics-Comparative", "movement", "Tennis Movement: Biomechanics & Comparative Analysis"),
    ("Biomechanics Research Report_ Wave Generation and Neurological Control in Tennis.md", "en", "Wave-Generation-Neurological-Control", "wave", "Wave Generation & Neurological Control"),
    ("Biomechanical Control Analysis Report_ Elite Tennis Techniques.md", "en", "Elite-Tennis-Techniques-Control-Analysis", "control-theory", "Elite Tennis Techniques: Control Analysis"),
    ("Biomechanical Control Analysis Report_ The Art of Volley Direction Change.md", "en", "Volley-Direction-Change-Control-Analysis", "volley", "Volley Direction Change: Control Analysis"),
    ("Tennis_Control_System_Manual_Final.md", "en", "Tennis-Control-System-Manual", "control-theory", "Tennis Control System Manual"),
    ("Total framework for stroke analysis.md", "en", "Total-Framework-for-Stroke-Analysis", "control-theory", "Total Framework for Stroke Analysis"),
    ("Tennis_Biomechanics_Key_Insights_Synthesis.md", "en", "Tennis-Biomechanics-Key-Insights-Synthesis", "synthesis", "Tennis Biomechanics: Key Insights Synthesis"),
    # === VIETNAMESE (13 files) ===
    ("Phân Tích Sinh Cơ Học Cú Trái Tay Một Tay Trong Quần Vợt Đỉnh Cao_ Dimitrov, Wawrinka và Federer.md", "vi", "Phan-Tich-Trai-Tay-Mot-Tay-Dimitrov-Wawrinka-Federer", "backhand", "Phân Tích Trái Tay Một Tay: Dimitrov, Wawrinka, Federer"),
    ("Phân tích Cơ sinh học và Kiểm soát Thần kinh của Kỹ thuật Split Step trong Tennis.md", "vi", "Phan-Tich-Split-Step-Co-Sinh-Hoc-Than-Kinh", "split-step", "Phân Tích Split Step: Cơ Sinh Học & Thần Kinh"),
    ("Phân Tích Sinh Cơ Học Forehand Tennis.md", "vi", "Phan-Tich-Sinh-Co-Hoc-Forehand", "forehand", "Phân Tích Sinh Cơ Học Forehand"),
    ("Báo cáo so sánh hai động cơ tạo lực trong cú thuận tay Tennis.md", "vi", "Bao-Cao-So-Sanh-Hai-Dong-Co-Tao-Luc-Thuan-Tay", "forehand", "Báo Cáo: So Sánh Hai Động Cơ Tạo Lực Thuận Tay"),
    ("Kỹ thuật giao bóng.md", "vi", "Ky-Thuat-Giao-Bong", "serve", "Kỹ Thuật Giao Bóng"),
    ("Cẩm nang chuyên sâu về Volley (Phiên bản nâng cao).md", "vi", "Cam-Nang-Chuyen-Sau-Volley-Nang-Cao", "volley", "Cẩm Nang Chuyên Sâu Về Volley (Nâng Cao)"),
    ("Chuyên Sâu về Kỹ Thuật _Carving_ và Quản Lý _Underspin_ trong Volley Hiện Đại.md", "vi", "Chuyen-Sau-Ky-Thuat-Carving-Underspin-Volley", "volley", "Kỹ Thuật Carving & Quản Lý Underspin Trong Volley"),
    ("Cáchgậpgốivàelbow.md", "vi", "Cach-Gap-Gop-Va-Elbow", "movement", "Cách Gập Gối & Elbow"),
    ("Khung Kiến Trúc Điểm Tiếp Xúc trong Quần Vợt_ Một Góc Nhìn Từ Lý Thuyết Điều Khiển Thần Kinh.md", "vi", "Khung-Kien-Truc-Diem-Tiep-Xuc", "contact", "Khung Kiến Trúc Điểm Tiếp Xúc"),
    ("Vị Trí Đầu và Hệ Thống Thăng Bằng_ Phân Tích Chuyên Sâu.md", "vi", "Vi-Tri-Dau-He-Thong-Thang-Bang", "head-balance", "Vị Trí Đầu & Hệ Thống Thăng Bằng"),
    ("Phân Tích So Sánh Sinh Cơ Học_ Tư Thế Mở (Open Stance) và Tư Thế Đóng (Closed Stance) trong Tennis.md", "vi", "Phan-Tich-So-Sanh-Tu-The-Mo-Dong", "stance", "So Sánh Tư Thế Mở & Tư Thế Đóng"),
    ("Tạo sóng trong tennis.md", "vi", "Tao-Song-Trong-Tennis", "wave", "Tạo Sóng Trong Tennis"),
    ("Hướng dẫn Huấn luyện Hệ thống Điều khiển Tennis cho Người chơi NTRP 3.5.md", "vi", "NTRP-3-5-He-Thong-Dieu-Khien-Tennis", "coaching", "Hệ Thống Điều Khiển Tennis Cho NTRP 3.5"),
]

def slugify(name: str) -> str:
    # Convert Vietnamese filename to ASCII slug suitable for URL
    # First, manual replacements for common Vietnamese diacritics
    repl = {
        'ạ':'a','ả':'a','ã':'a','à':'a','á':'a','ă':'a','ặ':'a','ằ':'a','ẳ':'a','ẵ':'a','ắ':'a',
        'â':'a','ậ':'a','ầ':'a','ẩ':'a','ẫ':'a','ấ':'a',
        'đ':'d','Đ':'d',
        'ẹ':'e','ẻ':'e','ẽ':'e','è':'e','é':'e','ê':'e','ệ':'e','ề':'e','ể':'e','ễ':'e','ế':'e',
        'ị':'i','ỉ':'i','ĩ':'i','ì':'i','í':'i',
        'ọ':'o','ỏ':'o','õ':'o','ò':'o','ó':'o','ô':'o','ộ':'o','ồ':'o','ổ':'o','ỗ':'o','ố':'o',
        'ơ':'o','ợ':'o','ờ':'o','ở':'o','ỡ':'o','ớ':'o',
        'ụ':'u','ủ':'u','ũ':'u','ù':'u','ú':'u','ư':'u','ự':'u','ừ':'u','ử':'u','ữ':'u','ứ':'u',
        'ỳ':'y','ỷ':'y','ỹ':'y','ý':'y','ỵ':'y',
    }
    s = name
    for k,v in repl.items():
        s = s.replace(k, v)
        s = s.replace(k.upper(), v)
    # Normalize and strip non-ASCII
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore').decode('ascii')
    s = re.sub(r'[^A-Za-z0-9]+', '-', s).strip('-').lower()
    return s

print(f"Total files: {len(FILES)}")
en_count = sum(1 for f in FILES if f[1] == 'en')
vi_count = sum(1 for f in FILES if f[1] == 'vi')
print(f"EN: {en_count}, VI: {vi_count}")

# Copy each file to en/docs/<slug>.md or vi/docs/<slug>.md
copied = 0
for fname, lang, slug, group, title in FILES:
    src_path = os.path.join(SRC, fname)
    if not os.path.exists(src_path):
        print(f"  MISSING: {fname}")
        continue
    # Final slug — use the pre-defined one for consistency
    final_slug = slug.lower()
    dst_path = os.path.join(DST, lang, 'docs', f"{final_slug}.md")
    shutil.copy2(src_path, dst_path)
    copied += 1
    print(f"  [{lang}] {final_slug}.md  <-  {fname[:60]}...")

print(f"\nCopied {copied} files")
