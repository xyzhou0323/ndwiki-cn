# Change Log

## [2026-06-13] style | 统一测试文件命名：去连字符，CamelCase

- 14 个 `wiki/06-测试/` 文件（简称）去除连字符，如 `AQ-Adol.md` → `AQAdol.md`
- 简体 32 + 繁体 32 个文件的 wikilink 引用同步更新
- `wiki-schema.md`、`wiki/CONTRIBUTING.md` 命名规范补充测试页规则

## [2026-06-13] style | 统一 author 文件命名：去连字符，CamelCase

- 82 个 `wiki/authors/` 文件从 `First-Last.md` 重命名为 `FirstLast.md`
- 所有 wikilink 引用（94 个文件）同步更新
- `wiki-schema.md`、`wiki/CONTRIBUTING.md` 命名规范相应调整

## [2026-06-10] tool | 自动计数系统：update-counts.py + {{KEY}} 占位符

- 将 4 个文件中所有硬编码页面数替换为 `{{KEY}}` 占位符：
  - `{{PAGE_COUNT}}` — wiki/ 总页数（228）
  - `{{AUTHOR_COUNT}}` — 作者页数（84）
  - `{{WORK_COUNT}}` — 著作页数（72）
  - `{{TEST_COUNT}}` — 测试工具数（24，排除 相关测试.md）
  - `{{SEC_01_COUNT}}`~`{{SEC_06_COUNT}}` — 各章节页数
- 创建 `.llm-wiki/update-counts.py`：
  - 统计 wiki/ 各子目录 .md 文件数
  - 通过 prose 上下文正则匹配更新 4 文件中的数字
  - 幂等：多次运行结果一致
- 用法：`python .llm-wiki/update-counts.py` — 今后增删页面后执行即可
- 发现并修正了过期计数：总页数 217→228，知识地图页 209→228，测试工具 22→24

## [2026-06-10] term | "骄傲" → "自尊"：Pride 译法统一（16 页）

- 将 wiki/ 目录下所有 identity pride 语境中的"骄傲"统一替换为"自尊"：
  - **ND 骄傲运动** → **ND 自尊运动**（2 处：[[神经多样性与残障]]）
  - **孤独谱系骄傲** / 孤独谱系骄傲日 → **孤独谱系自尊** / 日（7 处：[[神经多样性运动]]、[[残障模型]]、[[残障肯定模式]]、[[批判残障理论]]、[[Kapp2020|Kapp (2020)]]）
  - **疯狂骄傲（Mad Pride）** → **疯狂自尊**（2 处：[[残障模型]]、[[残障肯定模式]]）
  - **口吃骄傲（Stuttering Pride）** → **口吃自尊**（2 处：[[神经多样性运动]]）
  - **神经殊异骄傲（neurodivergent pride）** → **神经殊异自尊**（7 处：[[残障模型]]、[[残障肯定模式]]、[[残障的哲学定义]]、[[ChapmanBotha2023]]、[[Monique-Botha]]、[[Robert-Chapman]]）
  - **神经殊异接纳与骄傲** → **神经殊异接纳与自尊**（5 处：[[阅读路线]]、[[00-知识地图]]、[[ChapmanBotha2023]]、[[Monique-Botha]]、[[Robert-Chapman]]）
- 边缘情况统一处理：
  - "感到骄傲" → "持有自尊"（2 处：[[残障模型]]、[[Barnes2016|Barnes (2016)]]）
  - "骄傲的对象" / "产生骄傲" / "这种骄傲" → "自尊的对象" / "产生自尊" / "这种自尊"（[[残障的哲学定义]]）
  - "骄傲而非羞耻" → "自尊而非羞耻"（[[StennerEtAl2025|Stenner et al. (2025)]]）
  - "LGBT 骄傲旗" → "LGBT 自尊旗"（[[残障肯定模式]]）
  - "LGBTQ 骄傲" → "LGBTQ 自尊"（[[ChapmanFletcherWatson2025]]）
- 理由："Pride"在此类语境中指身份尊严（dignity/self-respect），非傲慢（arrogance）；"自尊"更准确
- 验证：grep "骄傲" 在 wiki/ 目录零命中
- 涉及 16 个文件，同步完成

## [2026-06-10] enrich | Heraty et al. (2023) 跨页面充实（共 4 页）

- 将 Heraty et al. (2023) 链接到 4 个已有页面：
  - **[[ASD干预]]** — 新增"Heraty et al. (2023)：ND 肯定式生物医学研究的操作框架"节
  - **[[参与式行动研究]]** — 新增"Heraty et al. (2023)：PAR 在生物医学研究中的应用"节
  - **[[残障模型]]** — 关系模型段：补充社会关系模型推荐
  - **[[神经多样性范式]]** — 新增"ND 范式在生物医学研究中的操作化：Heraty et al. (2023)"节：范式原则→研究设计映射表、常态范式在生物医学研究中的自我强化循环、研究基础设施中的常态范式——将范式批判从认识论层面推进到制度层面
- 索引不变（页数未增）



2026-06-12T19:50:00 | ingest: Green et al. (2020) - Teaching and Researching with a Mental Health Diagnosis → wiki/works/GreenEtAl2020.md
2026-06-12T19:50:00 | archive: Heraty et al. source → sources/papers/; Green et al. source → sources/papers/ + sources/2026-06-12/
2026-06-12T19:50:00 | sync: zh-hant submodule updated (3 pages)
