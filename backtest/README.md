# MCI価格予想バックテストツール / MCI Price Prediction Backtest Tools

第8章の価格予想原理に基づく月次バックテストツール
Monthly backtest tools based on Chapter 8 price prediction methodology

---

## 📋 目次 / Table of Contents

**日本語 (Japanese)**
1. [概要](#概要-overview)
2. [予想手法](#予想手法-methodology)
3. [ツール使用方法](#ツール使用方法-usage)
4. [バックテスト結果](#バックテスト結果-results)
5. [データソース](#データソース-data-source)

**English**
1. [Overview](#概要-overview)
2. [Methodology](#予想手法-methodology)
3. [Usage](#ツール使用方法-usage)
4. [Results](#バックテスト結果-results)
5. [Data Source](#データソース-data-source)

---

## 概要 / Overview

### 日本語

このディレクトリには、MCI（Mikan Currency Index）モデルを使った為替レート月次予想のバックテストツールが含まれています。

**📊 詳細な定量的評価については以下を参照:**
- **[BACKTEST_ANALYSIS.md](BACKTEST_ANALYSIS.md)** - 包括的なバックテスト結果の定量的分析（日本語）

**対象通貨ペア:**
- **USD/JPY**: 米ドル/日本円
- **USD/TRY**: 米ドル/トルコリラ
- **TRY/JPY**: トルコリラ/日本円

**対象期間:**
- **データ期間**: 2022-01 〜 2025-11（47ヶ月）
- **バックテスト期間**: 2022-03 〜 2025-11（45ヶ月の予想）

### English

This directory contains backtest tools for monthly exchange rate predictions using the MCI (Mikan Currency Index) model.

**📊 For detailed quantitative evaluation, see:**
- **[BACKTEST_ANALYSIS_EN.md](BACKTEST_ANALYSIS_EN.md)** - Comprehensive quantitative analysis of backtest results (English)

**Target Currency Pairs:**
- **USD/JPY**: US Dollar / Japanese Yen
- **USD/TRY**: US Dollar / Turkish Lira
- **TRY/JPY**: Turkish Lira / Japanese Yen

**Target Period:**
- **Data Period**: 2022-01 to 2025-11 (47 months)
- **Backtest Period**: 2022-03 to 2025-11 (45 months of predictions)

---

## 予想手法 / Methodology

### 日本語

#### 基本原理

**過去3カ月のm座標変動の平均**を使って翌月の為替レートを予想します。

#### 予想プロセス

N+1月を予想する場合：

1. **変動量の計算**
   - N-2月、N-1月、N月の各月について、前月からのm座標変動（Δm）を計算

2. **3カ月平均の算出**
   ```
   avg_Δm = (Δm_{N-2} + Δm_{N-1} + Δm_{N}) / 3
   ```

3. **予想m座標の計算**
   ```
   m_{N+1}^{pred} = m_N + avg_Δm
   ```

4. **予想為替レートの計算**
   ```
   S_{A/B} = PPP_{A/B} × exp(m[A] - m[B])
   ```

#### 特徴

- ✓ **シンプル**: 単一シナリオで明確
- ✓ **適応的**: 各月の実際のトレンドに追随
- ✓ **ニュートラル**: 構造的バイアスが少ない
- ✓ **実務的**: 直近の市場動向を反映

### English

#### Basic Principle

Predicts next month's exchange rates using **the average of m-coordinate changes over the past 3 months**.

#### Prediction Process

To predict month N+1:

1. **Calculate Changes**
   - Calculate m-coordinate change (Δm) from previous month for months N-2, N-1, and N

2. **Calculate 3-Month Average**
   ```
   avg_Δm = (Δm_{N-2} + Δm_{N-1} + Δm_{N}) / 3
   ```

3. **Calculate Predicted m-Coordinates**
   ```
   m_{N+1}^{pred} = m_N + avg_Δm
   ```

4. **Calculate Predicted Exchange Rates**
   ```
   S_{A/B} = PPP_{A/B} × exp(m[A] - m[B])
   ```

#### Features

- ✓ **Simple**: Clear single-scenario approach
- ✓ **Adaptive**: Follows actual monthly trends
- ✓ **Neutral**: Minimal structural bias
- ✓ **Practical**: Reflects recent market conditions

---

## ツール使用方法 / Usage

### 日本語

#### 1. バックテスト実行

**`backtest_with_rolling_avg.py`** - 3カ月平均を使った月次予想バックテスト

**単一月のテスト:**
```bash
python backtest_with_rolling_avg.py --base-month 2022-03
```

**出力例:**
```
=== Backtest: 2022-03 → 2022-04 ===

3-month average deltas used:
  USD: +0.017735
  JPY: +0.002217
  TRY: -0.019952

Predictions vs Actual:
  USDJPY: 120.31 vs 126.05 (error: -4.55%)
  USDTRY: 15.16 vs 14.71 (error: +3.06%)
  TRYJPY: 7.94 vs 8.57 (error: -7.39%)
```

**全期間の包括的バックテスト:**
```bash
python backtest_with_rolling_avg.py --comprehensive
```

**カスタム出力ファイル:**
```bash
python backtest_with_rolling_avg.py --comprehensive --output my_results.csv
```

**出力ファイル:**
- デフォルト: `backtest_rolling_avg_results.csv`
- 45ヶ月分の予想結果（2022-03 〜 2025-11）

#### 2. 結果分析

**`analyze_rolling_avg_results.py`** - バックテスト結果の詳細分析

**全期間の分析:**
```bash
python analyze_rolling_avg_results.py
```

**安定期のみ分析（2023-08以降）:**
```bash
python analyze_rolling_avg_results.py 2023-08
```

**出力内容:**
- 精度指標（平均誤差、MAE、RMSE）
- 誤差分布（0-1%, 1-2%, 2-3%, ...）
- 最も外れた予想 Top 5
- バイアス評価
- 総合評価

### English

#### 1. Running Backtest

**`backtest_with_rolling_avg.py`** - Monthly prediction backtest using 3-month average

**Single month test:**
```bash
python backtest_with_rolling_avg.py --base-month 2022-03
```

**Sample output:**
```
=== Backtest: 2022-03 → 2022-04 ===

3-month average deltas used:
  USD: +0.017735
  JPY: +0.002217
  TRY: -0.019952

Predictions vs Actual:
  USDJPY: 120.31 vs 126.05 (error: -4.55%)
  USDTRY: 15.16 vs 14.71 (error: +3.06%)
  TRYJPY: 7.94 vs 8.57 (error: -7.39%)
```

**Comprehensive backtest for full period:**
```bash
python backtest_with_rolling_avg.py --comprehensive
```

**Custom output file:**
```bash
python backtest_with_rolling_avg.py --comprehensive --output my_results.csv
```

**Output file:**
- Default: `backtest_rolling_avg_results.csv`
- 45 months of predictions (2022-03 to 2025-11)

#### 2. Results Analysis

**`analyze_rolling_avg_results.py`** - Detailed analysis of backtest results

**Full period analysis:**
```bash
python analyze_rolling_avg_results.py
```

**Stable period only (from 2023-08):**
```bash
python analyze_rolling_avg_results.py 2023-08
```

**Output includes:**
- Accuracy metrics (mean error, MAE, RMSE)
- Error distribution (0-1%, 1-2%, 2-3%, ...)
- Top 5 worst predictions
- Bias evaluation
- Overall assessment

---

## バックテスト結果 / Results

### 日本語

#### 全期間（2022-03〜2025-11、45ヶ月）

| 通貨ペア | 件数 | 平均誤差 | 平均絶対誤差 | RMSE | バイアス |
|---------|------|----------|-------------|------|---------|
| USDJPY  | 45   | +0.00%   | **2.42%**   | 3.32%| ニュートラル |
| USDTRY  | 45   | +0.17%   | **2.23%**   | 3.65%| ニュートラル |
| TRYJPY  | 45   | -0.03%   | **3.84%**   | 4.97%| ニュートラル |

**総合評価:**
- **平均MAE: 2.83%**
- **平均RMSE: 3.98%**
- **評価: [GOOD] 良好な精度**

#### 安定期（2023-08〜2025-11、28ヶ月）

| 通貨ペア | 件数 | 平均誤差 | 平均絶対誤差 | RMSE | バイアス |
|---------|------|----------|-------------|------|---------|
| USDJPY  | 28   | +0.03%   | **2.19%**   | 3.23%| ニュートラル |
| USDTRY  | 28   | +0.68%   | **1.44%**   | 2.72%| やや高め |
| TRYJPY  | 28   | -0.57%   | **3.38%**   | 4.46%| やや低め |

**総合評価:**
- **平均MAE: 2.34%**
- **平均RMSE: 3.47%**
- **評価: [GOOD] 良好な精度**

#### 主要な発見

**精度特性:**
- 全期間平均誤差: 2.83%（1か月先予想として良好）
- バイアス: ほぼゼロ（全て±0.2%以内）
- 安定期では精度向上（平均誤差 2.34%）
- USDTRYで特に高精度（MAE 1.44%）

**誤差分布（安定期・USDTRY）:**
- 約9割が誤差2%以内
- 64.3%が誤差1%以内

**大きな外れ値:**
- 政治イベント（トルコ大統領選挙 2023-06）
- 大きな市場変動（2024-08）で外れやすい

### English

#### Full Period (2022-03 to 2025-11, 45 months)

| Pair    | Count | Mean Error | MAE        | RMSE | Bias    |
|---------|-------|-----------|------------|------|---------|
| USDJPY  | 45    | +0.00%    | **2.42%**  | 3.32%| Neutral |
| USDTRY  | 45    | +0.17%    | **2.23%**  | 3.65%| Neutral |
| TRYJPY  | 45    | -0.03%    | **3.84%**  | 4.97%| Neutral |

**Overall Assessment:**
- **Average MAE: 2.83%**
- **Average RMSE: 3.98%**
- **Rating: [GOOD] Good accuracy**

#### Stable Period (2023-08 to 2025-11, 28 months)

| Pair    | Count | Mean Error | MAE        | RMSE | Bias         |
|---------|-------|-----------|------------|------|--------------|
| USDJPY  | 28    | +0.03%    | **2.19%**  | 3.23%| Neutral      |
| USDTRY  | 28    | +0.68%    | **1.44%**  | 2.72%| Slightly high|
| TRYJPY  | 28    | -0.57%    | **3.38%**  | 4.46%| Slightly low |

**Overall Assessment:**
- **Average MAE: 2.34%**
- **Average RMSE: 3.47%**
- **Rating: [GOOD] Good accuracy**

#### Key Findings

**Accuracy Characteristics:**
- Full period average error: 2.83% (good for 1-month-ahead prediction)
- Bias: Nearly zero (all within ±0.2%)
- Improved accuracy in stable period (average error 2.34%)
- Particularly high accuracy for USDTRY (MAE 1.44%)

**Error Distribution (Stable Period, USDTRY):**
- Approximately 90% within 2% error
- 64.3% within 1% error

**Large Outliers:**
- Political events (Turkish presidential election 2023-06)
- Major market volatility (2024-08) leads to larger errors

---

## データソース / Data Source

### 日本語

#### 使用データセット

**入力データ:**
- `../dataset/monthly_mci_backtest_ready_2022_2025.csv`

**内容:**
- 月次為替レート（S_USDJPY, S_USDTRY, S_TRYJPY）
- PPP値（PPP_JPY, PPP_TRY）
- m座標（m_USD, m_JPY, m_TRY）
- 前月とのm座標変動（delta_m_USD, delta_m_JPY, delta_m_TRY）
- **3カ月移動平均**（avg_delta_m_USD_3m, avg_delta_m_JPY_3m, avg_delta_m_TRY_3m）

**データ作成:**
```bash
cd ../dataset
python create_backtest_dataset.py      # delta_m_* を追加
python add_rolling_averages.py          # avg_delta_m_*_3m を追加
```

#### データ特性

- **PPP**: 年次PPPを月次で線形補間（実験的）
- **為替レート**: IMF IFS月次平均レート
- **期間**: 2022-01〜2025-11（47ヶ月）
- **PPP 2025年**: IMF WEO October 2025の投影値を使用（確定値は2026年10月IMF WEOで公表予定）

#### 出力ファイル

**`backtest_rolling_avg_results.csv`** - 全期間のバックテスト結果（45ヶ月分）

**列構成:**

| 列名 | 説明 |
|------|------|
| `base_month` | 基準月（この月のデータを使って予想） |
| `target_month` | 予想対象月（この月の実績と比較） |
| `pred_USDJPY` | USD/JPY予想値 |
| `actual_USDJPY` | USD/JPY実績値 |
| `error_pct_USDJPY` | USD/JPY誤差率（%） |
| `pred_USDTRY` | USD/TRY予想値 |
| `actual_USDTRY` | USD/TRY実績値 |
| `error_pct_USDTRY` | USD/TRY誤差率（%） |
| `pred_TRYJPY` | TRY/JPY予想値 |
| `actual_TRYJPY` | TRY/JPY実績値 |
| `error_pct_TRYJPY` | TRY/JPY誤差率（%） |
| `avg_delta_m_USD` | 使用したUSD m座標3カ月平均変動 |
| `avg_delta_m_JPY` | 使用したJPY m座標3カ月平均変動 |
| `avg_delta_m_TRY` | 使用したTRY m座標3カ月平均変動 |

#### 注意事項

**データの制約:**
- 月次平均レートを使用しているため、月内の急激な変動は捉えられない
- 2025年のPPPはIMF WEO October 2025の投影値（確定値は2026年10月IMF WEOで公表予定）
- 政治イベント等の突発的要因による変動は予測困難

**実務での利用:**
- あくまで統計的・理論的アプローチ
- 実際の取引判断には追加の分析が必要
- 政治イベント時は精度が低下する可能性に注意
- 短期のフロー主導相場（日銀介入、急激な金利変動等）には弱い

### English

#### Dataset Used

**Input Data:**
- `../dataset/monthly_mci_backtest_ready_2022_2025.csv`

**Contents:**
- Monthly exchange rates (S_USDJPY, S_USDTRY, S_TRYJPY)
- PPP values (PPP_JPY, PPP_TRY)
- m-coordinates (m_USD, m_JPY, m_TRY)
- Month-over-month m-coordinate changes (delta_m_USD, delta_m_JPY, delta_m_TRY)
- **3-month moving averages** (avg_delta_m_USD_3m, avg_delta_m_JPY_3m, avg_delta_m_TRY_3m)

**Data Preparation:**
```bash
cd ../dataset
python create_backtest_dataset.py      # Add delta_m_*
python add_rolling_averages.py          # Add avg_delta_m_*_3m
```

#### Data Characteristics

- **PPP**: Annual PPP linearly interpolated to monthly (experimental)
- **Exchange Rates**: IMF IFS monthly average rates
- **Period**: 2022-01 to 2025-11 (47 months)
- **PPP 2025**: Using IMF WEO October 2025 projection values (actual values to be published in IMF WEO October 2026)

#### Output Files

**`backtest_rolling_avg_results.csv`** - Full period backtest results (45 months)

**Column Structure:**

| Column | Description |
|--------|-------------|
| `base_month` | Base month (data used for prediction) |
| `target_month` | Target month (compared with actual results) |
| `pred_USDJPY` | USD/JPY predicted value |
| `actual_USDJPY` | USD/JPY actual value |
| `error_pct_USDJPY` | USD/JPY error rate (%) |
| `pred_USDTRY` | USD/TRY predicted value |
| `actual_USDTRY` | USD/TRY actual value |
| `error_pct_USDTRY` | USD/TRY error rate (%) |
| `pred_TRYJPY` | TRY/JPY predicted value |
| `actual_TRYJPY` | TRY/JPY actual value |
| `error_pct_TRYJPY` | TRY/JPY error rate (%) |
| `avg_delta_m_USD` | USD m-coordinate 3-month average change used |
| `avg_delta_m_JPY` | JPY m-coordinate 3-month average change used |
| `avg_delta_m_TRY` | TRY m-coordinate 3-month average change used |

#### Notes

**Data Limitations:**
- Uses monthly average rates, cannot capture intra-month rapid fluctuations
- 2025 PPP uses IMF WEO October 2025 projection values (actual values to be published in IMF WEO October 2026)
- Difficult to predict fluctuations due to sudden factors such as political events

**Practical Use:**
- This is a statistical and theoretical approach
- Additional analysis required for actual trading decisions
- Note potential accuracy decline during political events
- Weakness in short-term flow-driven markets (BOJ intervention, rapid interest rate changes, etc.)

---

**作成日 / Created**: 2025-12-01
**論文参照 / Paper Reference**: `../docs/FULL_PAPER_CORRECTED.md` 第8章 / Chapter 8
