# 贡献指南

欢迎为神经多样性 Wiki 贡献内容。以下是操作规范和流程。

## 先选择提交仓库

本项目把完整知识维护和轻量页面协作分开处理：

| 贡献内容 | 提交仓库 |
|----------|----------|
| 错别字、措辞、格式、链接和局部事实修正；来源明确且不改变结构的单页修改或新增 | [wiki 页面镜像](https://github.com/xyzhou0323/wiki) |
| 多个相互关联页面、批量文献、完整专题、新来源、目录或标签调整、高风险健康内容 | [ndwiki-cn 主仓库](https://github.com/xyzhou0323/ndwiki-cn)（本仓库） |
| 自动转换页面的繁体审校、地区术语和本地化表达 | [ndwiki-hant](https://github.com/xyzhou0323/ndwiki-hant) |

页面数量不是唯一标准。如果一项改动需要批量归档来源、设计多个页面之间的结构、扩展 `wiki-schema.md`、更新全量知识地图，或会触发大规模繁体同步，就属于“专题级摄入”，应从主仓库提交。

### 为什么专题级摄入必须进入主仓库

LLM Wiki 的知识链路由以下部分共同组成：

1. `sources/` 保存不可变的原始资料。
2. `wiki/` 保存知识页面，并通过 frontmatter 的 `sources` 指回原始资料。
3. `wiki-purpose.md`、`wiki-schema.md`、知识地图和阅读路线维护范围、结构、标签与导航。
4. `wiki-log.md`、lint 和 `llm-wiki sync` 维护审计记录、结构健康与搜索索引。
5. 简体内容复核后，再同步页面镜像和繁体版本。

轻量修改可以由维护者手动补齐这些环节；专题级改动需要让来源、页面、结构和索引作为同一批变更接受审阅。

### 已经在页面镜像提交了大型 PR 怎么办

不需要关闭 PR 或重写内容：

1. 保留现有 PR，作为讨论和页面内容的参考。
2. 基于已有分支向 `ndwiki-cn` 建立 PR，或先向维护者提供来源文件及来源清单。
3. 在主仓库中补齐 `sources/`、页面路径、schema、导航、日志和检查结果。
4. 让两个 PR 相互链接；主仓库版本合并后，将镜像 PR 标记为由主仓库 PR 取代。

## 页面规范

每个 Wiki 页面遵循 `wiki-schema.md` 定义的格式：

### 必需 Frontmatter

```yaml
---
title: 页面标题
description: 一句话摘要
aliases:
  - 英文/缩写
  - 中文别名
tags:
  - 类型标签
  - 领域标签
sources:
  - YYYY-MM-DD/源文件名
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

`aliases`、`tags` 和 `sources` 必须使用块状列表。`sources` 中的路径相对于主仓库的 `sources/`，不得使用 `[[文献页]]` 代替原始资料路径。

### 命名规则

- 概念页：连续中文，不加分词符（如 `神经多样性教育.md`）
- 作者页：`FirstName-LastName.md`（连字符分隔，如 `Robert-Chapman.md`）
- 著作页：`AuthorYear.md`（如 `Chapman2023.md`）

### 交叉引用

使用 Obsidian wikilink 格式：`[[页面名]]` 或 `[[页面名|显示文本]]`。优先链接已有页面。

### 著作页额外要求

- Frontmatter 需包含 `citation_apa` 字段
- 正文标题下方需有 `引用：` 行，方便读者复制

## 标签体系

| 类型标签 | 说明 |
|----------|------|
| `concept` | 概念/批判分析 |
| `author` | 作者页 |
| `work` | 著作页 |
| `test` | 测试/量表 |

| 领域标签 | 说明 |
|----------|------|
| `neurodiversity` | 神经多样性 |
| `autism` | 孤独谱系 |
| `disability` | 残障 |
| `capitalism` | 资本主义批判 |

完整列表见 `wiki-schema.md#标签体系`。

## 提交流程

### 轻量页面贡献

请向 [wiki 页面镜像](https://github.com/xyzhou0323/wiki) 提交，并遵循该仓库的 [共建指南](https://github.com/xyzhou0323/wiki/blob/master/COLLABORATING.md)。如果新增单页，请指向主仓库中已经归档的来源；若来源尚未归档，则改走下面的专题级流程。

### 专题级贡献

1. Fork `ndwiki-cn` 主仓库。
2. 创建分支：`git checkout -b your-feature`。
3. 提交来源文件或完整来源清单，并按 `wiki-schema.md` 将资料归档到 `sources/`。
4. 在 `wiki/` 中新增或修改页面，补全 `sources`、frontmatter、导语和 `[[wikilinks]]`。
5. 同步更新受影响的 schema、知识地图、阅读路线和目录统计。
6. 提交前检查来源路径、内部链接、命名和重复页面；如本地环境可用，运行 lint 与 `llm-wiki sync`。
7. 在 PR 描述中列出新增及更新页面、来源、结构变化、已完成的检查，以及仍需重点复核的内容。
8. 提交 PR 到 `main` 分支。维护者会补充操作日志、索引同步和后续简繁同步。

涉及医疗安全、自伤、自杀、药物或其他高风险内容时，请在 PR 中单独列出相关页面及其主要依据，便于重点复核。

## 署名

如果你新建或大幅编辑了某个页面，欢迎在页面底部署名，可链接到你的个人网站、GitHub 主页或社交媒体：

```markdown
> 贡献者：[你的名字](https://your-website.com)
```

多人贡献时用顿号分隔：

```markdown
> 贡献者：[张三](https://zhangsan.dev)、[李四](https://github.com/lisi)
```

署名行放在页面正文末尾、wikilinks 之前。此字段非强制——署名与否由贡献者自行决定。

## 繁体中文版本

详见 README 协作章节。`zh-hant`（ISO 15924）涵盖所有繁体使用者（台湾、香港、澳门等），不预设地区。地区术语差异通过术语对照表处理。

简繁页面通过以下 frontmatter 字段互链：

```yaml
zh-hant: "[[wiki-zh-hant/对应页面]]"   # 简体页指向繁体
zh-hans: "[[wiki/对应页面]]"           # 繁体页指向简体
```

术语差异较大时可在正文加注，标明地区，如"孤独谱系（臺：自閉症譜系；港：自閉症譜系）"。
