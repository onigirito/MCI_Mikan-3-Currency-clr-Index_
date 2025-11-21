# Mikan 3-Currency clr Index

PPP（購買力平価）を基準とした3通貨（USD・JPY・TRY）の構造的評価指標。

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

## 📖 ドキュメント

- [理論枠組み](docs/CHAPTER2_CORRECTED.md) - MCI座標の数理定義
- [ツール使用方法](tools/README.md) - 詳細な使い方
- [データ仕様](dataset/README.md) - データセット詳細

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
