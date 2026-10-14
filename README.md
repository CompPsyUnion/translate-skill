# translate-skill

[English](#english) | [中文](#中文)

---

## English

An AI agent skill specification for bidirectional technical document translation between Chinese and English (Chinese→English / English→Chinese), shipping with three domain glossaries. **Especially suitable for UNNC (University of Nottingham Ningbo China), School of Computer Science (CS), and CPU (Computer Psycho Union) scenarios**, including university institution and degree-system documents, course notes and study materials, and club activity or recruitment publicity.

Through structured prompt instructions and workflow constraints, this skill guides AI coding assistants (e.g., Claude Code, Cursor, Antigravity, or any environment supporting the agent skill specification) to deliver high-quality **bidirectional translation between Chinese and English technical documents**. Its core objective: keep code, links, and formatting untouched while the AI performs paragraph-by-paragraph self-review with quantitative scoring.

Maintained by the **Computer Psycho Union (CPU) at the University of Nottingham Ningbo China (UNNC)**.

---

## Background & Use Cases

Beyond general technical translation, the skill ships with three domain glossaries, making it **especially suitable** for:

| Use Case | Glossary | Sample Mapping |
| :-- | :-- | :-- |
| **UNNC university documents**: institutions, degree system, academic affairs, campus services | `glossary_unnc.csv` | 一等荣誉学位 → First-class Honours Degree; 教务处 → Academic Services Office |
| **CS study materials**: course notes, algorithms and data structures, AI/ML terms | `glossary_cs.csv` | 渐进分析 → Asymptotic Analysis; 大语言模型 → Large Language Model |
| **CPU club documents**: department structure, signature events, recruitment and publicity | `glossary_cpu.csv` | 信息安全问卷 → Cybersecurity Quiz; 技术部 → Tech Group |

Typical use cases: bilingual WeChat article publishing, side-by-side course notes, translating tech-sharing session and workshop materials, internationalizing recruitment publicity.

> **Tip**: many university and club official names have **fixed, non-literal renderings** (e.g., 信息安全问卷 → Cybersecurity Quiz). The skill enforces the official glossary rendering instead of literal translation; the glossaries are bidirectional, so English→Chinese translation back-translates through the same tables.

---

## Usage

### 1. Deploy to a Project

#### Option A: install via package manager

Add it directly from the command line:

```bash
npx skills add CompPsyUnion/translate-skill
```

#### Option B: manual copy

Copy the `.agents/skills/translate-skill` directory into the root of your target project.

#### Option C: use the prompt template directly (no skill install)

If loading the skill into your project root is inconvenient, use [docs/prompt_for_md.md](./docs/prompt_for_md.md) directly as a prompt template. It is a **single, all-in-one bidirectional template** (direction auto-detected): copy and paste it into any mainstream LLM (ChatGPT, Claude, Gemini, DeepSeek, Cursor, etc.), then paste the document to translate into the source slot at the end of the prompt to translate Markdown directly.

---

### 2. Invoke a Translation

Enter a translation request in an agent that supports skill invocation (state the target language; the direction can be auto-detected), for example:

```text
请使用 translate-skill 将 README.md 翻译为英文。
Please use translate-skill to translate README.md into Chinese.
```

The agent detects the direction from your instruction or the document language (Chinese→English / English→Chinese), activates `SKILL.md`, performs the translation, and outputs the self-review table.

---

## How It Works

The skill relies entirely on the AI agent executing the task.

The overall workflow:

1. **Direction detection & source parsing**: determine the direction from the user instruction or the document's dominant language; identify the Markdown structure (headings, paragraphs, lists, code blocks, tables, formulas) and source-language technical terms; for Markdown documents, activate the **built-in Markdown layout-protection rules** of `SKILL.md` automatically.
2. **Rule-based translation**: keep code blocks, inline code, formulas, and link URLs untouched; translate only natural-language text into the target language.
3. **Paragraph-level self-review & scoring**: the AI compares source and translation paragraph by paragraph, scores each paragraph (0-100), and computes the average.
4. **Re-translation on failure**: if any paragraph scores below 85 or the average falls below 90, the AI re-translates the failing paragraphs (up to 3 loops) until the thresholds are met.
5. **Non-destructive output**: save the final translation to a separate file (`_en.md` by default for Chinese→English, `_zh.md` for English→Chinese); the source file is never overwritten.

---

## Core Rules

- **Language direction (bidirectional)**:
   - Supports both **Chinese → professional English** and **English → natural Simplified Chinese**, with the direction detected from the user instruction or the document language.
   - Code, proper nouns, and content already in the target language stay untouched; only source-language natural language is translated.
   - **Additional conventions for English → Chinese**: full-width Chinese punctuation; exactly one space between Chinese and Latin characters or numerals (e.g., 使用 Python 3.11); back-translate terminology through the glossaries to the standard Chinese names; keep terms without an established translation in English, or annotate the original on first occurrence (e.g., 反向传播（backpropagation）).
- **Code & format protection (Markdown rules built into the SKILL)**:
   - Fenced code blocks (```...```) and inline code (`...`) stay verbatim.
   - Link and image syntax: translate only the display text; keep target URLs and paths unchanged.
   - LaTeX math (`$...$` and `$$...$$`) stays verbatim.
   - YAML frontmatter structure stays verbatim.
   - Heading levels, lists, table alignment, and indentation stay exactly as in the source.
- **Non-destructive writing**:
   - Output goes to a new file (e.g., `document_en.md`) by default; never modify or overwrite the source file.
- **Paragraph-level scoring criteria**:
   - Semantic fidelity (40%): complete information, no omissions, no hallucinated additions, correct logic.
   - Syntax & code safety (30%): code, variables, links, and formulas undamaged.
   - Technical writing quality (30%): idiomatic for the target language, accurate terminology.
- **Terminology management**:
   - Maintain proper-noun mappings centrally in the skill's `resources` directory.

---

## Repository Layout

```text
translate-skill/
├── docs/
│   └── prompt_for_md.md                  # All-in-one bidirectional Markdown translation prompt (direction auto-detected, no skill install needed)
├── .agents/
│   └── skills/
│       └── translate-skill/
│           ├── SKILL.md                  # Core skill instructions and self-review workflow (Markdown rules built in)
│           ├── resources/                # Glossary directory (CSV)
│           │   ├── glossary_cpu.csv      # CPU club glossary (departments / events / recruitment)
│           │   ├── glossary_cs.csv       # General computer science glossary
│           │   └── glossary_unnc.csv     # UNNC institutional and academic glossary
│           └── examples/                 # Bilingual translation reference examples (both directions)
│               ├── example01/            # Stack vs. heap (stack_and_heap.md / stack_and_heap_en.md)
│               └── example02/            # Docker architecture and commands (docker.md / docker_en.md)
├── README.md                             # Project documentation (bilingual)
└── LICENSE                               # MIT License
```

---

## Self-Review Report Format

After each translation, the agent produces a self-review table like this:

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

> **Note**: the table above shows Chinese→English; English→Chinese works the same way (swap the languages of the two columns). For long documents (> 15 paragraphs), the full paragraph-by-paragraph report is written to a separate `<basename>_review.md`, with only a summary and the average shown in chat, to avoid exceeding the token limit of a single response.

---

## Glossary Configuration

Add or edit project terminology mappings in the CSV files under [.agents/skills/translate-skill/resources](./.agents/skills/translate-skill/resources).

The glossaries are bidirectional Chinese-English mapping tables: look up the standard English term when translating into English, and back-translate to the standard Chinese term when translating into Chinese.

Three glossaries are currently provided:

- `glossary_cpu.csv`: CPU club proper nouns (departments, signature events, recruitment publicity)
- `glossary_cs.csv`: general computer science terminology
- `glossary_unnc.csv`: UNNC institutions, degree classifications, and academic affairs

---

## License

[MIT License](./LICENSE)

---

## 中文

专用于中英技术文档互译（中译英 / 英译中）的 AI Agent 技能规范，内置三套领域术语表，**适用于 UNNC（宁波诺丁汉大学）、计算机科学系（CS）、CPU（计算机爱好者协会）相关场景**，包括院校机构与学位体系文书、课程笔记与学习资料、社团活动与招新宣传物料。

本技能通过结构化的提示词指令与流程约束，引导 AI 编程助手（如 Claude Code、Cursor、Antigravity 等支持 Agent 技能规范的环境）高质量完成**中文与英文技术文档的双向翻译**。核心目标是在保证代码、链接与排版格式不被改动的前提下，由 AI 执行逐段对照自审与量化评分。

本技能由 **宁波诺丁汉大学（UNNC）计算机爱好者协会（Computer Psycho Union, CPU）** 出品维护。

---

## 背景与适用场景

除通用技术文档互译外，本技能内置三套领域术语表，对以下场景**尤其适用**：

| 适用场景 | 对应术语表 | 对照示例 |
| :-- | :-- | :-- |
| **UNNC 院校文档**：机构设置、学位体系、学术事务与校园服务 | `glossary_unnc.csv` | 一等荣誉学位 → First-class Honours Degree；教务处 → Academic Services Office |
| **CS 计算机科学资料**：课程笔记、算法与数据结构、AI/ML 术语 | `glossary_cs.csv` | 渐进分析 → Asymptotic Analysis；大语言模型 → Large Language Model |
| **CPU 社团文档**：部门架构、品牌活动、招新与宣传物料 | `glossary_cpu.csv` | 信息安全问卷 → Cybersecurity Quiz；技术部 → Tech Group |

典型用例：社团公众号推文双语化、课程笔记中英对照、技术分享会与工作坊材料翻译、招新宣传物料国际化等。

> **提示**：院校与社团的许多官方名称为**非字面对应的固定译名**（如「信息安全问卷 → Cybersecurity Quiz」）。技能会强制采用术语表中的官方译名而非逐字直译；术语表双向通用，英译中时同样按表回译。

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

如果不方便将 Skill 载入到目标项目根目录，可以直接使用 [docs/prompt_for_md.md](./docs/prompt_for_md.md) 作为提示词模板。它是一份**一体式双向模板**（中译英 / 英译中方向自动判定），将其复制粘贴到任意主流大模型（如 ChatGPT、Claude、Gemini、DeepSeek、Cursor 等）中，把待翻译文档粘贴到提示词末尾的源文档槽位即可直接完成 Markdown 翻译。

---

### 2. 调用翻译

在支持技能调用的 AI Agent 中输入翻译需求（指明目标语言，方向可自动判定），例如：

```text
请使用 translate-skill 将 README.md 翻译为英文。
Please use translate-skill to translate README.md into Chinese.
```

Agent 会根据指令或文档语言自动判定翻译方向（中译英 / 英译中），激活 `SKILL.md`，执行翻译并输出自审表格。

---

## 运行机制

本技能完全依赖执行任务的 AI Agent 本身。

整体工作流程如下：

1. **方向判定与源文档解析**：根据用户指令或文档主导语言判定翻译方向（中译英 / 英译中）；识别 Markdown 结构（标题、段落、列表、代码块、表格、公式）与源语言技术术语；若为 Markdown 文档，自动激活 `SKILL.md` **内置的 Markdown 专项排版保护规则**。
2. **规则化翻译**：保护代码块、行内代码、公式及链接 URL 不被修改，仅将源语言自然语言文本翻译为目标语言。
3. **逐段自审打分**：AI 对照原文与译文，按照既定标准对每个段落进行量化评分（0-100 分），并计算平均分。
4. **未达标重译**：若存在段落得分低于 85 分或总体平均分低于 90 分，AI 需重新翻译未达标段落（最多循环 3 次），直至符合要求。
5. **独立输出**：将最终译文保存至独立文件（中译英默认以 `_en.md` 结尾，英译中默认以 `_zh.md` 结尾），不覆盖原文件。

---

## 核心规则

- **语言方向（中英双向）**：
   - 支持**中文翻译为专业英文**与**英文翻译为自然简体中文**，按用户指令或文档语言自动判定方向。
   - 原文中的代码、专有名词、已为目标语言的内容保持原样，仅将源语言自然语言翻译为目标语言。
   - **英译中附加规范**：使用全角中文标点；中文与英文、数字之间留一个空格（如「使用 Python 3.11」）；术语按术语表回译为标准中文译名，无通用译法的术语保留英文或在首次出现时括注原文（如「反向传播（backpropagation）」）。
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
   - 技术写作专业度（30%）：符合目标语言技术文档写作习惯，术语使用准确。
- **术语管理**：
   - 支持通过技能专属的 `resources` 文件夹统一维护专有名词对照。

---

## 目录结构

```text
translate-skill/
├── docs/
│   └── prompt_for_md.md                  # 一体式 Markdown 中英互译提示词模板（方向自动判定，免 Skill 直接使用）
├── .agents/
│   └── skills/
│       └── translate-skill/
│           ├── SKILL.md                  # 核心技能指令与自审自纠工作流（内置 Markdown 规则）
│           ├── resources/                # 术语对照表目录 (CSV)
│           │   ├── glossary_cpu.csv      # CPU 社团术语表（部门/活动/招新）
│           │   ├── glossary_cs.csv       # 计算机科学通用术语表
│           │   └── glossary_unnc.csv     # UNNC 院校与学术事务术语表
│           └── examples/                 # 中英对照翻译参考示例（双向通用）
│               ├── example01/            # 内存栈与堆解析对照 (stack_and_heap.md / stack_and_heap_en.md)
│               └── example02/            # Docker 架构与常用命令对照 (docker.md / docker_en.md)
├── README.md                             # 项目说明文档（中英双语）
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

> **注**：上表以中译英为例，英译中方向同理（Source 与 Translated 两列语言互换）。对于段落较多（> 15 段）的长篇文档，完整逐段自审报告将输出到独立的 `<basename>_review.md` 中，聊天窗口中输出概览与平均分，防止单次对话超出 Token 限制。

---

## 术语表配置

可以在 [.agents/skills/translate-skill/resources](./.agents/skills/translate-skill/resources) 目录下的 CSV 文件中添加或修改项目专业术语对照。

术语表为中英对照映射表，**双向通用**：中译英时用于查询标准英文术语，英译中时用于回译标准中文译名。

目前提供以下三个术语表：

- `glossary_cpu.csv`：CPU 社团专有名词对照（部门架构、品牌活动、招新宣传）
- `glossary_cs.csv`：计算机科学通用专业术语表
- `glossary_unnc.csv`：UNNC 院校机构、学位体系与学术事务术语表

---

## 许可证

[MIT License](./LICENSE)
