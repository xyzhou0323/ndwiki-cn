#!/usr/bin/env python3
"""Sync zh-hant aliases from zh-hans using OpenCC s2t conversion."""
import re
from pathlib import Path
from opencc import OpenCC

ROOT = Path(__file__).resolve().parent.parent
cc = OpenCC('s2t.json')
wiki = ROOT / 'wiki'
hant = ROOT / 'wiki-zh-hant'

mismatches = 0
for f in sorted(wiki.rglob('*.md')):
    if f.name in ('COLLABORATING.md', 'README.md'):
        continue
    rel = f.relative_to(wiki)
    hf = hant / rel
    if not hf.exists():
        continue

    htext = hf.read_text(encoding='utf-8')
    text = f.read_text(encoding='utf-8')

    m_hans = re.search(r'aliases:\s*\[(.+?)\]', text, re.DOTALL)
    m_hant = re.search(r'aliases:\s*\[(.+?)\]', htext, re.DOTALL)

    if not m_hans or not m_hant:
        continue

    def parse_aliases(raw):
        items = []
        for item in raw.split(','):
            item = item.strip().strip("'\"")
            if item:
                items.append(item)
        return items

    hans_aliases = parse_aliases(m_hans.group(1))
    hant_aliases = parse_aliases(m_hant.group(1))

    # Expected: OpenCC convert each hans alias
    expected = [cc.convert(a) for a in hans_aliases]

    if expected != hant_aliases:
        mismatches += 1
        new_aliases = ', '.join(expected)
        old_raw = m_hant.group(0)
        new_raw = 'aliases: [' + new_aliases + ']'
        htext = htext.replace(old_raw, new_raw)
        hf.write_text(htext, encoding='utf-8')
        print(f'{rel}: {hant_aliases} -> {expected}')

print(f'\nTotal alias mismatches fixed: {mismatches}')
