#!/usr/bin/env python3
"""Reformat KyThuat_TraiTay_MotTay_Clean.html to main site theme (Modern_Tennis_Handbook)."""

from bs4 import BeautifulSoup
from pathlib import Path
import re

SRC = Path(r"C:\Users\Henry\Documents\Github Repos\tenniskb.github.io\en\handbooks\KyThuat_TraiTay_MotTay_Clean.html")
TEMPLATE = Path(r"C:\Users\Henry\Documents\Github Repos\tenniskb.github.io\vi\cam-nang\tfl\Modern_Tennis_Handbook.html")

def main():
    en_html = SRC.read_text(encoding='utf-8')
    tpl_html = TEMPLATE.read_text(encoding='utf-8')
    
    # Extract template CSS
    tpl_head_start = tpl_html.find('<head>') + len('<head>')
    tpl_head_end = tpl_html.find('</head>')
    tpl_head_content = tpl_html[tpl_head_start:tpl_head_end]
    
    style_match = re.search(r'<style>(.*?)</style>', tpl_head_content, re.DOTALL)
    tpl_style_css = style_match.group(1) if style_match else ""
    
    # Parse EN file
    en_soup = BeautifulSoup(en_html, 'html5lib')
    
    # Update lang
    en_soup.html['lang'] = 'en'
    
    # Rebuild head with template's CSS
    en_head = en_soup.head
    en_head.clear()
    
    # Meta
    en_head.append(BeautifulSoup('<meta charset="utf-8"/>', 'html5lib').meta)
    en_head.append(BeautifulSoup('<meta content="width=device-width, initial-scale=1.0" name="viewport"/>', 'html5lib').meta)
    
    # Title
    title = en_soup.new_tag('title')
    title.string = 'One-Handed Backhand Technique (1HBH) - Tennis Future Lab'
    en_head.append(title)
    
    # Template styles
    style_tag = en_soup.new_tag('style')
    style_tag.string = tpl_style_css
    en_head.append(style_tag)
    
    # Body structure
    en_body = en_soup.body
    
    # Find elements
    masthead = en_soup.find('div', class_='masthead')
    content_div = en_soup.find('div', class_='content')
    page_nav = en_soup.find('nav', class_='page-nav')
    container = en_soup.find('div', class_='container')
    
    # Extract content_div children
    if content_div and page_nav and page_nav.parent == content_div:
        page_nav.extract()
    
    # Create content-wrap
    content_wrap = en_soup.new_tag('div', **{'class': 'content-wrap'})
    if content_div:
        content_div.extract()
        content_wrap.append(content_div)
    
    # Clear body
    en_body.clear()
    
    # Add masthead
    if masthead:
        masthead['class'] = 'masthead'
        if 'style' in masthead.attrs:
            del masthead['style']
        # Update tag
        tag_span = masthead.find('span', class_='tag')
        if not tag_span:
            tag_span = en_soup.new_tag('span', **{'class': 'tag'})
            tag_span.string = 'Tennis Future Lab · Kỹ Thuật'
            masthead.insert(0, tag_span)
        # Update h1
        h1 = masthead.find('h1')
        if h1:
            h1.string = 'One-Handed Backhand Technique (1HBH)'
        # Subtitle
        subtitle = masthead.find('p', class_='subtitle')
        if not subtitle:
            subtitle = en_soup.new_tag('p', **{'class': 'subtitle'})
            subtitle.string = 'Biomechanics, Technique & Drills'
            if h1:
                h1.insert_after(subtitle)
        en_body.append(masthead)
    
    en_body.append(content_wrap)
    
    # Remove page-nav (main theme doesn't have it)
    # Just add footer directly
    
    # Update content div - remove page-nav if present
    content_div = en_soup.find('div', class_='content')
    if content_div:
        content_div['class'] = 'content'
        # Find and remove page-nav if still inside
        nav_in_content = content_div.find('nav', class_='page-nav')
        if nav_in_content:
            nav_in_content.extract()
    
    # Footer - match main theme (Henry Pham, Tennis Future Lab, CC BY-NC-SA)
    footer = en_soup.find('footer')
    if footer:
        footer.decompose()
    
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
    
    # Remove container if still present
    if container:
        container.decompose()
    
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