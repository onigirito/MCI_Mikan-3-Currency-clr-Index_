#!/usr/bin/env python3
"""
Regenerate FULL_PAPER_CORRECTED.md from individual corrected chapter files.
Updated to use 7 chapters (after deletions of old chapters 6 and 8).
"""

import os

# Define the structure
TITLE = """# Mikan 3-Currency clr Index に基づく購買力平価分析（修正版）

**副題**：USD・JPY・TRY三通貨のclr変換による相対評価指標の構築と時系列分析

**著者**：[著者名]

**所属**：[所属機関名]

**作成日**：2025年

---

## 概要

本稿では、米ドル（USD）、日本円（JPY）、トルコリラ（TRY）の3通貨を対象に、購買力平価（PPP）理論に基づく新たな相対評価指標「Mikan 3-Currency clr Index」を提案する。本指標は、組成データ分析（Compositional Data Analysis; CoDA）における中心化対数比変換（centered log-ratio; clr）の考え方を応用し、PPP乖離率を直交化した形で表現することで、各通貨の「割高・割安」度合いをバランスよく定量化する。2005年から2024年までの20年間のデータを用いた実証分析により、本指標が各通貨の構造的な動きを鮮明に捉えることを示す。また、本手法は単純な二国間PPP比較では得られない多通貨間のバランス情報を提供し、政策分析や投資判断への応用可能性を有することを論じる。

**キーワード**：購買力平価、為替相場、組成データ分析、clr変換、通貨評価、USD/JPY/TRY

---
"""

TOC = """
## 目次

1. [第1章 はじめに](#第1章-はじめに)
2. [第2章 理論的枠組み](#第2章-理論的枠組み)
3. [第3章 データと方法](#第3章-データと方法)
4. [第4章 実証分析結果：時系列の解釈](#第4章-実証分析結果時系列の解釈)
5. [第5章 単純PPP分析との比較](#第5章-単純ppp分析との比較)
6. [第6章 レジーム転換と通貨構造の再配置](#第6章-レジーム転換と通貨構造の再配置)
7. [第7章 運用指針](#第7章-運用指針)
8. [参照文献](#参照文献)

---
"""

def read_chapter(chapter_num):
    """Read a chapter file and return its content."""
    filepath = f"CHAPTER{chapter_num}_CORRECTED.md"
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found")
        return ""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    return content

def main():
    """Generate the full paper."""
    print("Regenerating FULL_PAPER_CORRECTED.md...")

    # Start with title and TOC
    full_paper = TITLE + TOC

    # Add all chapters (1-7, after deletions)
    for chapter_num in range(1, 8):
        print(f"Adding Chapter {chapter_num}...")
        chapter_content = read_chapter(chapter_num)
        if chapter_content:
            full_paper += "\n" + chapter_content + "\n"
            full_paper += "\n---\n\n"

    # Add references
    print("Adding references...")
    if os.path.exists("REFERENCES.md"):
        with open("REFERENCES.md", 'r', encoding='utf-8') as f:
            references = f.read()
        full_paper += references
    else:
        print("Warning: REFERENCES.md not found")

    # Write the full paper
    with open("FULL_PAPER_CORRECTED.md", 'w', encoding='utf-8') as f:
        f.write(full_paper)

    print(f"✓ FULL_PAPER_CORRECTED.md generated successfully!")
    print(f"  Total length: {len(full_paper)} characters")
    print(f"  Total lines: {full_paper.count(chr(10))} lines")

if __name__ == "__main__":
    main()
