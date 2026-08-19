#!/usr/bin/env python3
"""Mechanical consistency fixes for wiki/ — applies wiki-schema.md 2026-08-12 rules.

1. Convert inline frontmatter arrays (aliases/tags/sources) to block style
2. Insert `> [!toc]` for pages with >= 6 `##` sections (long pages)
3. Add `#stub` tag + note callout for pages with body < 500 chars
4. Set `updated` to today for every touched page

Usage:
  python .llm-wiki/fix-consistency.py --dry-run   # preview
  python .llm-wiki/fix-consistency.py             # apply
"""

import re
import sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

WIKI_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = WIKI_ROOT / "wiki"
TODAY = date.today().isoformat()  # 2026-08-12
TOC_THRESHOLD = 6
STUB_CHARS = 500

META_FILES = {
    "00-知识地图.md", "阅读路线.md", "术语翻译对照表.md", "TEMPLATE.md",
    "COLLABORATING.md", "README.md",
}
LIST_FIELDS = ("aliases", "tags", "sources")


def is_meta(rel):
    return rel.endswith("/README.md") or rel.rsplit("/", 1)[-1] in META_FILES


def split_inline_list(text):
    """Split a YAML flow array `[a, "b, c", d(e, f)]` into items.

    Tolerant of commas inside parentheses and double-quoted strings.
    """
    items, cur, quote, depth = [], [], None, 0
    for ch in text.strip()[1:-1]:
        if quote:
            if ch == quote:
                quote = None
            cur.append(ch)
        elif ch in ('"', "'"):
            quote = ch
            cur.append(ch)
        elif ch == "(":
            depth += 1
            cur.append(ch)
        elif ch == ")":
            depth = max(0, depth - 1)
            cur.append(ch)
        elif ch == "," and depth == 0:
            items.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    if cur:
        items.append("".join(cur).strip())
    return [i[1:-1] if len(i) >= 2 and i[0] == i[-1] == '"' else i for i in items if i]


def block_lines(field, items):
    if not items:
        return [f"{field}: []"]
    return [f"{field}:"] + [f"  - {item}" for item in items]


def main():
    dry = "--dry-run" in sys.argv
    pages = sorted(p for p in WIKI_DIR.rglob("*.md") if not is_meta(p.as_posix()))
    stats = {"toc": 0, "stub": 0, "fm": 0, "updated": 0}
    skipped, failed = [], []

    for path in pages:
        rel = path.relative_to(WIKI_DIR).as_posix()
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
        if not m:
            skipped.append((rel, "无 frontmatter"))
            continue
        fm_raw, body = m.group(1), m.group(2)
        lines = fm_raw.splitlines()
        changed = False

        # 1. inline arrays -> block style (tolerant line-based parse)
        for field in LIST_FIELDS:
            idx = next((i for i, ln in enumerate(lines) if re.match(rf"^{field}:\s*\[", ln)), None)
            if idx is None:
                continue
            m_inline = re.match(rf"^{field}:\s*(.*)$", lines[idx])
            if not m_inline:
                continue
            items = split_inline_list(m_inline.group(1))
            lines[idx : idx + 1] = block_lines(field, items)
            changed = True
            stats["fm"] += 1

        # 2. TOC for long pages
        sections = len(re.findall(r"^## ", body, re.M))
        if sections >= TOC_THRESHOLD and "[!toc]" not in body:
            body = re.sub(r"^(## .*)$", "> [!toc]\n\n\\1", body, count=1, flags=re.M)
            changed = True
            stats["toc"] += 1

        # 3. stub marker
        body_len = len(body.strip())
        if body_len < STUB_CHARS and not any(ln.strip() == "- stub" for ln in lines):
            idx = next((i for i, ln in enumerate(lines) if ln.startswith("tags:")), None)
            if idx is not None:
                lines.insert(idx + 1, "  - stub")
            body = body.rstrip() + "\n\n> [!note] 小作品\n> 本页内容尚不完整，待从源文献扩展。\n"
            changed = True
            stats["stub"] += 1

        # 4. bump updated on touched pages
        if changed:
            idx = next((i for i, ln in enumerate(lines) if ln.startswith("updated:")), None)
            if idx is not None:
                lines[idx] = f"updated: {TODAY}"
                stats["updated"] += 1

        if not changed:
            continue

        new_text = "---\n" + "\n".join(lines) + "\n---\n" + body
        if not dry:
            path.write_text(new_text, encoding="utf-8")
        print(f"[{'DRY' if dry else 'WROTE'}] {rel}  (toc={sections >= TOC_THRESHOLD})")

    print("\n=== 统计 ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    if failed:
        print("=== 失败（需人工处理） ===")
        for rel, why in failed:
            print(f"  {rel}: {why}")


if __name__ == "__main__":
    main()
