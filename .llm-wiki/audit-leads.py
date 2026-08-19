#!/usr/bin/env python3
"""Lead paragraph audit for wiki/ — checks the paragraph between H1 (after infobox/引用行) and the first ## heading.

Criteria (wiki-schema.md「页面结构」):
- Lead must be a complete sentence with a subject, standing alone as the page's topic statement
- Lead should match description intent (used for search + HTML meta)
- Neutral, factual, non-promotional tone

Checks:
  1. missing lead (H1/infobox/引用行 followed directly by a heading)
  2. lead too short (< 25 chars)
  3. lead starting with weak connectors / pronouns (这说明、这是一个、本文是…)
  4. subjective / loaded words (惊人、遗憾、伟大、卓越、令人、叹为观止、非凡 etc.)
  5. lead ends without period (。！？)
"""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

WIKI_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = WIKI_ROOT / "wiki"

MIN_LEAD_CHARS = 25
# Meta pages exempt from lead requirements (wiki-schema.md「Meta 页豁免」)
META_EXEMPT = {"00-知识地图.md", "阅读路线.md", "术语翻译对照表.md", "TEMPLATE.md", "README.md", "COLLABORATING.md"}

# subjective / non-neutral markers (tone audit)
SUBJECTIVE = [
    "惊人", "遗憾", "令人", "叹为观止", "非凡", "卓越", "出色", "精彩", "伟大",
    "糟糕", "可怕", "不幸", "幸运", "可惜", "可悲", "可喜", "振奋", "激动人心",
    "令人发指", "荒谬", "可笑", "尴尬", "完美", "极其", "非常", "十分", "极度",
    "感同身受", "共鸣", "震撼", "宝贵", "珍贵", "重要贡献"  # 重要贡献 borderline, flag only
]

# weak openers — lead should name the subject directly
WEAK_OPENERS = [
    r"^这是一个", r"^这是对", r"^该(文|书|篇|研究)", r"^本文", r"^本页",
    r"^它(是|指|讨论|提出)", r"^其(是|指|讨论|提出)", r"^此(文|书|篇)",
    r"^简单说", r"^一句话", r"^即", r"^也就是", r"^所谓",
]


def extract_lead(body):
    """Return the lead paragraph text between H1 (and infobox/引用行) and the first ## heading."""
    stripped = body.strip()
    # drop H1
    after_h1 = re.sub(r"^# .+\n+", "", stripped, count=1)
    # drop leading infobox / blockquote blocks (possibly separated by blank lines)
    while True:
        m2 = re.match(r"^(?:>.*\n)+\n*", after_h1)
        if not m2:
            break
        after_h1 = after_h1[m2.end():]
    # drop 引用： line for works pages
    after_h1 = re.sub(r"^引用：.*(?:\n|$)", "", after_h1, count=1, flags=re.M)
    after_h1 = after_h1.strip()
    # take only the first paragraph: stop at blank line, heading, blockquote/callout, horizontal rule, or EOF
    m = re.match(r"^(.*?)(?=\n\s*\n|\n#{1,6} |\n> |\n---\s*\n|\Z)", after_h1, re.S)
    lead = m.group(1).strip() if m else ""
    if lead.startswith("#"):
        return ""
    return lead


def main():
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
        lead = extract_lead(body)
        pages.append({"path": rel, "fm": fmd, "lead": lead, "body": body})

    only_missing = "--missing" in sys.argv
    issues = {}

    for p in pages:
        rel, fm, lead = p["path"], p["fm"], p["lead"]
        if Path(rel).name in META_EXEMPT:
            continue
        flags = []

        if not lead:
            flags.append("无导语段落")
        else:
            if len(lead) < MIN_LEAD_CHARS:
                flags.append(f"导语过短（{len(lead)} 字符）")
            for w in SUBJECTIVE:
                if w in lead:
                    flags.append(f"主观/情绪化用词：{w}")
                    break
            for pat in WEAK_OPENERS:
                if re.search(pat, lead):
                    flags.append(f"弱主语开头：{pat}")
                    break
            if not re.search(r"[。！？][\"'”』」]*$", lead):
                flags.append("导语未以句号/问号/感叹号结尾")

        if flags:
            if only_missing and "无导语段落" not in flags:
                continue
            issues[rel] = flags

    for rel, flags in issues.items():
        p = next(x for x in pages if x["path"] == rel)
        print(f"[{rel}]")
        for f in flags:
            print(f"  - {f}")
        lead_preview = p["lead"].replace("\n", " ")[:100]
        if lead_preview:
            print(f"    导语：{lead_preview}")

    from collections import Counter
    cats = Counter()
    for flags in issues.values():
        for f in flags:
            cats[f] += 1
    print("\n=== 按问题类型统计 ===")
    for k, v in cats.most_common():
        print(f"{v:4d}  {k}")

    print(f"\n=== 共 {len(issues)} 页存在导语问题（共 {len(pages)} 页） ===")


if __name__ == "__main__":
    main()
