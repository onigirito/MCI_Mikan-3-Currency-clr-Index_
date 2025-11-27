# Mikan 3-Currency clr Index (MCI)

**Web:** https://onigirito.github.io/MCI_Mikan-3-Currency-clr-Index_/

## 📄 論文 / Paper

**SSRN:** [https://ssrn.com/abstract=XXXXX](https://ssrn.com/abstract=XXXXX) *(Update with your SSRN link)*

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

## 📊 データファイル

### 年次データ（公式）
- **[annual_mci_2005_2024.csv](dataset/annual_mci_2005_2024.csv)** - 2005-2024年の確定値（IMF WEO）

### 月次データ（2022-2025）
- **[monthly_mci_fixed_ppp_2022_2025.csv](dataset/monthly_mci_fixed_ppp_2022_2025.csv)** - 月次MCI分析データ（2022-01〜2025-11、47ヶ月）
  - PPP基準、MCI座標、月次変動率を含む
- **[mci_monthly_recent.csv](dataset/mci_monthly_recent.csv)** - 月次MCI生データ
- **[monthly_exchange_rates_2022_2025.csv](dataset/monthly_exchange_rates_2022_2025.csv)** - 月次為替レート（元データ）
- **[monthly_rates_template.csv](dataset/monthly_rates_template.csv)** - データ入力用テンプレート

## 📖 ドキュメント / Documentation

- [全文（日本語）](docs/FULL_PAPER_CORRECTED.md) - 完全版論文 / Full paper (Japanese)
- [Full Paper (English)](docs/FULL_PAPER_EN.md) - 完全版論文（英語）/ Full paper (English)
- [ツール使用方法](tools/README.md) - 詳細な使い方 / Tool usage details
- [データ仕様](dataset/README.md) - データセット詳細 / Dataset specifications

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
for Multi-Currency Valuation. Available at SSRN: https://ssrn.com/abstract=XXXXX
```
