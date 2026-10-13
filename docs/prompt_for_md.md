# Markdown Document Translation Prompt (Direct Copy & Paste)

This prompt is designed for technical translation of Markdown documents from Chinese to natural, fluent English while strictly preserving Markdown syntax, code blocks, tables, and document layout.

You can directly copy and paste the prompt template below into any LLM (e.g., ChatGPT, Claude, Gemini, DeepSeek, Cursor) to translate your `.md` files without installing or configuring agent skills in your project root.

---

## Translation Prompt Template

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

## 💡 Usage Instructions

1. **Copy**: Copy the prompt template above.
2. **Paste Source**: Paste your source Chinese Markdown content directly under the `### Input Markdown (Chinese):` block.
3. **Execute**: Send it to any preferred LLM (Claude, ChatGPT, Gemini, DeepSeek, etc.).
4. **Save Non-Destructively**: Save the generated output to a new file (e.g., `<original_name>_en.md`) to keep the source file intact.
