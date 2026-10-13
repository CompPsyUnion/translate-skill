# translate-skill

专用于中文技术文档翻译为英文（中译英）的 AI Agent 技能规范。

本技能通过结构化的提示词指令与流程约束，引导 AI 编程助手（如 Claude Code、Cursor、Antigravity 等支持 Agent 技能规范的环境）高质量完成**中文技术文档到英文**的翻译工作。核心目标是在保证代码、链接与排版格式不被改动的前提下，由 AI 执行逐段对照自审与量化评分。

---

## 使用方式

### 1. 部署到项目

#### 方式 A：通过包管理器安装

可通过命令行直接添加：

```bash
npx skills add CompPsyUnion/translate-skill
```

#### 方式 B：手动复制

将 `.agents/skills/translate-skill` 目录复制到目标项目的根目录下。

#### 方式 C：直接使用提示词模板（免载入 Skill）

如果不方便将 Skill 载入到目标项目根目录，可以直接使用 [docs/prompt_for_md.md](./docs/prompt_for_md.md) 作为提示词模板。将其复制粘贴到任意主流大模型（如 ChatGPT、Claude、Gemini、DeepSeek、Cursor 等）中，替换其中的中文内容即可直接完成 Markdown 翻译。

---

### 2. 调用翻译

在支持技能调用的 AI Agent 中输入翻译需求（明确为中文转英文），例如：

```text
请使用 translate-skill 将 README.md 翻译为英文。
```

Agent 会自动激活 `SKILL.md`，执行翻译并输出自审表格。

---

## 运行机制

本技能完全依赖执行任务的 AI Agent 本身。

整体工作流程如下：

1. **源文档解析**：识别 Markdown 结构（标题、段落、列表、代码块、表格、公式）与中文技术术语；若为 Markdown 文档，自动激活 `SKILL.md` **内置的 Markdown 专项排版保护规则**。
2. **规则化翻译**：保护代码块、行内代码、公式及链接 URL 不被修改，仅翻译中文自然语言文本。
3. **逐段自审打分**：AI 对照中文原文与英文译文，按照既定标准对每个段落进行量化评分（0-100 分），并计算平均分。
4. **未达标重译**：若存在段落得分低于 85 分或总体平均分低于 90 分，AI 需重新翻译未达标段落（最多循环 3 次），直至符合要求。
5. **独立输出**：将最终译文保存至独立文件（默认以 `_en.md` 结尾），不覆盖原文件。

---

## 核心规则

- **语言方向**：
  - 明确为**中文翻译为专业英文**。
  - 原文中的代码、专有名词、已为英文的内容保持原样，仅将中文自然语言翻译为英文。
- **代码与格式保护（SKILL 内置 Markdown 规则）**：
  - 围栏代码块（```...```）与行内代码（`...`）保持原样。
  - 超链接与图片语法仅翻译显示文本，保留目标 URL 与路径。
  - LaTeX 数学公式（`$...$` 与 `$$...$$`）原样保留。
  - YAML Frontmatter 头部结构保持原样。
  - 标题层级、列表、表格对齐与缩进格式完全保持一致。
- **非破坏性写入**：
  - 默认输出为新文件（例如 `document_en.md`），严禁直接修改或覆盖源文件。
- **逐段自审打分标准**：
  - 语义保真度（40%）：信息完整，无漏译，无无中生有的增添，逻辑关系正确。
  - 语法与代码安全（30%）：代码、变量、链接与公式未受损坏。
  - 技术英语专业度（30%）：符合英文技术文档写作习惯，术语使用准确。
- **术语管理**：
  - 支持通过技能专属的 `resources` 文件夹统一维护专有名词对照。

---

## 目录结构

```text
translate-skill/
├── docs/
│   └── prompt_for_md.md                  # 独立 Markdown 中译英提示词模板（免 Skill 直接使用）
├── .agents/
│   └── skills/
│       └── translate-skill/
│           ├── SKILL.md                  # 核心技能指令与自审自纠工作流（内置 Markdown 规则）
│           ├── resources/                # 术语对照表目录 (CSV)
│           │   ├── glossary_cpu.csv      # CPU 体系相关术语表
│           │   ├── glossary_cs.csv       # 计算机科学通用术语表
│           │   └── glossary_unnc.csv     # 专业课程与院校术语表
│           └── examples/                 # 翻译参考示例
│               ├── example01/            # 内存栈与堆解析对照 (stack_and_heap.md / stack_and_heap_en.md)
│               └── example02/            # Docker 架构与常用命令对照 (docker.md / docker_en.md)
├── README.md                             # 项目说明文档
└── LICENSE                               # MIT 许可证
```

---

## 自审报告格式

翻译完成后，Agent 会生成如下类似格式的自审对照表：

```markdown
### AI Translation Self-Review Report

| # | Source Excerpt | Translated Excerpt | Score | Review Notes |
| :- | :------------- | :----------------- | :---- | :----------- |
| 1 | # 高性能缓存服务设计规范 | # High-Performance Cache Service Design Specification | 98 | 术语对应准确 |
| 2 | 本项目提供基于分布式架构的... | This project provides high-performance cache... | 95 | 结构完整，表述自然 |
| 3 | `redis-cluster` >= 7.0 | `redis-cluster` >= 7.0 | 100 | 表格与行内代码保持不变 |
| 4 | [官方安全指南](https://...) | [Official Security Guide](https://...) | 98 | 仅翻译文字，链接完好 |
| 5 | $$HitRate = \frac{TotalHits}...$$ | $$HitRate = \frac{TotalHits}...$$ | 100 | 数学公式完整保留 |

**Overall Average Score**: 98.2 / 100 (Threshold: All >= 85, Average >= 90)
**Status**: PASSED
```

> **注**：对于段落较多（> 15 段）的长篇文档，完整逐段自审报告将输出到独立的 `<basename>_review.md` 中，聊天窗口中输出概览与平均分，防止单次对话超出 Token 限制。

---

## 术语表配置

可以在 [.agents/skills/translate-skill/resources](./.agents/skills/translate-skill/resources) 目录下的 CSV 文件中添加或修改项目专业术语对照。

目前提供以下三个术语表：
- `glossary_cpu.csv`：社团与学生组织相关专有名词对照
- `glossary_cs.csv`：计算机科学通用专业术语表
- `glossary_unnc.csv`：院校、机构与课程专业术语表

---

## 许可证

[MIT License](./LICENSE)
