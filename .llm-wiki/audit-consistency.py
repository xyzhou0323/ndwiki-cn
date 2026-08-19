#!/usr/bin/env python3
"""Consistency audit for wiki/ — flags pages that deviate from wiki-schema.md.

Usage:
  python .llm-wiki/audit-consistency.py            # full report
  python .llm-wiki/audit-consistency.py --missing  # required fields only
"""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

WIKI_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = WIKI_ROOT / "wiki"

REQUIRED_FIELDS = ["title", "description", "aliases", "tags", "sources", "created", "updated"]
STUB_CHARS = 500                # body length below this (no frontmatter) => stub candidate
# Meta pages exempt from sources/Related/lead/summary requirements (wiki-schema.md「Meta 页豁免」)
META_EXEMPT = {"00-知识地图.md", "阅读路线.md", "术语翻译对照表.md", "TEMPLATE.md", "README.md", "COLLABORATING.md"}


def read_pages():
    pages = []
    for path in sorted(WIKI_DIR.rglob("*.md")):
        rel = path.relative_to(WIKI_DIR).as_posix()
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
        fm, body = (m.group(1), m.group(2)) if m else ("", text)
        fmd = {}
        for line in fm.splitlines():
            mm = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
            if mm:
                fmd[mm.group(1)] = mm.group(2).strip()
        pages.append({"path": rel, "fm": fmd, "body": body, "text": text})
    return pages


def main():
    only_missing = "--missing" in sys.argv
    pages = read_pages()
    issues = {}

    for p in pages:
        rel, fm, body = p["path"], p["fm"], p["body"]
        if Path(rel).name in META_EXEMPT:
            continue
        flags = []

        # 1. required frontmatter fields
        for f in REQUIRED_FIELDS:
            if f not in fm:
                flags.append(f"缺 frontmatter: {f}")

        # 2. lead paragraph (content before the first heading, after H1 title)
        stripped = body.strip()
        after_h1 = re.sub(r"^# .+\n+", "", stripped, count=1)
        if after_h1.startswith("#") or not after_h1:
            flags.append("无导语段落（H1 后直接是标题或无正文）")

        # 3. toc must NOT be written into md (deployment auto-generates it)
        no_comments = re.sub(r"<!--.*?-->", "", body, flags=re.S)
        if "[!toc]" in no_comments:
            flags.append("md 中含 [!toc]（应由部署端自动生成，应移除）")

        # 4. headings using 核心
        for line in re.findall(r"^#{1,3} .*核心.*$", body, re.M):
            flags.append(f"标题含'核心'：{line.strip()}")

        # 5. inline frontmatter list style (normalize to block)
        for f in ("aliases", "tags", "sources"):
            if f in fm and "[" in fm[f]:
                flags.append(f"frontmatter {f} 为行内数组写法")

        # 6. missing Related
        if not re.search(r"^## Related", body, re.M):
            flags.append("无 ## Related 节")

        # 7. stub candidate (skip pages already marked as stub)
        raw_fm = ""
        mf = re.match(r"^---\n(.*?)\n---", p["text"], re.S)
        if mf:
            raw_fm = mf.group(1)
        tags_block = ""
        mt = re.search(r"^tags:\s*(.*)$", raw_fm, re.M)
        if mt:
            if mt.group(1).strip():
                tags_block = mt.group(1)
            else:
                blk = re.match(r"((?:  - .*\n)+)", raw_fm[mt.end():])
                if blk:
                    tags_block = blk.group(1)
        is_stub = "stub" in tags_block
        body_len = len(stripped)
        if body_len < STUB_CHARS and not is_stub:
            flags.append(f"内容过短（{body_len} 字符）— stub 候选")

        if flags and not only_missing or (only_missing and any("frontmatter" in f for f in flags)):
            issues[rel] = flags

    for rel, flags in issues.items():
        print(f"[{rel}]")
        for f in flags:
            print(f"  - {f}")

    from collections import Counter
    cats = Counter()
    for flags in issues.values():
        for f in flags:
            key = re.sub(r"（\d+ 个 ## 节）", "（N 个 ## 节）", f)
            key = re.sub(r"（\d+ 字符）", "（N 字符）", key)
            cats[key] += 1
    print("\n=== 按问题类型统计 ===")
    for k, v in cats.most_common():
        print(f"{v:4d}  {k}")

    print(f"\n=== 共 {len(issues)} 页存在规范偏差（共 {len(pages)} 页） ===")


if __name__ == "__main__":
    main()
