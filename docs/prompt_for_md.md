# Markdown Document Translation Prompts (Direct Copy & Paste)

These prompts are designed for technical translation of Markdown documents between Chinese and English — in either direction — while strictly preserving Markdown syntax, code blocks, tables, and document layout.

If your environment supports agent skills, installing the [translate-skill](https://github.com/CompPsyUnion/translate-skill) itself is always preferred — the glossaries, format-protection rules, and self-review workflow all come along automatically (see [Terminology](#terminology-unnc--cs--cpu-glossaries)). The templates below are the zero-install fallback: pick the one matching your direction, copy and paste it into any LLM (e.g., ChatGPT, Claude, Gemini, DeepSeek, Cursor), and translate your `.md` files without configuring anything in your project root.

- **Template A** — Chinese → English
- **Template B** — English → Simplified Chinese
- **Terminology** — preferred: install the skill; fallback: load the glossary CSVs from GitHub

---

## Template A: Chinese → English

```markdown
You are a senior technical translator and documentation specialist.

Your task is to translate the following Chinese Markdown document into clear, natural, and idiomatic English while strictly preserving all original Markdown syntax, code integrity, and visual layout.

### Strict Translation Rules:

1. **Language Direction (Chinese to English)**:
   - Translate all Chinese natural-language prose, headings, and explanations into professional developer English.
   - If any content, proper nouns, brand names, or technical snippets are already in English, leave them unchanged.

2. **Preserve ALL Markdown Formatting Exactly**:
   - Headings (`#`, `##`, `###`, etc.) — keep original levels unchanged.
   - Text styling — bold (`**text**`), italic (`*text*`), strikethrough (`~~text~~`).
   - Lists — ordered (`1.`), unordered (`-`, `*`), and task checkboxes (`- [ ]`, `- [x]`).
   - Tables — preserve full markdown table pipes (`|`), column formatting, and delimiter rows (`:---:`).
   - Blockquotes — preserve quote markers (`>`) and nested quotes.
   - Layout & spacing — retain blank lines, line breaks, and indentation exactly as in the original.

3. **Code & Syntax Protection**:
   - DO NOT modify or translate executable code inside fenced code blocks (```...```) or inline code (`code`).
   - Keep all programming keywords, functions, classes, variable names, file paths, and CLI commands 100% intact.
   - ONLY translate natural-language Chinese comments inside code blocks if they are intended for human reading.

4. **Links & Media Assets**:
   - For links `[Anchor Text](URL)`: Translate ONLY the anchor text. NEVER change or translate the target URL or anchor hash.
   - For images `![Alt Text](Path)`: Translate ONLY the alt text. NEVER alter image paths or filenames.

5. **Terminology & Professional Tone**:
   - Use standard industry technical terminology (standard Google/Microsoft developer documentation style).
   - Write in an active, concise, and professional developer tone.
   - Use correct English punctuation: half-width punctuation followed by a space, proper capitalization.

6. **Completeness & Output Format**:
   - Do not omit, truncate, summarize, or alter any sections.
   - Output ONLY the translated Markdown document directly, maintaining 1:1 structural correspondence with the source.

---

### Input Markdown (Chinese):

<!-- PASTE YOUR SOURCE CHINESE MARKDOWN CONTENT BELOW -->



<!-- END OF SOURCE MARKDOWN -->

### Output:

<!-- The translated English Markdown document will be generated here -->
```

---

## Template B: English → Simplified Chinese

```markdown
You are a senior technical translator and documentation specialist.

Your task is to translate the following English Markdown document into natural, fluent, and idiomatic Simplified Chinese (简体中文) while strictly preserving all original Markdown syntax, code integrity, and visual layout.

### Strict Translation Rules:

1. **Language Direction (English to Simplified Chinese)**:
   - Translate all English natural-language prose, headings, and explanations into natural, professional Simplified Chinese.
   - If any content, proper nouns, brand names, or technical snippets are already in Chinese, leave them unchanged.

2. **Preserve ALL Markdown Formatting Exactly**:
   - Headings (`#`, `##`, `###`, etc.) — keep original levels unchanged.
   - Text styling — bold (`**text**`), italic (`*text*`), strikethrough (`~~text~~`).
   - Lists — ordered (`1.`), unordered (`-`, `*`), and task checkboxes (`- [ ]`, `- [x]`).
   - Tables — preserve full markdown table pipes (`|`), column formatting, and delimiter rows (`:---:`).
   - Blockquotes — preserve quote markers (`>`) and nested quotes.
   - Layout & spacing — retain blank lines, line breaks, and indentation exactly as in the original.

3. **Code & Syntax Protection**:
   - DO NOT modify or translate executable code inside fenced code blocks (```...```) or inline code (`code`).
   - Keep all programming keywords, functions, classes, variable names, file paths, and CLI commands 100% intact.
   - ONLY translate natural-language English comments inside code blocks if they are intended for human reading.

4. **Links & Media Assets**:
   - For links `[Anchor Text](URL)`: Translate ONLY the anchor text into Chinese. NEVER change or translate the target URL or anchor hash.
   - For images `![Alt Text](Path)`: Translate ONLY the alt text into Chinese. NEVER alter image paths or filenames.

5. **Terminology & Chinese Writing Conventions**:
   - Use standard, established Chinese technical terminology (技术社区通用译名); keep proper nouns, brand names, product and tool names in their original English form unless a widely accepted Chinese name exists.
   - For terms without a common Chinese translation, keep the English term, or give the Chinese rendering with the English original in parentheses on first occurrence (e.g., 反向传播（backpropagation）).
   - Use full-width Chinese punctuation（，。、；：？！（）《》）and never insert a space before punctuation.
   - Leave exactly one space between Chinese characters and Latin words or numerals (e.g., 使用 Python 3.11 部署服务).

6. **Completeness & Output Format**:
   - Do not omit, truncate, summarize, or alter any sections.
   - Output ONLY the translated Markdown document directly, maintaining 1:1 structural correspondence with the source.

---

### Input Markdown (English):

<!-- PASTE YOUR SOURCE ENGLISH MARKDOWN CONTENT BELOW -->



<!-- END OF SOURCE MARKDOWN -->

### Output:

<!-- The translated Simplified Chinese Markdown document will be generated here -->
```

---

## Terminology (UNNC / CS / CPU Glossaries)

Many official names are **non-literal brand names** (e.g., 信息安全问卷 → Cybersecurity Quiz), so terminology must come from the canonical glossary CSVs in the repository — never from the model's own literal translation. Two ways to load them:

### Option 1 (preferred): install the skill

If the environment supports agent skills (Claude Code, Cursor, Antigravity, ...), guide the agent to add this skill directly — the glossaries, format-protection rules, and self-review workflow all come along automatically:

```bash
npx skills add CompPsyUnion/translate-skill
```

After installation, no manual prompt is needed at all — just ask, e.g., `请使用 translate-skill 将 README.md 翻译为英文。`

### Option 2 (fallback): read the glossary CSVs from GitHub

If the skill cannot be installed (e.g., a plain LLM chat with no agent runtime), have the agent read the needed CSVs directly from the repository. Agents with web access can fetch these raw URLs themselves; otherwise open a URL in the browser and paste the CSV content into the prompt:

- CPU club (departments, events, recruitment, publicity):
   `https://raw.githubusercontent.com/CompPsyUnion/translate-skill/main/.agents/skills/translate-skill/resources/glossary_cpu.csv`
- General computer science terminology:
   `https://raw.githubusercontent.com/CompPsyUnion/translate-skill/main/.agents/skills/translate-skill/resources/glossary_cs.csv`
- UNNC institutions, degree classifications, and academic affairs:
   `https://raw.githubusercontent.com/CompPsyUnion/translate-skill/main/.agents/skills/translate-skill/resources/glossary_unnc.csv`

Whichever way the glossary arrives, add one instruction line to the prompt: **"Glossary renderings are authoritative and override literal translation."**

> The CSVs are the single source of truth — this document deliberately does not inline a copy of them, so it can never drift out of sync with the repository.

---

## Usage Instructions

1. **Try Installing the Skill First (Preferred)**: If the environment supports agent skills, run `npx skills add CompPsyUnion/translate-skill` and simply ask the agent to translate — glossaries and the full workflow come along automatically. The remaining steps are the no-install fallback.
2. **Pick a Direction**: Choose Template A (Chinese → English) or Template B (English → Simplified Chinese).
3. **Copy**: Copy the entire prompt template of your choice.
4. **Load Terminology (Optional)**: If the document involves UNNC/CS/CPU-specific names, load the glossary CSVs as described in the Terminology section (have the agent fetch the raw GitHub URLs, or paste the CSV content) so official renderings are enforced.
5. **Paste Source**: Paste your source Markdown content directly under the `### Input Markdown (...)` block of that template.
6. **Execute**: Send it to any preferred LLM (Claude, ChatGPT, Gemini, DeepSeek, etc.).
7. **Save Non-Destructively**: Save the generated output to a new file (e.g., `<original_name>_en.md` for Chinese→English, `<original_name>_zh.md` for English→Chinese) to keep the source file intact.
