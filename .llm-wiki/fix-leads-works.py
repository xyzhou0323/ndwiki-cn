#!/usr/bin/env python3
"""Rewrite works-page leads that start with 本文 → Author (Year) subject opening.

For each flagged page: extract lead (first paragraph after H1/infobox/引用行),
replace with a subject-first sentence. Default: prepend "Author (Year) " to the
original text minus "本文". Pages where the author name is redundant or the
sentence needs restructuring have explicit mappings below.
"""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

WIKI_DIR = Path(__file__).resolve().parent.parent / "wiki"
WORKS = WIKI_DIR / "works"

# explicit rewrites for redundant/structure cases: filename -> full new lead
EXPLICIT = {
    "Botha2021": "Botha (2021) 以自传式民族志研究审视自己作为孤独谱系研究者在学术界的经历，揭示实证主义“客观性”如何庇护非人化研究并边缘化孤独谱系者的专业见解。",
    "ChengEtAl2023": "Cheng et al. (2023) 在 *Autism* 期刊发表的社论指出神经多样性运动的西方中心性，以埃塞俄比亚、印度和香港为例分析全球南方社区的独特社会文化条件，呼吁避免将神经多样性框架不加批判地移植至非欧美语境，倡导多向知识交流与本土化权利运动。",
    "Dekker2023": "Dekker (2023) 的博客文章撤回此前对 Judy Singer 为“神经多样性”术语创造者的认可，并公布 Tony Langdon 于 1996 年 10 月在 InLv 邮件列表中使用“neurological diversity”的档案证据——这是已知最早的完整表述。",
    "denHouting2019": "den Houting (2019) 以孤独谱系研究者身份在 *Autism* 期刊发表社论，系统澄清了对神经多样性运动的三种常见误解，阐述社会模型在孤独谱系中的应用，并首次将“neurodiversity lite”概念引入学术话语。",
    "Dwyer2022": "Dwyer (2022) 在 *Human Development* 发表的理论论文首次系统梳理“神经多样性方法群”（复数）的内涵、与强社会模型的争论及适用范围争议，并基于互动主义/生态残障观为发展研究者提供实践建议。",
    "Dwyer2025": "Dwyer et al. (2025) 在 *Autism* 期刊发表的混合方法研究基于 504 名社群成员的实证调查，揭示“强”社会模型修辞与实际干预态度之间的系统性差异，以及孤独谱系与非孤独谱系神经多样性方法支持者之间的关键张力。",
    "DwyerEtAl2026": "Dwyer et al. (2026) 在 *Journal of Attention Disorders* 发表的跨诊断实证研究探讨孤独谱系、ADHD 及一般人群中注意力与听觉过度反应的多样化表型之间的关系。",
    "DwyerEtAl2023": "Dwyer et al. (2023) 由神经殊异学生与研究者共同撰写，提出建设神经多样性包容高校的三项领域 13 条系统建议，并获加州大学学术评议会（UC Academic Senate）正式支持。",
    "Sinclair1993": "Sinclair (1993) 是神经多样性运动奠基宣言，首次将孤独谱系者的公共发言从个人叙事转变为政治诉求。",
    "SonugaBarke2023": "Sonuga-Barke (2023) 作为 JCPP 主编发表社论，论证神经多样性视角的本体论假设可从意识形态主张中分离，提出从“障碍范式”到“分歧范式”的范式翻转，以“个人成长弧”重新定义干预目标，并以 RE-STAR 青年研究者小组（Y-RP）作为参与式研究典范。",
    "SonugaBarkeThapar2021": "Sonuga-Barke & Thapar (2021) 在 *The Lancet Psychiatry* 发表的临床视角评论拒绝 ND 的“激进”解释，但主张将 ND 概念纳入主流研究与实践并行的整合路径。",
    "Srinivasan2025": "Srinivasan (2025) 在 *Research in Autism* 发表的框架论文整合残障研究、社会正义与政策的跨学科洞见，提出“神经多样性 2.0”框架，反对社会 vs 医学、自主 vs 依赖、优势 vs 缺陷的虚假二元，倡导从被动便利措施转向主动系统设计。",
    "Walker2014": "Walker (2014) 对神经多样性、神经多样性范式、神经多样性运动、神经殊异、神经典型等核心概念作出奠基性界定。",
    "SzechyEtAl2024": "Szechy et al. (2024) 首次将双向同理心问题（DEP）应用于职场情境，实证比较 ToM 缺陷假说与 DEP 对孤独谱系员工行为的解释力，结果显示孤独谱系者比非孤独谱系者更准确地理解孤独谱系员工，从而支持 DEP。",
    "StennerEtAl2025": "10 位神经殊异研究者（Stenner et al., 2025）使用 Q 方法学，系统识别关于“神经多样性是什么”的三种理解与“运动应该做什么”的三种处方，首次以集体反思性程序经验性地展示神经多样性运动内部的观点多样性及其共识基础。",
}


def extract_lead(body):
    stripped = body.strip()
    after_h1 = re.sub(r"^# .+\n+", "", stripped, count=1)
    while True:
        m2 = re.match(r"^(?:>.*\n)+\n*", after_h1)
        if not m2:
            break
        after_h1 = after_h1[m2.end():]
    after_h1 = re.sub(r"^引用：.*(?:\n|$)", "", after_h1, count=1, flags=re.M)
    after_h1 = after_h1.strip()
    m = re.match(r"^(.*?)(?=\n\s*\n|\n#{1,6} |\n> |\n---\s*\n|\Z)", after_h1, re.S)
    lead = m.group(1).strip() if m else ""
    if lead.startswith("#"):
        return ""
    return lead


def author_year_from_title(title):
    m = re.match(r"^(.*?)\s*\(\d{4}[a-z]?\)", title)
    year = re.search(r"\((\d{4}[a-z]?)\)", title)
    if not m or not year:
        return None
    return f"{m.group(1).strip()} ({year.group(1)})"


def main():
    done = 0
    for path in sorted(WORKS.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
        if not m:
            continue
        fm, body = m.group(1), m.group(2)
        lead = extract_lead(body)
        if not lead.startswith("本文"):
            continue
        title = re.search(r"^title:\s*(.*)$", fm, re.M).group(1).strip()
        if path.stem in EXPLICIT:
            new_lead = EXPLICIT[path.stem]
        else:
            ay = author_year_from_title(title)
            if not ay:
                print(f"!! {path.stem}: cannot derive author-year from title: {title}")
                continue
            new_lead = ay + lead[2:]
        if lead not in body:
            print(f"!! {path.stem}: lead not found verbatim in body")
            continue
        body2 = body.replace(lead, new_lead, 1)
        text2 = re.sub(r"^---\n.*?\n---\n", f"---\n{fm}\n---\n", text, count=1, flags=re.S)
        text2 = text2.replace(body, body2, 1)
        path.write_text(text2, encoding="utf-8")
        done += 1
        print(f"[{path.stem}]")
        print(f"  old: {lead[:120]}...")
        print(f"  new: {new_lead[:120]}...")
    print(f"\n共改写 {done} 页")


if __name__ == "__main__":
    main()
