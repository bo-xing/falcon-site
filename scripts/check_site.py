#!/usr/bin/env python3
"""Check routes, anchors, assets, accessible names, and bilingual navigation."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://bo-xing.github.io/falcon-site/'


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = []
        self.refs = []
        self.images = []
        self.h1s = 0
        self.lang = None
        self.language_link = None
        self.home = None
        self.canonical = None
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'html': self.lang = a.get('lang')
        if tag == 'h1': self.h1s += 1
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical = a.get('href')
        if tag == 'a':
            if 'language-link' in a.get('class', '').split(): self.language_link = a.get('href')
            if a.get('aria-label', '').endswith(('home', '首页')): self.home = a.get('href')
        if tag == 'img': self.images.append(a)
        for attr in ['href', 'src']:
            if a.get(attr): self.refs.append(a[attr])
        if a.get('aria-controls'): self.refs.append('#' + a['aria-controls'])
        for id_ in a.get('aria-labelledby', '').split(): self.refs.append('#' + id_)


pages = {p.name: Page(p) for p in ROOT.glob('*.html')}
errors = []
for name, page in pages.items():
    def fail(message): errors.append(f'{name}: {message}')
    if page.h1s != 1: fail(f'expected one h1, got {page.h1s}')
    if page.lang not in ['en', 'zh-Hans']: fail('missing or invalid page language')
    for id_, count in Counter(page.ids).items():
        if count > 1: fail(f'duplicate id {id_}')
    expected_home = 'index-zh.html' if page.lang == 'zh-Hans' else 'index.html'
    if page.home != expected_home: fail('brand link loses the current language')
    partner = name.replace('-zh.html', '.html') if page.lang == 'zh-Hans' else name.replace('.html', '-zh.html')
    if page.language_link != partner: fail('language switch does not lead to the equivalent page')
    if partner in pages and set(page.ids) != set(pages[partner].ids):
        fail('translated pages must share anchor IDs to preserve the reading position')
    expected_canonical = BASE if name == 'index.html' else BASE + name
    if page.canonical != expected_canonical: fail('incorrect canonical URL')
    for image in page.images:
        if 'alt' not in image: fail('image missing alt attribute')
        if image.get('src') and (not image.get('width') or not image.get('height')): fail('image missing intrinsic dimensions')
    for ref in page.refs:
        if ref.startswith(BASE): ref = ref[len(BASE):] or 'index.html'
        url = urlsplit(ref)
        if url.scheme or url.netloc: continue
        path = unquote(url.path) or name
        if not (ROOT/path).is_file(): fail('missing local target ' + ref)
        if url.fragment and path in pages and unquote(url.fragment) not in pages[path].ids: fail('missing anchor ' + ref)

if len(pages) != 8: errors.append(f'expected 8 pages, found {len(pages)}')
for name in ['privacy.html', 'privacy-zh.html', 'terms.html', 'terms-zh.html']:
    if 'Google Play' not in (ROOT/name).read_text(): errors.append(f'{name}: missing Google Play disclosure')
if errors:
    print('\n'.join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f'Passed: {len(pages)} pages; local routes, fragments, assets, language continuity, headings and legal platform coverage.')
