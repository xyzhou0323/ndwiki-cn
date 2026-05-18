---
title: Wiki Schema
description: 页面类型、目录结构和标签体系
tags: [meta]
created: 2026-05-07
updated: 2026-05-18
---

# Schema

## 目录结构

按 [[00-知识地图|知识地图]] 的六部分重要性排序组织：

| 目录 | MOC 章节 | 用途 | 页面数 |
|------|----------|------|--------|
| `wiki/01-基础/` | 一 | 生物学事实、范式框架、核心术语、运动史 | 7 |
| `wiki/02-批判分析/` | 二 | 政治经济学批判、意识形态分析 | 16 |
| `wiki/03-历史脉络/` | 三 | 历史脉络——"正常"的发明及其抵抗 | 4 |
| `wiki/04-体验与实践/` | 四 | 体验、研究、教育与方法论——范式如何转化为行动 | 11 |
| `wiki/05-诊断与现象/` | 五 | 神经发育类型与相关心理现象——ASD、ADHD、述情障碍等 | 6 |
| `wiki/06-测试/` | 六 | 量表、测试工具与相关文献——与神经多样性理论相对隔离 | 23 |
| `wiki/authors/` | 七 | 作者 | 62 |
| `wiki/works/` | 八 | 参考文献 | 57 |

入口页面：[[00-知识地图]]

## Sources 目录组织

`sources/` 根目录是待处理文件的**收件箱**。完成摄取后，原始文件移入对应子文件夹。

| 目录 | 用途 |
|------|------|
| `sources/books/` | 专著、编辑卷（.epub, .pdf, .md 衍生阅读版） |
| `sources/papers/` | 期刊论文、会议论文（.pdf） |
| `sources/blog-posts/` | Substack、博客等网络文章（.md） |
| `sources/articles/` | 翻译文章、原创中文文章、其他非期刊写作（.md） |
| `sources/tests/` | 测试/量表相关的文献（期刊论文、PDF）——与神经多样性理论文献隔离 |
| `sources/YYYY-MM-DD/` | 按日期归档的摄取副本——摄入时自动创建，不可修改 |

### 工作流

1. 新文件直接放入 `sources/` 根目录（收件箱）
2. 执行 `/ingest`：文件复制到 `sources/YYYY-MM-DD/`，创建/更新 wiki 页面
3. **EPUB 格式**：摄入后自动运行 `epub2md.py` 转换为 .md 衍生阅读版，与原始 .epub 放置在同一目录
4. 完成后，原始文件从根目录移入对应类别文件夹（如 `sources/books/`），更新路径以便下次阅读
5. `sources/YYYY-MM-DD/` 内的副本保持不变——它们作为 wiki frontmatter `sources:` 字段的引用目标

## 命名规范

- 使用中文 kebab-case 作为文件名（如 `神经多样性教育.md`）
- 英文概念保留英文原名，中文译名作为别名
- 著作页以"作者-年份-中文标题"格式命名

## 必需 Frontmatter

每个 Wiki 页面必须包含：

```yaml
---
title: 页面标题
description: 一句话摘要
aliases: [别名列表]
tags: [类型标签, 领域标签, ...]
sources: [YYYY-MM-DD/源文件名]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

### 作品页（works/）额外要求

所有 `works/` 目录下的页面必须额外包含：

1. **Frontmatter `citation_apa`** — APA 7th 格式的完整引用：

```yaml
citation_apa: "Author, A. A. (Year). Title. Journal, Volume(Issue), Pages. https://doi.org/xx"
```

2. **正文引用行** — 标题下方紧跟 `引用：` 行，方便读者直接复制：

```markdown
# 标题

引用：Author, A. A. (Year). Title. Journal, Volume(Issue), Pages. https://doi.org/xx
```

## 标签体系

标签采用扁平列表格式（Obsidian 兼容），按以下维度组织：

### 页面类型（每个页面一个）

| 标签 | 说明 |
|------|------|
| `theory` | 元层次范式框架（01-基础/中的理论页） |
| `concept` | 概念与批判分析（01-基础/ 02-批判/ 04-实践/） |
| `event` | 历史事件/运动（03-历史/） |
| `author` | 人物页面（authors/） |
| `work` | 著作页面（works/） |
| `test` | 测试/量表页面（05-测试/） |

### 领域标签（可多个）

| 标签 | 说明 |
|------|------|
| `neurodiversity` | 神经多样性 |
| `autism` | 孤独谱系 |
| `capitalism` | 资本主义批判 |
| `education` | 教育 |
| `disability` | 残障 |

### 主题标签（可多个）

| 标签 | 说明 |
|------|------|
| `foundational` | 基础性/奠基性 |
| `historical` | 历史脉络 |
| `political` | 政治经济学批判 |
| `applied` | 实践应用 |
| `intersectionality` | 交叉性 |
| `critique` | 批判分析 |
| `methodology` | 方法论 |
