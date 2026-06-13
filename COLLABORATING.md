# 贡献指南

欢迎为神经多样性 Wiki 贡献内容。以下是操作规范和流程。

## 页面规范

每个 Wiki 页面遵循 `wiki-schema.md` 定义的格式：

### 必需 Frontmatter

```yaml
---
title: 页面标题
description: 一句话摘要
aliases: [英文/缩写, 中文别名, ...]  ← 首个为英文或缩写（部署 URL）
tags: [类型标签, 领域标签]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

### 命名规则

- 概念页：中文 kebab-case（如 `神经多样性教育.md`）
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

1. Fork 本仓库
2. 创建分支：`git checkout -b your-feature`
3. 遵循上述规范编辑页面
4. 提交前确保 wikilinks 指向的页面存在
5. 提交 PR 到 `main` 分支，描述变更内容

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
