# 神经多样性 Wiki

一个关于神经多样性（Neurodiversity）的中文知识库，涵盖核心概念、批判分析、历史脉络、研究实践、诊断现象、测试工具、作者与参考文献。由 AI 协助维护，Obsidian 兼容。

**270 个页面**，从[[阅读路线|入门]]到[[神经殊异马克思主义|批判]]递进组织。

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
  04-体验与实践/          # 研究、教育、干预
  05-诊断与现象/          # ASD、ADHD、述情障碍等
  06-测试/               # 量表与工具
  authors/               # 104 位作者
  works/                 # 84 部参考文献
wiki-zh-hant/            # 繁体中文子模块 → ndwiki-hant 仓库
sources/                 # 原始文献（不可修改）
wiki-log.md              # 操作日志
```

## 协作

欢迎贡献！详细规范见 [COLLABORATING.md](COLLABORATING.md)。大致流程：

1. Fork 本仓库，在 `wiki/` 中新建或编辑页面
2. 遵循 [[wiki-schema|Wiki Schema]] 的命名规范、Frontmatter 和标签体系
3. 使用 `[[wikilinks]]` 交叉引用已有页面
4. 提交 PR 到 `main` 分支

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

两岸三地神经多样性术语存在差异。建议在 wiki 内维护一份[[术语对照表]]，记录简体、台湾繁体、香港繁体的对应关系，方便协作者跨变体编辑。

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
