# 神经多样性 Wiki

一个关于神经多样性（Neurodiversity）的中文知识库，涵盖核心概念、批判分析、历史脉络、研究实践、诊断现象、测试工具、作者与参考文献。由 AI 协助维护，Obsidian 兼容。

**312 个页面**，从[[阅读路线|入门]]到[[神经殊异马克思主义|批判]]递进组织。

### 关联仓库

| 仓库 | 说明 |
|------|------|
| [ndwiki-cn](https://github.com/xyzhou0323/ndwiki-cn)（本仓库） | 完整项目：wiki 页面 + 源文件 + 工具链 + 繁体子模块 |
| [wiki](https://github.com/xyzhou0323/wiki) | 纯 wiki 页面（Obsidian vault），方便直接 clone 用 Obsidian 打开 |
| [ndwiki-hant](https://github.com/xyzhou0323/ndwiki-hant) | 繁体中文版，ndwiki-cn 的 git submodule（`wiki-zh-hant/`） |

简体页面更新后，`sync-zh-hant.py --push` 自动转换并推送至 ndwiki-hant。

## 快速开始

**在线阅读**：[neuroxyz.cn/wiki](https://neuroxyz.cn/wiki/) 提供部署版本，无需安装任何软件。

**本地使用**：用 [Obsidian](https://obsidian.md) 打开本仓库即可浏览。入口：

- **新读者** → [[阅读路线]]：四层递进导航，四个起点
- **查概念** → [[00-知识地图|知识地图]]：八部分完整索引

## 目录结构

```
wiki/                    # Wiki 页面，简体中文（Obsidian vault）
  00-知识地图.md          # 总导航
  阅读路线.md             # 入门导航
  01-基础/               # 范式、术语、运动
  02-批判分析/            # 政治经济学、意识形态
  03-历史脉络/            # "正常"的发明与抵抗
  04-实践应用/            # 研究、教育、干预
  05-诊断与现象/          # ASD、ADHD、述情障碍等
  06-测试/               # 量表与工具
  authors/               # 124 位作者
  works/                 # 102 部参考文献
wiki-zh-hant/            # 繁体中文子模块 → ndwiki-hant 仓库
sources/                 # 原始文献（不可修改）
wiki-log.md              # 操作日志
```

## 协作

欢迎贡献！详细页面规范见 [COLLABORATING.md](COLLABORATING.md)。本项目采用“主仓库维护完整知识链路、页面仓库承接轻量协作、繁体仓库承接人工审校”的分工方式。

### 应该向哪个仓库提交

| 改动类型 | 提交位置 | 说明 |
|----------|----------|------|
| 错别字、措辞和链接修正，局部补充，来源明确且不改变结构的单页修改或新增 | [wiki](https://github.com/xyzhou0323/wiki) | 页面镜像适合直接在浏览器中完成轻量协作；维护者负责吸收必要的同步工作 |
| 多个相互关联页面、批量新增文献、完整专题、目录或标签体系调整、高风险健康内容 | [ndwiki-cn](https://github.com/xyzhou0323/ndwiki-cn)（本仓库） | 需要让原始资料、页面、结构、日志和索引作为同一批变更接受检查 |
| `needs-review: true` 页面的繁体审校、地区术语和表达调整 | [ndwiki-hant](https://github.com/xyzhou0323/ndwiki-hant) | 主要处理简体同步后的人工审校，不单独建立与简体来源链路脱节的新专题 |

这里没有机械的页面数量门槛。只要一项贡献需要批量归档来源、建立多个页面之间的结构、扩展 schema 或标签、更新全量知识地图，或会触发大规模繁体同步，就应当按“专题级摄入”从主仓库提交。若一个最初很小的页面 PR 在讨论中逐渐扩大，维护者可以请贡献者把它迁移到主仓库；原 PR 可以保留并与新的主仓库 PR 相互链接，不要求重写已经完成的内容。

### 为什么专题级改动必须经过主仓库

LLM Wiki 将知识维护分为彼此关联的几层：

1. `sources/` 保存不可变的原始资料，构成事实与引用的追溯基础。
2. `wiki/` 保存由资料摄入形成的知识页面；每个页面通过 frontmatter 的 `sources` 指回原始资料。
3. `wiki-purpose.md`、`wiki-schema.md`、[[00-知识地图]]和[[阅读路线]]维护范围、页面结构、标签和导航。
4. `wiki-log.md` 记录操作历史，`llm-wiki sync` 更新文件状态和搜索索引；lint 检查来源、frontmatter、链接和命名。
5. 简体页面确认后，再同步至 `ndwiki-hant` 供人工审校。

少量页面修订可以由维护者手动补齐这些环节；专题级改动则必须在主仓库中一次完成，避免原始资料、知识页面、索引和派生版本之间失去对应关系。

### 主仓库摄入流程

1. 将来源文件或来源清单随 PR 提供，并在 `sources/` 中完成归档。
2. 在 `wiki/` 中新增或修改页面，补全可追溯的 `sources`、规范 frontmatter 和 `[[wikilinks]]`。
3. 同步更新 schema、知识地图、目录统计和必要的导航页面。
4. 运行 lint 和 `llm-wiki sync`，并将操作追加到 `wiki-log.md`。
5. 简体内容通过复核后，再同步页面镜像和繁体仓库。

如果不确定改动属于哪一种，可以先提交草稿 PR 或 Issue；维护者会协助确定仓库和迁移方式。

### 繁体中文（zh-hant）

繁体中文版以 git submodule 形式存在於 `wiki-zh-hant/`，對應獨立倉庫 **[ndwiki-hant](https://github.com/xyzhou0323/ndwiki-hant)**。使用 ISO 15924 腳本代碼（`zh-hant` 涵蓋臺灣、香港、澳門等所有繁體使用者），不預設地區。

> **繁體協作者請直接前往 [ndwiki-hant](https://github.com/xyzhou0323/ndwiki-hant)，閱讀 [COLLABORATING.md](https://github.com/xyzhou0323/ndwiki-hant/blob/master/COLLABORATING.md) 瞭解完整審校流程。**

#### 協作流程

簡繁同步由 `sync-zh-hant.py` 腳本自動完成，人工審校是第二步：

1. **簡體維護者**編輯 `wiki/` 頁面後，執行：
   ```bash
   python .llm-wiki/sync-zh-hant.py --push
   ```
   OpenCC 轉換 → 標記 `needs-review: true` → 提交推送至 ndwiki-hant 倉庫。

2. **繁體協作者**在 [ndwiki-hant](https://github.com/xyzhou0323/ndwiki-hant) 中搜尋 `needs-review: true`，逐頁審校：
   - 修正 OpenCC 轉換不準確處（罕用詞或術語）
   - 統ㄧ地區術語差異（如簡"孤獨譜系"→臺"自閉症譜系"）
   - 確認 wikilinks 正確指向繁體頁面
   - 審校完畢後，移除 frontmatter 中的 `needs-review: true`
   - 提交 PR 到 ndwiki-hant

3. **初次全量轉換**：
   ```bash
   python .llm-wiki/sync-zh-hant.py --full --push
   ```
   全量模式不添加 `needs-review` 標記。後續日常更新用增量模式（不加 `--full`）。

#### 本地開發

如需同時開發簡體和繁體版本：

```bash
git clone --recurse-submodules https://github.com/xyzhou0323/ndwiki-cn.git
```

僅需繁體版本：

```bash
git clone https://github.com/xyzhou0323/ndwiki-hant.git
```

#### 交叉鏈接

每個繁體頁面 frontmatter 自動包含 `zh-hans: "[[wiki/對應頁面]]"`，簡體頁面包含 `zh-hant: "[[wiki-zh-hant/對應頁面]]"`，便於跨變體跳轉。

### 术语对齐

两岸三地神经多样性术语存在差异。建议在 wiki 内维护一份[[术语翻译对照表]]，记录简体、台湾繁体、香港繁体的对应关系，方便协作者跨变体编辑。

## 维护

本 Wiki 由 Claude Code 通过 `llm-wiki` 技能协助维护：

- **摄入**：新文献放入 `sources/`，AI 创建/更新对应页面
- **计数**：`python .llm-wiki/update-counts.py` 同步页面数量
- **简繁同步**：`python .llm-wiki/sync-zh-hant.py --push` 将简体变更 OpenCC 转为繁体并推送至子仓库
- **状态同步**：`llm-wiki sync` 追踪变更状态
- **日志**：每次操作追加至 `wiki-log.md`

## 署名

欢迎合作者在贡献的页面底部署名，可链接到个人网站。格式见 [COLLABORATING.md#署名](COLLABORATING.md#署名)。

## 学分

初始内容由 NeuroXYZ 团队整理，后续由 AI 协助扩展与维护。
