#!/usr/bin/env python3
"""Reformat KyThuat_TraiTay_MotTay_Clean.html to match VI sibling style (Mode B)."""

from bs4 import BeautifulSoup
from pathlib import Path
import re

SRC = Path(r"C:\Users\Henry\Documents\Github Repos\tenniskb.github.io\en\handbooks\KyThuat_TraiTay_MotTay_Clean.html")
VI_REF = Path(r"C:\Users\Henry\Documents\Github Repos\tenniskb.github.io\vi\cam-nang\tfl\KyThuat_TraiTay_MotTay_10Chuong.html")

def main():
    en_html = SRC.read_text(encoding='utf-8')
    vi_html = VI_REF.read_text(encoding='utf-8')
    
    # Extract VI styles manually from raw HTML
    vi_head_start = vi_html.find('<head>')
    vi_head_end = vi_html.find('</head>')
    vi_head_content = vi_html[vi_head_start:vi_head_end] if vi_head_start >= 0 and vi_head_end >= 0 else ""
    
    # Extract the <style> block
    style_match = re.search(r'<style>(.*?)</style>', vi_head_content, re.DOTALL)
    vi_style_css = style_match.group(1) if style_match else ""
    
    # Extract font links
    font_links = re.findall(r'<link[^>]*href="([^"]*fonts\.googleapis\.com[^"]*)"[^>]*>', vi_head_content)
    
    # Parse EN and transform
    en_soup = BeautifulSoup(en_html, 'html5lib')
    
    # 1. Update html lang
    en_soup.html['lang'] = 'en'
    
    # 2. Rebuild head with VI styles
    en_head = en_soup.head
    en_head.clear()
    
    # Meta
    en_head.append(BeautifulSoup('<meta charset="utf-8"/>', 'html5lib').meta)
    en_head.append(BeautifulSoup('<meta content="width=device-width, initial-scale=1.0" name="viewport"/>', 'html5lib').meta)
    
    # Title
    title = en_soup.new_tag('title')
    title.string = 'One-Handed Backhand Technique (1HBH) - Tennis Future Lab'
    en_head.append(title)
    
    # Font links from VI
    for href in font_links:
        link = en_soup.new_tag('link', href=href, rel="stylesheet")
        en_head.append(link)
    
    # VI styles
    style_tag = en_soup.new_tag('style')
    style_tag.string = vi_style_css
    en_head.append(style_tag)
    
    # 3. Restructure body
    en_body = en_soup.body
    
    # Find elements
    container = en_soup.find('div', class_='container')
    masthead = en_soup.find('div', class_='masthead')
    content_div = en_soup.find('div', class_='content')
    page_nav = en_soup.find('nav', class_='page-nav')
    
    # Extract masthead from container if inside
    if container and masthead and masthead.parent == container:
        masthead.extract()
    
    # Extract page_nav from content_div if inside
    if content_div and page_nav and page_nav.parent == content_div:
        page_nav.extract()
    
    # Create content-wrap
    content_wrap = en_soup.new_tag('div', **{'class': 'content-wrap'})
    if content_div:
        content_div.extract()
        content_wrap.append(content_div)
    
    # Clear body and rebuild: masthead -> content-wrap -> page-nav
    en_body.clear()
    if masthead:
        en_body.append(masthead)
    en_body.append(content_wrap)
    if page_nav:
        en_body.append(page_nav)
    
    # Remove container if still present
    if container:
        container.decompose()
    
    # 4. Update masthead
    masthead = en_soup.find('div', class_='masthead')
    if masthead:
        masthead['class'] = 'masthead'
        if 'style' in masthead.attrs:
            del masthead['style']
        # Rename brand-tag to tag to match VI
        brand_tag = masthead.find('span', class_='brand-tag')
        if brand_tag:
            brand_tag['class'] = 'tag'
        # Add subtitle div if missing
        h1 = masthead.find('h1')
        if h1 and not masthead.find(class_='subtitle'):
            # Add subtitle after h1
            subtitle = en_soup.new_tag('p', **{'class': 'subtitle'})
            subtitle.string = 'Biomechanics, Technique & Drills'
            h1.insert_after(subtitle)
    
    # 5. Update content div
    content_div = en_soup.find('div', class_='content')
    if content_div:
        content_div['class'] = 'content'
    
    # 6. Fix navigation classes
    page_nav = en_soup.find('nav', class_='page-nav')
    if page_nav:
        page_nav['class'] = 'page-nav'
        for a in page_nav.find_all('a'):
            text = a.get_text().strip().lower()
            new_classes = []
            if 'trước' in text or 'prev' in text:
                new_classes = ['nav-btn', 'prev']
            elif 'mục lục' in text or 'table' in text or 'toc' in text:
                new_classes = ['nav-btn', 'toc']
            elif 'sau' in text or 'next' in text:
                new_classes = ['nav-btn', 'next']
            if new_classes:
                a['class'] = new_classes
    
    # 7. Fix footer - use VI-style footer
    footer = en_soup.find('footer')
    if footer:
        footer.decompose()
    footer_div = en_soup.find('div', class_='footer')
    if footer_div:
        footer_div.decompose()
    
    # Create new footer matching VI
    footer = en_soup.new_tag('footer')
    p = en_soup.new_tag('p', style="margin: 4px 0;")
    credit_label = en_soup.new_tag('span', **{'class': 'credit-label'})
    credit_label.string = 'Created by'
    strong = en_soup.new_tag('strong')
    strong.string = 'Henry Pham, Tennis Future Lab'
    a = en_soup.new_tag('a', href="https://creativecommons.org/licenses/by-nc-sa/4.0/", rel="noopener", target="_blank")
    a.string = 'Creative Commons BY-NC-SA 4.0'
    
    p.append(credit_label)
    p.append(' ')
    p.append(strong)
    p.append(' under ')
    p.append(a)
    p.append('.')
    footer.append(p)
    en_body.append(footer)
    
    # 8. Update lead paragraph style
    content_div = en_soup.find('div', class_='content')
    if content_div:
        lead = content_div.find('p', class_='lead')
        if lead:
            lead['class'] = 'lead'
    
    # Backup and write
    backup = SRC.with_suffix('.html.bak')
    backup.write_text(en_html, encoding='utf-8')
    
    output = en_soup.prettify()
    SRC.write_text(output, encoding='utf-8')
    
    print(f"✓ Reformatted: {SRC}")
    print(f"  Original: {len(en_html):,} chars")
    print(f"  New: {len(output):,} chars")
    print(f"  Backup: {backup}")

if __name__ == '__main__':
    main()