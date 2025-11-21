# MCI計算ツール

## ツール一覧

### 1. calculate_mci_from_rates.py
リアルタイムの為替レートからMCI座標を計算

**使い方:**
```bash
python3 tools/calculate_mci_from_rates.py --usdjpy 157 --usdtry 42.3 --ppp-year 2024
```

**オプション:**
- `--usdjpy`: USD/JPY レート（必須）
- `--usdtry`: USD/TRY レート（必須）
- `--ppp-year`: PPP基準年（デフォルト: 2024）
- `--compare`: 比較対象年（データセットから）

**出力例:**
```
MCI座標:
  m[USD] = +0.578855
  m[JPY] = +0.057357
  m[TRY] = -0.636212
```

### 2. create_monthly_mci.py
直近3年の月次MCIデータを作成

**ステップ1: テンプレート作成**
```bash
python3 tools/create_monthly_mci.py --template
```
→ `monthly_rates_template.csv` が生成される

**ステップ2: データ入力**
CSVファイルに月次平均レートを入力：
```csv
date,S_USDJPY,S_USDTRY
2022-01,115.10,13.42
2022-02,115.54,14.01
...
```

**ステップ3: MCI計算**
```bash
python3 tools/create_monthly_mci.py monthly_rates_template.csv
```
→ `dataset/mci_monthly_recent.csv` が生成される

## PPP設定

各年のPPP基準値：

| 年 | PPP_JPY | PPP_TRY | 状態 |
|----|---------|---------|------|
| 2022 | 92.50 | 4.975 | 確定 |
| 2023 | 92.84 | 8.074 | 確定 |
| 2024 | 93.20 | 12.55 | 確定 |
| 2025 | 93.20 | 18.83 | **推定** |

**2025年PPP推定方法:**
- JPY: 据え置き（直近3年ほぼ横ばい）
- TRY: 2024年値 × 1.50（年50%インフレ想定）

## 月次データの活用

月次MCIデータを使うことで：
- 年次データでは見えない短期変動を捕捉
- 月次の深度判定が可能
- ストップライン接近の早期警戒

**注意点:**
- PPPは年次固定のため、年内のPPP変動は反映されない
- 高インフレ国（TRY）では年末に近づくほどバイアスが大きくなる
- あくまで「構造的な位置」の推定であり、短期的な価格変動とは別

## データファイル構成

```
dataset/
  ├── mikan_3currency_clr_index_ppp_data.csv  # 年次公式データ（2005-2024）
  └── mci_monthly_recent.csv                   # 月次データ（2022-2025、推定含む）

tools/
  ├── calculate_mci_from_rates.py              # リアルタイム計算
  ├── create_monthly_mci.py                    # 月次データ作成
  └── README.md                                # このファイル
```

## ユースケース

### 短期トレーダー向け
```bash
# 毎日の市場クローズ時にチェック
python3 tools/calculate_mci_from_rates.py --usdjpy <今日の終値> --usdtry <今日の終値> --compare 2024
```

### 中期投資家向け
```bash
# 月次でポートフォリオ評価
# 月次レートCSVを更新 → create_monthly_mci.py で月次トレンド分析
```

### リスク管理者向け
```bash
# ストレステスト: 深度1ラインまでのマージンを確認
python3 tools/calculate_mci_from_rates.py --usdjpy 157 --usdtry 45.88 --compare 2024
# → 深度1到達時のレート水準を確認
```
