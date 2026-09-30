#!/usr/bin/env python3
"""
Semantic Vector Consistency Checker for Bilingual Documentation.
Zero external dependencies (pure Python standard library).
Compatible with any OpenAI-compatible Embedding API:
- OpenAI (text-embedding-3-small, text-embedding-3-large)
- Ollama (e.g. http://localhost:11434/v1, nomic-embed-text, bge-m3)
- LocalAI, vLLM, SiliconFlow, DeepSeek, or other compatible endpoints.
"""

import os
import sys
import re
import json
import math
import argparse
import urllib.request
import urllib.error
from typing import List, Tuple, Dict, Any


def clean_markdown_for_embedding(text: str) -> str:
    """Strip code blocks, inline code, URLs, and image links, keeping natural language."""
    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    # Keep text inside inline code, remove backticks: `code` -> code
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # Convert [text](url) to text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove image links ![alt](url)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # Clean excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_paragraphs(filepath: str) -> List[Tuple[int, str]]:
    """
    Parse a Markdown file and extract meaningful semantic paragraphs with their line numbers.
    Skips code blocks and empty lines.
    """
    paragraphs = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_chunk = []
    start_line = 1
    in_code_block = False

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Toggle fenced code blocks
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        if stripped:
            if not current_chunk:
                start_line = idx
            current_chunk.append(stripped)
        else:
            if current_chunk:
                raw_text = " ".join(current_chunk)
                cleaned = clean_markdown_for_embedding(raw_text)
                if cleaned and len(cleaned) > 5:
                    paragraphs.append((start_line, cleaned))
                current_chunk = []

    if current_chunk:
        raw_text = " ".join(current_chunk)
        cleaned = clean_markdown_for_embedding(raw_text)
        if cleaned and len(cleaned) > 5:
            paragraphs.append((start_line, cleaned))

    return paragraphs


def fetch_embeddings(
    texts: List[str],
    api_key: str,
    api_base: str,
    model: str
) -> List[List[float]]:
    """Fetch vector embeddings via OpenAI-compatible REST API using urllib."""
    url = f"{api_base.rstrip('/')}/embeddings"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}" if api_key else ""
    }

    # Remove empty Authorization header if not provided (useful for local Ollama)
    if not api_key:
        del headers["Authorization"]

    payload = {
        "model": model,
        "input": texts
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            data = res_data.get("data", [])
            # Sort by index to maintain original order
            data_sorted = sorted(data, key=lambda x: x.get("index", 0))
            return [item["embedding"] for item in data_sorted]
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        print(f"[Error] API HTTP {e.code}: {err_body}", file=sys.stderr)
        raise
    except urllib.error.URLError as e:
        print(f"[Error] Failed to connect to {url}: {e.reason}", file=sys.stderr)
        raise


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Compute cosine similarity between two numeric vectors in pure Python."""
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def run_check(
    source_file: str,
    target_file: str,
    threshold: float,
    api_key: str,
    api_base: str,
    model: str
) -> bool:
    print(f"Reading source file: {source_file}")
    src_paras = extract_paragraphs(source_file)
    print(f"Reading target file: {target_file}")
    tgt_paras = extract_paragraphs(target_file)

    print(f"Extracted {len(src_paras)} source paragraphs, {len(tgt_paras)} target paragraphs.")

    if not src_paras or not tgt_paras:
        print("[Error] No valid paragraphs extracted from one or both files.")
        return False

    if len(src_paras) != len(tgt_paras):
        print(f"[Warning] Paragraph count mismatch: Source has {len(src_paras)}, Target has {len(tgt_paras)}.")
        print("Comparing aligned prefix pairs up to the shorter count...\n")

    compare_count = min(len(src_paras), len(tgt_paras))

    # Prepare batch input
    batch_src = [p[1] for p in src_paras[:compare_count]]
    batch_tgt = [p[1] for p in tgt_paras[:compare_count]]

    print(f"Requesting embeddings via API ({api_base}, model: {model})...")
    # Fetch in two calls or combined
    all_texts = batch_src + batch_tgt
    all_embeddings = fetch_embeddings(all_texts, api_key, api_base, model)

    src_embeddings = all_embeddings[:compare_count]
    tgt_embeddings = all_embeddings[compare_count:]

    failures: List[Dict[str, Any]] = []
    scores: List[float] = []

    print("\n" + "=" * 70)
    print(f"{'Status':<8} | {'Para':<6} | {'SrcLine':<8} | {'TgtLine':<8} | {'Score':<8}")
    print("-" * 70)

    for i in range(compare_count):
        score = cosine_similarity(src_embeddings[i], tgt_embeddings[i])
        scores.append(score)
        src_line = src_paras[i][0]
        tgt_line = tgt_paras[i][0]

        status = "PASS" if score >= threshold else "FAIL"
        print(f"{status:<8} | #{i+1:<5} | L{src_line:<7} | L{tgt_line:<7} | {score:.4f}")

        if score < threshold:
            failures.append({
                "index": i + 1,
                "src_line": src_line,
                "tgt_line": tgt_line,
                "src_text": src_paras[i][1],
                "tgt_text": tgt_paras[i][1],
                "score": score
            })

    print("=" * 70)
    avg_score = sum(scores) / len(scores) if scores else 0.0
    print(f"Average Similarity Score: {avg_score:.4f} (Threshold: {threshold:.4f})")

    if failures:
        print(f"\n[ALERT] {len(failures)} paragraph(s) failed semantic consistency check:\n")
        for f in failures:
            print(f"--- Paragraph #{f['index']} (Score: {f['score']:.4f}, Src Line {f['src_line']}) ---")
            print(f"  [Original]:   {f['src_text']}")
            print(f"  [Translated]: {f['tgt_text']}\n")
        return False

    print("\nAll paragraphs passed semantic verification successfully!")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Verify semantic similarity between original and translated markdown files using an OpenAI-compatible Embedding API."
    )
    parser.add_argument("source", help="Path to original (source) Markdown file")
    parser.add_argument("target", help="Path to translated (target) Markdown file")
    parser.add_argument(
        "--threshold",
        type=float,
        default=float(os.environ.get("EMBEDDING_THRESHOLD", "0.75")),
        help="Similarity threshold between 0.0 and 1.0 (default: 0.75, or via EMBEDDING_THRESHOLD env)"
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("EMBEDDING_API_KEY") or os.environ.get("OPENAI_API_KEY", ""),
        help="API Key (default: EMBEDDING_API_KEY or OPENAI_API_KEY env)"
    )
    parser.add_argument(
        "--api-base",
        default=os.environ.get("EMBEDDING_API_BASE") or os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1"),
        help="Base URL for the Embedding API (default: https://api.openai.com/v1, or via EMBEDDING_API_BASE / OPENAI_API_BASE env)"
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small"),
        help="Embedding model identifier (default: text-embedding-3-small, or via EMBEDDING_MODEL env)"
    )

    args = parser.parse_args()

    if not os.path.exists(args.source):
        print(f"[Error] Source file not found: {args.source}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.target):
        print(f"[Error] Target file not found: {args.target}", file=sys.stderr)
        sys.exit(1)

    try:
        success = run_check(
            source_file=args.source,
            target_file=args.target,
            threshold=args.threshold,
            api_key=args.api_key,
            api_base=args.api_base,
            model=args.model
        )
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"[Error] Execution failed: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
