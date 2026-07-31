import requests
import re
from pathlib import Path
import time

# Chapter slugs from EN landing page (match live URLs)
chapters = [
    ("01", "chapter-01-theproblem"),
    ("02", "chapter-02-thetool"),
    ("03", "chapter-03-theprecision"),
    ("04", "chapter-04-theoutcome"),
    ("05", "chapter-05-theenergystore"),
    ("06", "chapter-06-thetransmission"),
    ("07", "chapter-07-thecoresystem"),
    ("08", "chapter-08-quieteye"),
    ("09", "chapter-09-vestibularstabilityvormanagement"),
    ("10", "chapter-10-fasciaproprioception"),
    ("11", "chapter-11-tensegrity"),
    ("12", "chapter-12-stretchshorteningcycle"),
    ("13", "chapter-13-figure8regulation"),
    ("14", "chapter-14-45degreeswingplane"),
    ("15", "chapter-15-brakingimpulse"),
    ("16", "chapter-16-jin"),
    ("17", "chapter-17-huthucfootwork"),
    ("18", "chapter-18-rooting"),
    ("19", "chapter-19-forehpushsystem"),
    ("20", "chapter-20-onehedbackhsaber"),
    ("21", "chapter-21-twohedbackhhybrid"),
    ("22", "chapter-22-serve"),
    ("23", "chapter-23-returnofserve"),
    ("24", "chapter-24-volleyoverhead"),
    ("25", "chapter-25-slicedropshotlob"),
    ("26", "chapter-26-courtgeometryshotselection"),
    ("27", "chapter-27-singlespatternsdoublessystems"),
    ("28", "chapter-28-mental"),
    ("29", "chapter-29-physical"),
    ("30", "chapter-30-theunifiedsystem"),
]

base_url = "https://tenniskb.github.io/tenniskb/en/chuong/"
out_dir = Path(r"C:\Users\Henry\Documents\Github Repos\tenniskb.github.io\tenniskb\en\chuong")
out_dir.mkdir(parents=True, exist_ok=True)

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

for num, slug in chapters:
    url = f"{base_url}{slug}/"
    print(f"Downloading Chapter {num}: {slug} ...", end=" ", flush=True)
    try:
        r = session.get(url, timeout=30)
        if r.status_code == 200:
            html = r.text
            # Fix image paths: C1-A2.png -> ../../assets/images/C1-A2.jpg
            html = re.sub(r'src="C(\d+)-A(\d+)\.png"', r'src="../../assets/images/C\1-A\2.jpg"', html)
            html = re.sub(r'src="C(\d+)-A(\d+)\.jpg"', r'src="../../assets/images/C\1-A\2.jpg"', html)
            
            chapter_dir = out_dir / slug
            chapter_dir.mkdir(parents=True, exist_ok=True)
            (chapter_dir / "index.html").write_text(html, encoding="utf-8")
            print("OK")
        else:
            print(f"FAIL {r.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")
    time.sleep(0.5)

print("\nDone!")