#!/usr/bin/env python3
"""Add a Wikipedia-style infobox to work pages (wiki/works/*.md).

Infobox is generated from data already present in the page (citation_apa,
the `**作者**` line, the `**类型**` line, aliases) — never fabricates facts.

Usage:
  python .llm-wiki/add-works-infobox.py --dry-run
  python .llm-wiki/add-works-infobox.py
"""

import re
import sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

WIKI_DIR = Path(__file__).resolve().parent.parent / "wiki"
TODAY = date.today().isoformat()

AUTHOR_YEAR_ALIAS = re.compile(r"^(.+?)\s*\((\d{4})\)$")
CITATION_HEAD = re.compile(r"^([^,]+),?.*?\s*\((\d{4})\)")
VOLUME_PATTERN = re.compile(r", \d+(\(\d+\))?, \d+")


def alias_title(aliases):
    for a in aliases:
        m = AUTHOR_YEAR_ALIAS.match(a.strip())
        if m:
            return f"{m.group(1)} ({m.group(2)})"
    return None


def citation_author_year(cit):
    m = CITATION_HEAD.match(cit)
    if m:
        return m.group(1).strip(), m.group(2)
    return None, None


def author_field(body):
    m = re.search(r"\*\*作者\*\*：(.+)", body)
    if not m:
        return None
    links = re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", m.group(1))
    if links:
        return "、".join(f"[[{name}]]" for name in links)
    return None


CHAPTER_PATTERN = re.compile(r"(, In |\. In )[^(]*\(Ed")
JOURNAL_PATTERN = re.compile(r", \d+(\(\d+\))?, \d+")


def type_field(body, cit):
    # infer publication type from the citation structure first (consistent taxonomy)
    if CHAPTER_PATTERN.search(cit):
        return "书章"
    if JOURNAL_PATTERN.search(cit):
        return "期刊论文"
    if "Press" in cit or "(Ed" in cit:
        return "专著/编著"
    m = re.search(r"\*\*类型\*\*：(.+)", body)
    if m and len(m.group(1).strip()) <= 12:
        return m.group(1).strip()
    return None


def main():
    dry = "--dry-run" in sys.argv
    changed = skipped = 0
    for path in sorted((WIKI_DIR / "works").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
        if not m:
            skipped += 1
            continue
        fm_raw, body = m.group(1), m.group(2)
        # strip an existing infobox block (idempotent re-run)
        body = re.sub(r"^> \[!infobox\].*\n(?:> .*\n)*", "", body, count=1, flags=re.M)
        cit_m = re.search(r"^citation_apa:\s*[\"']?(.+?)[\"']?\s*$", fm_raw, re.M)
        cit = cit_m.group(1).strip() if cit_m else ""
        aliases = re.findall(r"^  - (.+)$", fm_raw, re.M)

        title = alias_title(aliases)
        author, year = citation_author_year(cit)
        if not title:
            if author and year:
                title = f"{author} ({year})"
            else:
                title = re.sub(r"(\d{4})$", r" (\1)", path.stem)

        lines = [f"> [!infobox] {title}"]
        af = author_field(body)
        if af:
            lines.append(f"> **作者**：{af}")
        elif author:
            lines.append(f"> **作者**：{author}")
        if year:
            lines.append(f"> **出版年份**：{year}")
        tf = type_field(body, cit)
        if tf:
            lines.append(f"> **类型**：{tf}")
        infobox = "\n".join(lines)

        # insert right after the H1 title line; tidy blank lines in the top region
        new_body = re.sub(r"(^# .+$\n)", rf"\1\n{infobox}\n", body, count=1, flags=re.M)
        new_body = re.sub(r"\n{3,}", "\n\n", new_body[:2500]) + new_body[2500:]
        if new_body == body:
            skipped += 1
            continue
        body = new_body

        fm_raw = re.sub(r"^updated:.*$", f"updated: {TODAY}", fm_raw, flags=re.M)
        if not dry:
            path.write_text("---\n" + fm_raw + "\n---\n" + body, encoding="utf-8")
        print(f"[{'DRY' if dry else 'WROTE'}] {path.name}  <- {title}")
        changed += 1

    print(f"\n=== {changed} 页添加 infobox，{skipped} 页跳过 ===")


if __name__ == "__main__":
    main()
