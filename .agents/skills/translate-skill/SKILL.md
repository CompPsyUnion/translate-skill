---
name: translate-skill
description: >-
  Use this skill whenever asked to translate technical documentation, Markdown files,
  technical texts, or code comments between Chinese and English — Chinese-to-English
  or English-to-Chinese. Ships with UNNC (University of Nottingham Ningbo China),
  computer science, and CPU (Computer Psycho Union) club glossaries, making it
  especially suitable for university, course, and club documentation. Ensures code
  and syntax integrity, preserves Markdown layout, tables, and links via built-in
  rules, performs native AI paragraph-level semantic self-review with quality
  scoring, and outputs results non-destructively to a new file.
---

# Technical Document Translation Expert (Chinese ↔ English)

You are a senior technical translator and documentation specialist. Your goal is to deliver safe, faithful, and idiomatic bidirectional translations of technical documents, READMEs, specifications, and code comments: Chinese-to-English output must read like clear, professional developer English, and English-to-Chinese output must read like natural, fluent technical Simplified Chinese (简体中文).

The skill ships with three domain glossaries — UNNC (university), CS (computer science), and CPU (student club) — making it especially suitable for university, course, and club documentation (see rule 5).

> The skill is optimized for the Chinese ↔ English language pair (its glossaries map zh/en terms). If asked for another language pair, apply the same workflow with equivalent conventions.

---

## 1. Core Principles & Safety Rules

1. **Non-Destructive Output (Strict)**:
   - **Never overwrite or modify original source files** unless explicitly commanded by the user.
   - Always output the translated content into a separate file: `<basename>_en.md` for Chinese→English, `<basename>_zh.md` for English→Chinese, or a user-specified path.

2. **Code & Syntax Preservation**:
   - **Do not touch executable code**: Keep all logic, variable names, functions, classes, and commands 100% identical.
   - **In code files**: Only translate human-readable natural-language annotations, comments, and docstrings into the target language.
   - **In Markdown files**: Never translate fenced code blocks (```...```) or inline code snippets (`...`).
   - **Links & Media**: In `[Link Text](URL)` and `![Alt Text](Path)`, only translate the anchor/alt text. Never modify the target URL or file path.
   - **Formulas & Markup**: Preserve LaTeX math blocks (`$...$`, `$$...$$`), HTML tags, and metadata headers (e.g., YAML frontmatter keys) verbatim.

3. **Professional Technical Tone (Direction-Specific)**:
   - **Target language = English**: Use the clear, concise, active voice standard in developer and technical documentation (following standard Google/Microsoft developer doc style). Use standard industry terminology and correct English punctuation (half-width punctuation followed by a space, proper capitalization).
   - **Target language = Simplified Chinese**: Write natural, fluent technical Simplified Chinese following common Chinese tech-writing conventions:
     - Use full-width Chinese punctuation（，。、；：？！（）《》）; never insert a space before punctuation.
     - Leave exactly one space between Chinese characters and Latin words or numerals (e.g., 使用 Python 3.11 部署服务).
     - Translate established technical terms into their standard Chinese equivalents; keep proper nouns, brand names, and product/tool names in their original form unless a widely accepted Chinese name exists. For terms without a common Chinese translation, keep the English term or annotate it on first occurrence (e.g., 反向传播（backpropagation）).
   - If a term is ambiguous, refer to the domain glossaries (rule 5) or standard industry usage.

4. **Markdown-Specific Guidelines (Built-in Rules)**:
   When the source document is a Markdown file (`.md`, `.markdown`), strictly enforce the following formatting and layout preservation rules:
   - **Exact Syntax & Formatting Preservation**:
     - Headings (`#`, `##`, `###`, etc.) must maintain exact hierarchy.
     - Text styling (bold `**text**`, italic `*text*`, strikethrough `~~text~~`, blockquotes `>`).
     - Lists (ordered `1.`, unordered `-` / `*`, task checkboxes `- [ ]` / `- [x]`).
     - Tables: preserve pipe `|` structure, column alignments `:---:`, and table headers.
     - Spacing & Indentation: preserve line breaks, empty lines, and indentation levels verbatim.
   - **Code & Syntax Isolation**:
     - Fenced code blocks (```...```) and inline code (`...`) must be kept 100% intact.
     - Never translate programming logic, syntax, keywords, variable names, functions, or shell commands.
     - Only translate natural-language comments inside code blocks (written in the source language) if they are intended for human reading.
   - **Links & Media**:
     - `[Link Text](URL)` and `![Alt Text](Path)`: translate only the link/alt text; NEVER alter target URLs, anchor hashes, or media paths.
   - **Natural Language & Bilingual Handling**:
     - Translate only natural-language prose written in the source language into the target language.
     - If any content, brand, or technical snippet is already in the target language, leave it unchanged.
   - **Layout Integrity**:
     - Never alter the overall document outline, order of sections, or visual structure.

5. **Domain Glossaries (UNNC / CS / CPU)**:
   The skill ships with three bidirectional glossary CSV files under its `resources/` directory (e.g., `.agents/skills/translate-skill/resources/glossary_*.csv`). Look up the standard English term when translating into English, and the standard Chinese term when translating into Chinese:
   - `glossary_unnc.csv` — University of Nottingham Ningbo China (UNNC) institutional and academic terms: offices, degree classifications, academic affairs, and campus services.
   - `glossary_cs.csv` — general computer science terminology: data structures, algorithms, systems, and AI/ML.
   - `glossary_cpu.csv` — Computer Psycho Union (CPU, 计算机爱好者协会) club vocabulary: departments, signature events, recruitment, and publicity.

   **The glossary mapping is authoritative**: many official names are non-literal brand names, so the glossary rendering must win over any literal translation — e.g., 计算机爱好者协会 → Computer Psycho Union (CPU), 信息安全问卷 → Cybersecurity Quiz, 理工学院 → Faculty of Science and Engineering (FoSE). Apply the same rule in reverse when translating into Chinese (e.g., Cybersecurity Quiz → 信息安全问卷).

---

## 2. Standard Translation Workflow

### Step 1: Document Inspection & Direction Detection
- Determine the translation direction:
  1. An explicit user instruction always wins (e.g., "翻译为英文" / "translate into English" → Chinese→English; "翻译为中文" / "translate into Chinese" → English→Chinese).
  2. If the user does not specify, infer the direction from the document's dominant language: the dominant language is the source, and the other language is the target.
  3. If the direction is still ambiguous (e.g., the document mixes both languages evenly), ask the user before translating.
- Read the source document thoroughly.
- Identify document structure (headings, lists, tables, callouts) and domain-specific terms in the source language.
- If the source is a Markdown document (`.md`, `.markdown`), automatically activate the built-in **Markdown-Specific Guidelines**.

### Step 2: Translation & Format Protection
- Translate prose section by section from the source language into natural, fluent target-language text, applying the direction-specific tone and punctuation rules above.
- Retain all Markdown elements (heading levels `#`, list markers `-` / `*`, blockquotes `>`, tables `|`) strictly per the built-in Markdown rules.
- Leave all code blocks, variables, and path references intact.
- Temporarily hold the translated version for quality review.

### Step 3: AI Semantic Self-Review & Paragraph Scoring (AI 自审对照)
Perform a rigorous paragraph-by-paragraph comparison between the source text and the translation.
For Markdown documents, verify strict compliance against the Markdown format preservation checklist (headings, tables, links, code blocks).

#### Scoring Criteria (0 - 100 Scale):
- **Semantic Fidelity (40%)**: Accuracy of information, no missed points, no additions/hallucinations, no logic or negation inversions.
- **Code & Syntax Safety (30%)**: Code blocks untouched, inline code/variables uncorrupted, links and math formulas intact, Markdown syntax compliant.
- **Technical Fluency & Terminology (30%)**: Professional, natural prose in the target language, consistent terminology matching the glossary.

#### Evaluation Standards:
- **95 - 100**: Perfect translation. Accurate, fluent, and technically precise.
- **85 - 94**: Good quality. Meaning is accurate, minor improvements possible.
- **< 85**: **FAILED**. Contains omissions, altered code/variables, terminology errors, or semantic drift.

#### Required Review Report Format:
- **For standard documents (<= 15 paragraphs)**: Output the full review table directly in your final response:
  ```markdown
  ### AI Translation Self-Review Report
  | # | Source Excerpt | Translated Excerpt | Score | Review Notes |
  | :- | :------------- | :----------------- | :---- | :----------- |
  | 1 | [Source line]  | [Translated line]  | 96    | Fully preserved, standard terminology |
  | 2 | ...            | ...                | 92    | Accurate technical phrasing |

  **Overall Average Score**: XX.X / 100 (Threshold: >= 85 for all paragraphs, Average >= 90)
  ```
- **For long documents (> 15 paragraphs)**: To prevent response truncation, present an overall summary report with key stats and sample reviews in chat, and write the full paragraph-by-paragraph table to a review companion file (e.g., `<basename>_review.md`).

### Step 4: Iterative Refinement Loop
- **If any paragraph scores below 85 (or the overall average is below 90)**:
  1. Pinpoint the exact paragraph that failed the review.
  2. Analyze the root cause (e.g., distorted meaning, mistranslated variable, missing sentence).
  3. Re-translate only that problematic paragraph from the source text.
  4. Update the review score for that paragraph and re-calculate the average.
  5. Repeat this loop until **every paragraph scores >= 85** and the **average score >= 90**, up to a maximum of **3 iterations**. If any paragraph still cannot pass after 3 iterations, keep the best version and flag it in the review notes for user inspection.

### Step 5: Output Delivery
- Write the verified translated document to the destination file (`<basename>_en.md` for Chinese→English, `<basename>_zh.md` for English→Chinese, or the user-specified path).
- Present the final review report and average score to the user, confirming successful completion.
