#!/usr/bin/env python3
"""Update wiki page counts — replace {{KEY}} placeholders with actual counts.

Usage:  python .llm-wiki/update-counts.py

On each run, counts .md files in wiki/ subdirectories and updates the
count display in wiki-purpose.md, wiki-schema.md, wiki/00-知识地图.md,
and wiki/阅读路线.md.  Works regardless of whether the files currently
contain {{KEY}} placeholders or concrete numbers — the script matches
the surrounding prose context to update the right value.
"""

import re
from pathlib import Path

WIKI_ROOT = Path(__file__).resolve().parent.parent

FILES = [
    "wiki-purpose.md",
    "wiki-schema.md",
    "wiki/00-知识地图.md",
    "wiki/阅读路线.md",
]


def count(dir_rel: str) -> int:
    p = WIKI_ROOT / dir_rel
    return len([f for f in p.iterdir() if f.suffix == ".md"]) if p.is_dir() else 0


def counts() -> dict[str, int]:
    c = {
        "SEC_01_COUNT": count("wiki/01-基础"),
        "SEC_02_COUNT": count("wiki/02-批判分析"),
        "SEC_03_COUNT": count("wiki/03-历史脉络"),
        "SEC_04_COUNT": count("wiki/04-体验与实践"),
        "SEC_05_COUNT": count("wiki/05-诊断与现象"),
        "SEC_06_COUNT": count("wiki/06-测试"),
        "AUTHOR_COUNT": count("wiki/authors"),
        "WORK_COUNT": count("wiki/works"),
        "PAGE_COUNT": len(list((WIKI_ROOT / "wiki").rglob("*.md"))),
        "TEST_COUNT": count("wiki/06-测试") - 1,
    }
    return c


# Each rule: (regex_with_capture_group_for_the_number, replacement_template)
# The replacement template uses {KEY} placeholders, which get expanded after.
# Rules are applied in order; the first match on a line wins.
RULES = [
    # ── 阅读路线.md ──
    (r"本 Wiki 有 (\d+) 个页面，按",            "本 Wiki 有 {PAGE_COUNT} 个页面，按"),
    (r"引用作者索引]]：(\d+) 位作者",            "引用作者索引]]：{AUTHOR_COUNT} 位作者"),
    (r"参考文献索引]]：(\d+) 部/篇",             "参考文献索引]]：{WORK_COUNT} 部/篇"),
    (r"测试工具索引]]：(\d+) 项自填式探索工具",    "测试工具索引]]：{TEST_COUNT} 项自填式探索工具"),

    # ── 00-知识地图.md ──
    (r"共 \*\*(\d+) 个页面\*\*",               "共 **{PAGE_COUNT} 个页面**"),
    (r"> (\d+) 位作者，按姓氏字母排序",           "> {AUTHOR_COUNT} 位作者，按姓氏字母排序"),

    # ── wiki-purpose.md (use distinctive anchor text before the count) ──
    (r"(\[\[残障模型\]\]) 等 (\d+) 页",          r"\1 等 {SEC_01_COUNT} 页"),
    (r"(\[\[神经撒切尔主义\]\]) 等 (\d+) 页",      r"\1 等 {SEC_02_COUNT} 页"),
    (r"(\[\[神经多样性运动史\]\]) 等 (\d+) 页",    r"\1 等 {SEC_03_COUNT} 页"),
    (r"(\[\[ASD干预\]\]) 等 (\d+) 页",           r"\1 等 {SEC_04_COUNT} 页"),
    (r"(\[\[述情障碍\]\]) 等 (\d+) 页",           r"\1 等 {SEC_05_COUNT} 页"),
    (r"\(量表与工具索引\)，与理论部分相对隔离（(\d+) 页）",
                                                 "(量表与工具索引)，与理论部分相对隔离（{SEC_06_COUNT} 页）"),
    (r"(\[\[Sue-Fletcher-Watson\]\]) 等 (\d+) 页", r"\1 等 {AUTHOR_COUNT} 页"),
    (r"(\[\[ChapmanFletcherWatson2025\]\]) 等 (\d+) 页", r"\1 等 {WORK_COUNT} 页"),

    # ── wiki-schema.md table rows ──
    (r"(\| `wiki/01-基础/` \| 一 \| .+? \|) \d+ (\|)",       r"\1 {SEC_01_COUNT} \2"),
    (r"(\| `wiki/02-批判分析/` \| 二 \| .+? \|) \d+ (\|)",    r"\1 {SEC_02_COUNT} \2"),
    (r"(\| `wiki/03-历史脉络/` \| 三 \| .+? \|) \d+ (\|)",    r"\1 {SEC_03_COUNT} \2"),
    (r"(\| `wiki/04-体验与实践/` \| 四 \| .+? \|) \d+ (\|)",  r"\1 {SEC_04_COUNT} \2"),
    (r"(\| `wiki/05-诊断与现象/` \| 五 \| .+? \|) \d+ (\|)",  r"\1 {SEC_05_COUNT} \2"),
    (r"(\| `wiki/06-测试/` \| 六 \| .+? \|) \d+ (\|)",       r"\1 {SEC_06_COUNT} \2"),
    (r"(\| `wiki/authors/` \| 七 \| .+? \|) \d+ (\|)",       r"\1 {AUTHOR_COUNT} \2"),
    (r"(\| `wiki/works/` \| 八 \| .+? \|) \d+ (\|)",         r"\1 {WORK_COUNT} \2"),
]


def update_file(filepath: Path, c: dict[str, int]) -> bool:
    """Replace count numbers (or {{KEY}} placeholders) with fresh counts."""
    text = filepath.read_text(encoding="utf-8")

    # Step 1: Unexpand — replace concrete numbers (or stale placeholders)
    # with {KEY} tokens by matching the surrounding prose.
    for pattern, template in RULES:
        text = re.sub(pattern, template, text)

    # Step 2: Expand — replace {KEY} tokens with actual counts.
    # Also handle {{KEY}} from the original placeholder format.
    for key, val in c.items():
        text = text.replace("{" + key + "}", str(val))
        text = text.replace("{{" + key + "}}", str(val))

    if text != filepath.read_text(encoding="utf-8"):
        filepath.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    c = counts()
    for rel in FILES:
        fp = WIKI_ROOT / rel
        if not fp.exists():
            print(f"  SKIP {rel} (not found)")
            continue
        changed = update_file(fp, c)
        print(f"  {'WROTE' if changed else 'OK'}   {rel}")

    print(f"\n  total={c['PAGE_COUNT']}  authors={c['AUTHOR_COUNT']}  "
          f"works={c['WORK_COUNT']}  tests={c['TEST_COUNT']}")
    for k in sorted(c):
        if k.startswith("SEC_"):
            print(f"  {k}={c[k]}", end="")
    print()


if __name__ == "__main__":
    main()
