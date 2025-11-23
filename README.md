# Mikan 3-Currency clr Index (MCI)

## 📄 論文 / Paper

| 日本語 | English |
|--------|---------|
| [全文（日本語）](docs/FULL_PAPER_CORRECTED.md) | [Full Paper (English)](docs/FULL_PAPER_EN.md) |

---

PPP（購買力平価）を基準とした3通貨（USD・JPY・TRY）の構造的評価指標。

A structural evaluation index for three currencies (USD, JPY, TRY) based on PPP (Purchasing Power Parity).

## 概要 / Overview

MCIは、3通貨間のPPP乖離を**ゼロサム制約**のもとで定量化する指標です。

MCI quantifies PPP deviations among three currencies under a **zero-sum constraint**.

各通貨の相対価値 m[i] は以下の性質を持ちます：
- **m[i] < 0**: その通貨がバスケット内で割安
- **m[i] > 0**: その通貨がバスケット内で割高
- **常に m[USD] + m[JPY] + m[TRY] = 0**（ゼロサム保存則）

The relative value m[i] of each currency has the following properties:
- **m[i] < 0**: The currency is undervalued within the basket
- **m[i] > 0**: The currency is overvalued within the basket
- **Always m[USD] + m[JPY] + m[TRY] = 0** (Zero-sum conservation law)

この設計により、一つの通貨の過大評価は必ず他通貨の過小評価と釣り合い、3通貨間の力学的バランスを可視化できます。

This design ensures that overvaluation of one currency always balances with undervaluation of others, visualizing the dynamic equilibrium among the three currencies.

> 理論の原典は著者の小説「果物世界」に収録されています → [ミカン定理：原典](docs/ORIGINAL_MIKAN_THEORY.md)

## 📊 データファイル

### 年次データ（公式）
- **[mikan_3currency_clr_index_ppp_data.csv](dataset/mikan_3currency_clr_index_ppp_data.csv)** - 2005-2024年の確定値（World Bank WDI）

### 月次データ（2022-2025）
- **[monthly_mci_analysis.csv](monthly_mci_analysis.csv)** - 月次MCI分析データ（2022-01〜2025-11、47ヶ月）
  - PPP基準、MCI座標、月次変動率を含む
- **[mci_monthly_recent.csv](dataset/mci_monthly_recent.csv)** - 月次MCI生データ
- **[monthly_rates_data.csv](monthly_rates_data.csv)** - 月次為替レート（元データ）

## 🔧 ツール

### リアルタイム計算
```bash
python3 tools/calculate_mci_from_rates.py --usdjpy 157 --usdtry 42.3 --ppp-year 2024
```

### 月次データ更新
```bash
# 1. 月次レートCSVを更新
# 2. MCIを再計算
python3 tools/create_monthly_mci.py monthly_rates_data.csv

# 3. 分析CSVを生成
python3 export_monthly_analysis.py
```

## 📖 ドキュメント / Documentation

- [理論枠組み](docs/CHAPTER2_CORRECTED.md) - MCI座標の数理定義 / Mathematical definition of MCI coordinates
- [月次分析](docs/CHAPTER8_MONTHLY_ANALYSIS.md) - 月次データとPPP補間 / Monthly data and PPP interpolation
- [ツール使用方法](tools/README.md) - 詳細な使い方 / Tool usage details
- [データ仕様](dataset/README.md) - データセット詳細 / Dataset specifications

## 🎯 現在の状況（2025-11）

```
PPP基準: 16.63（2025年推定）
現在位置: m[TRY] = -0.453
価格: TRY/JPY = 3.66
判定: 正常域
```

## 📝 分析レポート

- [客観的評価](objective_evaluation.py) - MCIの有効性検証
- [月次分析](analyze_monthly_mci.py) - 月次変動の詳細分析
