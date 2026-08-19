#!/usr/bin/env python3
"""Find pages with bold key-value lines (**身份**：…) in the body top region
(between H1 and first ## heading) that duplicate/compete with the infobox.
Prints per-type lists with counts and field names."""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

WIKI_DIR = Path(__file__).resolve().parent.parent / "wiki"

BOLD_LINE = re.compile(r"^\*\*([^*]+?)\*\*：(.+)$")

def page_parts(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    fm, body = (m.group(1), m.group(2)) if m else ("", text)
    return fm, body

def top_region(body):
    stripped = body.strip()
    after_h1 = re.sub(r"^# .+\n+", "", stripped, count=1)
    return after_h1.split("\n## ")[0]

def has_lead(region, bold_positions):
    """Is there a real text paragraph (not bold meta, not callout, not citation
    line, not list) in the region?"""
    lines = region.splitlines()
    for i, line in enumerate(lines):
        ls = line.strip()
        if not ls or ls.startswith((">", "<!--", "- ", "* ")):
            continue
        if BOLD_LINE.match(ls):
            continue
        # citation line (works pages): starts with 引用：
        if ls.startswith(("引用：", "引用:")):
            continue
        return True
    return False

by_type = {}
for path in sorted(WIKI_DIR.rglob("*.md")):
    rel = path.relative_to(WIKI_DIR).as_posix()
    if Path(rel).name in {"00-知识地图.md", "阅读路线.md", "术语翻译对照表.md", "TEMPLATE.md", "README.md", "COLLABORATING.md"}:
        continue
    fm, body = page_parts(path.read_text(encoding="utf-8"))
    if "[!infobox]" not in body:
        continue
    region = top_region(body)
    bold_lines = [l.strip() for l in region.splitlines() if BOLD_LINE.match(l.strip())]
    if not bold_lines:
        continue
    ptype = rel.split("/")[0]
    has_lead_p = has_lead(region, None)
    by_type.setdefault(ptype, []).append((rel, bold_lines, has_lead_p))

for ptype, items in by_type.items():
    print(f"\n=== {ptype} ({len(items)} pages) ===")
    fields = {}
    no_lead = 0
    for rel, lines, has_lead_p in items:
        if not has_lead_p:
            no_lead += 1
        print(f"  {rel}")
        for l in lines:
            f = l.split("：")[0].strip("*")
            fields[f] = fields.get(f, 0) + 1
    print(f"  -- 无导语段落: {no_lead}")
    print(f"  -- fields: {fields}")
