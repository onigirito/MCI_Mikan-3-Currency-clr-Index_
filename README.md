# Mikan 3-Currency clr Index (MCI)

**Web:** https://onigirito.github.io/MCI_Mikan-3-Currency-clr-Index_/

## 📄 論文 / Paper

**SSRN:** [https://ssrn.com/abstract=5872622](https://ssrn.com/abstract=5872622)

| 日本語 | English |
|--------|---------|
| [全文（日本語）](docs/FULL_PAPER_CORRECTED.md) | [Full Paper (English)](docs/FULL_PAPER_EN.md) |

---

任意の3通貨に適用可能なPPP（購買力平価）ベースの構造的評価指標（本論文ではUSD・JPY・TRYを分析）。

A PPP (Purchasing Power Parity) based structural evaluation framework applicable to any three currencies (this paper analyzes USD, JPY, and TRY).

## 概要 / Overview

MCIは、任意の3通貨間のPPP乖離を**ゼロサム制約**のもとで定量化する汎用的フレームワークです（本実装ではUSD・JPY・TRYを使用）。

MCI is a general framework that quantifies PPP deviations among any three currencies under a **zero-sum constraint** (this implementation uses USD, JPY, and TRY).

各通貨の相対価値 m[i] は以下の性質を持ちます：
- **m[i] < 0**: その通貨がバスケット内で割安
- **m[i] > 0**: その通貨がバスケット内で割高
- **常に m[USD] + m[JPY] + m[TRY] = 0**（ゼロサム保存則）

The relative value m[i] of each currency has the following properties:
- **m[i] < 0**: The currency is undervalued within the basket
- **m[i] > 0**: The currency is overvalued within the basket
- **Always m[USD] + m[JPY] + m[TRY] = 0** (Zero-sum conservation law)

この設計により、一つの通貨の過大評価は必ず他通貨の過小評価と釣り合い、選択した3通貨間の力学的バランスを可視化できます。

This design ensures that overvaluation of one currency always balances with undervaluation of others, visualizing the dynamic equilibrium among the selected three currencies.

> 理論の原典は著者の小説「果物世界」に収録されています → [ミカン定理：原典](docs/ORIGINAL_MIKAN_THEORY.md)

---

## 📊 データファイル / Data Files

### 年次データ（2005-2024）/ Annual Data (2005-2024)

- **[`annual_mci_2005_2024.csv`](dataset/annual_mci_2005_2024.csv)** - 20年年次データ / 20-year annual data
  - 期間：2005-2024年（20年） / Period: 2005-2024 (20 years)
  - 用途：長期トレンド分析、構造転換点の検出 / Use: Long-term trend analysis, structural turning point detection
  - 特徴：3つの構造転換点（2011年、2018年、2022年） / Features: 3 structural turning points (2011, 2018, 2022)

### 月次データ（2022-2025）/ Monthly Data (2022-2025)

- **[`monthly_mci_fixed_ppp_2022_2025.csv`](dataset/monthly_mci_fixed_ppp_2022_2025.csv)** - 固定PPP版（比較検証用） / Fixed PPP version (for comparison)
  - 期間：2022年1月～2025年11月（47カ月） / Period: Jan 2022 to Nov 2025 (47 months)
  - 特徴：年次PPP固定、月次為替レート / Features: Annual PPP fixed, monthly exchange rates
  - 用途：論文第8章「固定PPPとの比較」 / Use: Chapter 8 "Comparison with Fixed PPP"

- **[`monthly_mci_complete_2022_2025.csv`](dataset/monthly_mci_complete_2022_2025.csv)** ⭐ **完全版（推奨）/ Complete version (Recommended)**
  - 期間：2022年1月～2025年11月（47カ月、25列） / Period: Jan 2022 to Nov 2025 (47 months, 25 columns)
  - 特徴：**2022年PPP線形補間済み**（v2.0修正版） / Features: **2022 PPP linearly interpolated** (v2.0 corrected)
  - 含む：m座標、3カ月移動平均、予測値、誤差 / Includes: m-coordinates, 3-month rolling averages, predictions, errors
  - バックテスト：2022-05～2025-11（43カ月分の予測結果） / Backtest: May 2022 to Nov 2025 (43 months of predictions)
  - **構造安定期（2023-08以降、28カ月）** / **Stable period (from Aug 2023, 28 months)**
    - MAE（平均絶対誤差）：2.34% / MAE (Mean Absolute Error): 2.34%
    - RMSE（二乗平均平方根誤差）：3.47% / RMSE (Root Mean Square Error): 3.47%
  - 品質：ゼロサム制約充足（偏差 < 10^-15） / Quality: Zero-sum constraint satisfied (deviation < 10^-15)

**📖 統合ドキュメント：** [**dataset/README.md**](dataset/README.md) - データ取得からバックテストまで全て記載 / Comprehensive documentation from data acquisition to backtesting

---

## 🔬 バックテスト / Backtest

**予測精度（全期間43カ月）** / **Prediction Accuracy (Full period 43 months)**:
- MAE: 2.66%, RMSE: 3.86%
- 構造安定期（28カ月）/ Stable period (28 months): MAE 2.34%, RMSE 3.47%

**詳細 / Details**: [定量的評価 / Quantitative Evaluation](dataset/BACKTEST_ANALYSIS.md) ([English](dataset/BACKTEST_ANALYSIS_EN.md))

---

## 📖 ドキュメント / Documentation

### 論文 / Papers

- **[全文（日本語）](docs/FULL_PAPER_CORRECTED.md)** - 完全版論文 / Full paper (Japanese)
- **[Full Paper (English)](docs/FULL_PAPER_EN.md)** - 完全版論文 / Full paper (English)
- **[修正サマリー](docs/CORRECTIONS_SUMMARY.md)** - v2.0での修正内容 / Corrections in v2.0
- **[参考文献](docs/REFERENCES.md)** - 理論的背景 / Theoretical background

### データ / Data

- **[データセット統合ドキュメント](dataset/README.md)** - データ取得、CSV列の説明、バックテスト（包括的） / Integrated documentation: data acquisition, CSV columns, backtesting (comprehensive)

### 理論 / Theory

- **[ミカン定理：原典](docs/ORIGINAL_MIKAN_THEORY.md)** - 小説「果物世界」からの理論抽出 / Theory extracted from novel "Fruit World"
- **[第8章（英語）](docs/CHAPTER8_EN.md)** - PPP補間の比較検証 / Comparison of PPP interpolation methods

---

## 🚀 クイックスタート / Quick Start

### 1. データを見る / View Data

```bash
# 20年間のトレンド / 20-year trend
head dataset/annual_mci_2005_2024.csv

# 最新の月次データ / Latest monthly data
tail dataset/monthly_mci_complete_2022_2025.csv
```

### 2. バックテスト / Run Backtest

詳細は [dataset/README.md](dataset/README.md) と [BACKTEST_ANALYSIS.md](dataset/BACKTEST_ANALYSIS.md) を参照 / See [dataset/README.md](dataset/README.md) and [BACKTEST_ANALYSIS.md](dataset/BACKTEST_ANALYSIS.md) for details

---

## 💼 Commercial Use Notice

This project is **MIT licensed** - you can use it freely for any purpose, including commercial use.

However, for **commercial use** (business products, paid services, trading platforms, financial tools, etc.), I'd appreciate if you:

1. **Let me know** - Open an [issue](https://github.com/onigirito/MCI_Mikan-3-Currency-clr-Index_/issues) or send me an email
2. **Consider sponsoring** - Support continued development via [GitHub Sponsors](https://github.com/sponsors/onigirito)
3. **Give proper attribution** - Cite the SSRN paper or link to this repository

**Not legally required, but it supports continued research and development.** 🙏

If you're building something cool with MCI, I'd love to hear about it!

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

**Citation:**
```
Honda, Y. (2025). Mikan 3-Currency clr Index: A Compositional Data Analysis Framework
for Multi-Currency Valuation. Available at SSRN: https://ssrn.com/abstract=5872622
```

---

## 🔗 Links

- **Web:** https://onigirito.github.io/MCI_Mikan-3-Currency-clr-Index_/
- **SSRN:** https://ssrn.com/abstract=5872622
- **Dataset Documentation:** [dataset/README.md](dataset/README.md)
- **Issues:** [GitHub Issues](https://github.com/onigirito/MCI_Mikan-3-Currency-clr-Index_/issues)

---

**Version:** 2.1 (2026-01-08) - 2022 m-coordinates corrected, prediction accuracy properly evaluated
