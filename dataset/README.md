# MCI Dataset & Backtest - 統合ドキュメント

**Mikan 3-Currency clr Index (MCI)**
**データセット・バックテスト・データ取得 統合ドキュメント**

Version 2.0 | 2026-01-08

---

## 目次

1. [プロジェクト概要](#1-プロジェクト概要)
2. [ファイル構成](#2-ファイル構成)
3. [データ取得仕様](#3-データ取得仕様)
4. [データセット詳細](#4-データセット詳細)
5. [バックテスト方法論](#5-バックテスト方法論)
6. [使用例](#6-使用例)
7. [データ更新手順](#7-データ更新手順)
8. [参考資料](#8-参考資料)

---

## 1. プロジェクト概要

### 1.1 MCI指数とは

**Mikan 3-Currency clr Index (MCI)** は、購買力平価（PPP）を基準とした為替レート評価指標です。

**特徴:**
- **理論基盤**: Aitchison (1986) の組成データ分析（Compositional Data Analysis）
- **変換手法**: clr変換（centered log-ratio transformation）
- **ゼロサム制約**: m[USD] + m[JPY] + m[TRY] = 0（厳密に充足）
- **予測手法**: 過去3カ月のm座標変動平均を翌月に外挿

### 1.2 研究成果

**構造安定期（2023-08～2025-11、28カ月）の予測精度:**
- **MAE（3通貨ペア平均）**: 2.34%
- **RMSE（3通貨ペア平均）**: 3.54%
- **評価**: 極めて高い予測精度（MAE < 2.5%）

**論文掲載:**
- 証券アナリストジャーナル（投稿準備中）
- GitHub Pages: [MCI Project](https://github.com/...)

---

## 2. ファイル構成

### 📁 ディレクトリ構成

```
dataset/
├── データファイル（3個）
│   ├── annual_mci_2005_2024.csv              # 20年年次データ
│   ├── monthly_mci_fixed_ppp_2022_2025.csv   # 固定PPP版（比較検証用）
│   └── monthly_mci_complete_2022_2025.csv    # 完全版（v2.0修正済み）
│
├── スクリプト（2個）
│   ├── backtest_with_rolling_avg.py          # バックテスト実行
│   └── analyze_rolling_avg_results.py        # 結果分析
│
└── ドキュメント（4個）
    ├── README.md                              # 本ファイル（統合ドキュメント）
    ├── BACKTEST_README.md                     # バックテスト詳細理論
    ├── BACKTEST_ANALYSIS.md                   # 定量的評価（日本語）
    └── BACKTEST_ANALYSIS_EN.md                # 定量的評価（英語）
```

### 📊 データファイル一覧

| ファイル名 | 説明 | 期間 | 行数 | サイズ | 用途 |
|-----------|------|------|------|-------|------|
| `annual_mci_2005_2024.csv` | 20年年次データ | 2005-2024 | 20 | ~2KB | 長期トレンド分析 |
| `monthly_mci_fixed_ppp_2022_2025.csv` | 固定PPP版（比較用） | 2022-2025 | 47 | ~8KB | PPP補間の効果検証 |
| `monthly_mci_complete_2022_2025.csv` | **完全版（推奨）⭐** | 2022-2025 | 47 | ~12KB | **MCI分析・バックテスト評価** |

**各ファイルの関係:**
```
annual_mci_2005_2024.csv        ← 長期トレンド分析用（20年）
     ↓
monthly_mci_fixed_ppp_2022_2025.csv    ← 比較検証用（PPP固定版）
     ↓
monthly_mci_complete_2022_2025.csv     ← メインデータ（PPP線形補間済み + バックテスト結果統合）
```

### 🔧 スクリプト一覧

| ファイル名 | 説明 | 実行時間 |
|-----------|------|---------|
| `backtest_with_rolling_avg.py` | バックテスト実行（43カ月分） | ~1秒 |
| `analyze_rolling_avg_results.py` | 結果統計分析 | ~0.1秒 |

---

## 3. データ取得仕様

### 3.1 必要データ

MCI計算に必要なデータは2種類：

| データ種別 | 内容 | 頻度 | ソース |
|-----------|------|------|--------|
| **為替レート** | Domestic currency per USD（期間平均） | 月次 | IMF IFS |
| **PPP** | Implied PPP conversion rate（LCU per intl$） | 年次 | IMF WEO |

### 3.2 データソースAPI

#### 為替レート（IMF IFS）

**API仕様:**
```
エンドポイント: https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.STA/ER/{countries}/*.XDC_USD.ENDA.M
インジケーター: ENDA_XDC_USD_RATE
形式: SDMX 3.0 JSON
認証: 不要
```

**リクエスト例:**
```bash
# 日本とトルコの月次為替レート
curl "https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.STA/ER/JP+TR/*.XDC_USD.ENDA.M"
```

**パラメータ:**
- `{countries}`: ISO 3166 Alpha-2コード（例: JP, TR, GB）
- `XDC_USD`: Domestic currency per USD（固定）
- `ENDA`: Period average（期間平均、固定）
- `M`: Monthly（月次）

#### PPP（IMF WEO）

**API仕様:**
```
エンドポイント: https://www.imf.org/external/datamapper/api/v1/PPPEX/{countries}
インジケーター: PPPEX
形式: JSON
認証: 不要
投影値: 2030年まで含む
```

**リクエスト例:**
```bash
# 日本とトルコのPPP（特定年）
curl "https://www.imf.org/external/datamapper/api/v1/PPPEX/JPN/TUR?periods=2021,2022,2023,2024,2025"
```

**パラメータ:**
- `{countries}`: ISO 3166 Alpha-3コード（例: JPN, TUR, GBR）
- `periods`: 年フィルター（オプション）

**レスポンス例:**
```json
{
  "values": {
    "PPPEX": {
      "JPN": {
        "2021": 98.691,
        "2022": 92.759,
        "2023": 92.535,
        "2024": 93.200,
        "2025": 93.520
      },
      "TUR": {
        "2021": 2.726,
        "2022": 4.884,
        "2023": 8.733,
        "2024": 12.550,
        "2025": 16.510
      }
    }
  }
}
```

### 3.3 国コードマッピング

**⚠️ 重要:** 為替レートAPIとPPP APIで国コード体系が異なります。

| API | 国コード体系 | 日本 | トルコ | 英国 |
|-----|------------|------|--------|------|
| **IMF IFS（為替レート）** | ISO 3166 Alpha-2 | `JP` | `TR` | `GB` |
| **IMF WEO（PPP）** | ISO 3166 Alpha-3 | `JPN` | `TUR` | `GBR` |

**主要通貨の国コードマッピング:**

| 通貨 | 通貨コード | Alpha-2 | Alpha-3 | 国名 |
|------|----------|---------|---------|------|
| 日本円 | JPY | JP | JPN | Japan |
| トルコリラ | TRY | TR | TUR | Türkiye |
| 米ドル | USD | US | USA | United States |
| ユーロ | EUR | EMU | EMU | Euro Area |
| 英ポンド | GBP | GB | GBR | United Kingdom |
| 中国元 | CNY | CN | CHN | China |
| インドルピー | INR | IN | IND | India |
| ブラジルレアル | BRL | BR | BRA | Brazil |
| メキシコペソ | MXN | MX | MEX | Mexico |
| 韓国ウォン | KRW | KR | KOR | Korea, Republic of |

完全なマッピング表（50通貨）は `DATA_ACQUISITION_SPEC.md` の付録Aを参照。

### 3.4 データ更新スケジュール

| データ | 更新頻度 | 推奨取得タイミング | 備考 |
|--------|---------|------------------|------|
| **為替レート（確定値）** | 月次 | 毎月10日以降 | IMF IFSに掲載 |
| **為替レート（速報値）** | 日次 | リアルタイム | 各国中銀データ |
| **PPP（投影値）** | 年2回 | 4月下旬、10月下旬 | WEO公表時 |
| **PPP（確定値）** | 年1回 | 翌年10月 | ICP結果反映 |

**更新ワークフロー:**
```
1. 月初（1-10日）
   └─ 前月為替レート確定値を取得

2. WEO公表月（4月・10月）
   ├─ PPP投影値を取得
   ├─ 前年PPP確定値を取得（10月のみ）
   └─ データセット全体を再計算

3. ICP改訂時（3-6年ごと）
   └─ 過去データ全体を再取得・再計算
```

---

## 4. データセット詳細

### 4.1 annual_mci_2005_2024.csv

**ファイル名:** `annual_mci_2005_2024.csv`
**説明:** 20年間の年次データ（2005-2024年）
**期間:** 2005年～2024年（20年）
**行数:** 20行（ヘッダー含めて21行）
**列数:** 9列
**用途:** 長期構造変化の分析、論文の図1「年次m座標の推移」

#### 列の説明

**全て計算済みデータ（入力データと計算値の両方を含む）:**

| 列名 | 説明 | 単位 | データ種別 | 備考 |
|------|------|------|-----------|------|
| `year` | 年 | YYYY | - | 2005-2024 |
| `PPP_JPY` | 日本円PPP | JPY per intl$ | **入力：IMF WEO年次確定値** | |
| `PPP_TRY` | トルコリラPPP | TRY per intl$ | **入力：IMF WEO年次確定値** | |
| `S_USDJPY` | USD/JPY為替レート | JPY | **入力：IMF IFS年平均** | |
| `S_USDTRY` | USD/TRY為替レート | TRY | **入力：IMF IFS年平均** | |
| `d_USDJPY` | USD/JPY PPP乖離率 | - | **計算値** | `ln(S_USDJPY/PPP_JPY)` |
| `d_USDTRY` | USD/TRY PPP乖離率 | - | **計算値** | `ln(S_USDTRY/PPP_TRY)` |
| `m_USD` | 米ドルm座標 | - | **計算値（clr変換）** | |
| `m_JPY` | 日本円m座標 | - | **計算値（clr変換）** | |
| `m_TRY` | トルコリラm座標 | - | **計算値（clr変換）** | |

**データソース:**
- **PPP**: IMF World Economic Outlook Database（October 2024）
- **為替レート**: IMF International Financial Statistics（期間平均）

**用途:**
- 長期構造変化の分析
- 論文の図1「年次m座標の推移」
- 3つの構造転換点（2011年、2018年、2022年）の検出

---

### 4.2 monthly_mci_fixed_ppp_2022_2025.csv

**ファイル名:** `monthly_mci_fixed_ppp_2022_2025.csv`
**説明:** 固定PPP版（比較検証用）
**期間:** 2022年1月～2025年11月（47カ月）
**行数:** 47行（ヘッダー含めて48行）
**列数:** 11列
**用途:** PPP線形補間の効果検証、論文第8章「固定PPPとの比較」

#### 特徴

- ✅ **PPPを年次で固定**（月中変化なし）
- ✅ 各年1月1日にPPP値が階段状に変化
- ✅ 論文第8章「補間なし」の比較検証に使用
- ⚠️ **注意:** このファイルはバックテストには使用しません（`monthly_mci_complete_2022_2025.csv`を使用）

#### 列の説明

| 列名 | 説明 | 単位 | データ種別 | 備考 |
|------|------|------|-----------|------|
| `date` | 年月 | YYYY-MM | - | 2022-01～2025-11（47カ月） |
| `S_USDJPY` | USD/JPY為替レート | JPY | **入力：IMF IFS月次平均** | |
| `S_USDTRY` | USD/TRY為替レート | TRY | **入力：IMF IFS月次平均** | |
| `S_TRYJPY` | TRY/JPY為替レート | JPY | **計算値** | `S_USDJPY / S_USDTRY` |
| `PPP_JPY` | 日本円PPP（固定） | JPY per intl$ | **入力：年次で固定** | 2022年全月=92.5 |
| `PPP_TRY` | トルコリラPPP（固定） | TRY per intl$ | **入力：年次で固定** | 2022年全月=4.975 |
| `d_USDJPY` | USD/JPY PPP乖離率 | - | **計算値** | `ln(S_USDJPY / PPP_JPY)` |
| `d_USDTRY` | USD/TRY PPP乖離率 | - | **計算値** | `ln(S_USDTRY / PPP_TRY)` |
| `m_USD` | 米ドルm座標 | - | **計算値（clr変換）** | |
| `m_JPY` | 日本円m座標 | - | **計算値（clr変換）** | |
| `m_TRY` | トルコリラm座標 | - | **計算値（clr変換）** | |

**用途:**
- PPP線形補間の効果検証
- 論文第8章「固定PPPとの比較」
- **線形補間版（`monthly_mci_complete_2022_2025.csv`）との比較分析**

---

### 4.3 monthly_mci_complete_2022_2025.csv ⭐

**ファイル名:** `monthly_mci_complete_2022_2025.csv`
**説明:** 月次MCI完全版データセット（m座標、予測値、誤差を含む統合データ、v2.0修正済み）
**期間:** 2022年1月～2025年11月（47カ月）
**行数:** 47行（ヘッダー含めて48行）
**列数:** 25列（基本データ19列 + 予測値3列 + 誤差3列）
**用途:** MCI分析、バックテスト評価、論文の表4・表5の計算元

#### 特徴

- ✅ **2022年PPPを線形補間済み**（2021年→2022年）
- ✅ 3カ月移動平均（`avg_delta_m_*_3m`）を含む
- ✅ **バックテスト結果統合**（予測値・誤差、2022-05～2025-11の43カ月分）
- ✅ ゼロサム制約を厳密に充足（最大偏差 < 10^-15）

#### データフロー図

```
【入力データ】
  ↓
S_USDJPY, S_USDTRY (為替レート) ← IMF IFS
PPP_JPY, PPP_TRY (PPP) ← IMF WEO（線形補間済み）
  ↓
【計算値】
  ↓
S_TRYJPY = S_USDJPY / S_USDTRY (クロスレート)
d_USDJPY, d_USDTRY (PPP乖離率)
  ↓
m_USD, m_JPY, m_TRY (m座標) ← clr変換
  ↓
【時系列変動】
  ↓
delta_m_* = m[t] - m[t-1] (月次変動)
  ↓
【予測用データ】
  ↓
avg_delta_m_*_3m = rolling(3).mean() (3カ月平均変動)
  ↓
【バックテスト実行】
  ↓
m_predicted[t+1] = m[t] + avg_delta_m_3m[t]
S_predicted[t+1] = PPP[t+1] × exp(m_predicted[t+1])
  ↓ pred_USDJPY, pred_USDTRY, pred_TRYJPY
【予測誤差】
  ↓
error_pct_* = (pred_* - actual_*) / actual_* × 100
```

#### 列の詳細説明

##### 📥 **グループ1: 入力データ（IMFから取得）**

| 列名 | 説明 | 単位 | データソース | 備考 |
|------|------|------|-------------|------|
| `date` | 年月 | YYYY-MM | - | 2022-01～2025-11（47カ月） |
| `S_USDJPY` | USD/JPY為替レート（実績値） | JPY | IMF IFS月次平均 | **入力データ：実際の市場レート** |
| `S_USDTRY` | USD/TRY為替レート（実績値） | TRY | IMF IFS月次平均 | **入力データ：実際の市場レート** |
| `PPP_JPY` | 日本円PPP | JPY per intl$ | IMF WEO（線形補間済み） | **入力データ：2021-2022年を線形補間** |
| `PPP_TRY` | トルコリラPPP | TRY per intl$ | IMF WEO（線形補間済み） | **入力データ：2021-2022年を線形補間** |

##### 🔢 **グループ2: 基本計算値（為替レートから導出）**

| 列名 | 説明 | 単位 | 計算式 | 備考 |
|------|------|------|--------|------|
| `S_TRYJPY` | TRY/JPY為替レート（クロスレート） | JPY | `S_USDJPY / S_USDTRY` | **計算値：2つの為替レートから算出** |
| `d_USDJPY` | USD/JPY PPP乖離率 | - | `ln(S_USDJPY / PPP_JPY)` | **計算値：対数での乖離率** |
| `d_USDTRY` | USD/TRY PPP乖離率 | - | `ln(S_USDTRY / PPP_TRY)` | **計算値：対数での乖離率** |

##### 📊 **グループ3: m座標（MCI指数の中核）**

| 列名 | 説明 | 単位 | 計算式 | 備考 |
|------|------|------|--------|------|
| `m_USD` | 米ドルm座標 | - | `ln(r_USD / G)` | **計算値：clr変換後の座標** |
| `m_JPY` | 日本円m座標 | - | `ln(r_JPY / G)` | **計算値：clr変換後の座標** |
| `m_TRY` | トルコリラm座標 | - | `ln(r_TRY / G)` | **計算値：clr変換後の座標** |

**注:**
- `r_USD = 1.0`（基準通貨）
- `r_JPY = S_USDJPY / PPP_JPY`
- `r_TRY = S_USDTRY / PPP_TRY`
- `G = (r_USD × r_JPY × r_TRY)^(1/3)`（幾何平均）
- **ゼロサム制約:** `m_USD + m_JPY + m_TRY = 0`（厳密に充足）

##### 📐 **グループ4: 補助的計算値**

| 列名 | 説明 | 単位 | 計算式 | 備考 |
|------|------|------|--------|------|
| `D_mTRY` | TRY/JPYのm座標差 | - | `m_TRY - m_JPY` | **計算値：2通貨間のm座標差** |
| `pct_TRYJPY` | TRY/JPY乖離率 | % | `(S_TRYJPY/PPP_cross - 1) × 100` | **計算値：パーセント表示の乖離率** |

##### 📈 **グループ5: 時系列変動値（月次差分）**

| 列名 | 説明 | 単位 | 計算式 | 備考 |
|------|------|------|--------|------|
| `delta_m_USD` | USDのm座標変動（月次） | - | `m_USD[t] - m_USD[t-1]` | **計算値：最初の月（2022-01）はNaN** |
| `delta_m_JPY` | JPYのm座標変動（月次） | - | `m_JPY[t] - m_JPY[t-1]` | **計算値：最初の月（2022-01）はNaN** |
| `delta_m_TRY` | TRYのm座標変動（月次） | - | `m_TRY[t] - m_TRY[t-1]` | **計算値：最初の月（2022-01）はNaN** |

##### 🎯 **グループ6: 予測用データ（3カ月移動平均）**

| 列名 | 説明 | 単位 | 計算式 | 備考 |
|------|------|------|--------|------|
| `avg_delta_m_USD_3m` | USDの3カ月平均変動 | - | `rolling(3).mean()` | **予測用：最初の3カ月（2022-01～03）はNaN** |
| `avg_delta_m_JPY_3m` | JPYの3カ月平均変動 | - | `rolling(3).mean()` | **予測用：最初の3カ月（2022-01～03）はNaN** |
| `avg_delta_m_TRY_3m` | TRYの3カ月平均変動 | - | `rolling(3).mean()` | **予測用：最初の3カ月（2022-01～03）はNaN** |

**重要:** これらの3カ月平均がバックテストで「翌月予測」に使用されます。
- 例：2024-10の`avg_delta_m_*_3m`を使って2024-11を予測

##### 🔮 **グループ7: バックテスト結果（予測値と誤差）**

| 列名 | 説明 | 単位 | 計算式 | 備考 |
|------|------|------|--------|------|
| `pred_USDJPY` | USD/JPY予測レート | JPY | `PPP_JPY[t] × exp(m_pred_USD[t] - m_pred_JPY[t])` | **予測値：最初の4カ月（2022-01～04）はNaN** |
| `pred_USDTRY` | USD/TRY予測レート | TRY | `PPP_TRY[t] × exp(m_pred_USD[t] - m_pred_TRY[t])` | **予測値：最初の4カ月（2022-01～04）はNaN** |
| `pred_TRYJPY` | TRY/JPY予測レート | JPY | `pred_USDJPY / pred_USDTRY` | **予測値：クロスレート** |
| `error_pct_USDJPY` | USD/JPY予測誤差 | % | `(pred_USDJPY - S_USDJPY) / S_USDJPY × 100` | **誤差：正なら過大評価** |
| `error_pct_USDTRY` | USD/TRY予測誤差 | % | `(pred_USDTRY - S_USDTRY) / S_USDTRY × 100` | **誤差：正なら過大評価** |
| `error_pct_TRYJPY` | TRY/JPY予測誤差 | % | `(pred_TRYJPY - S_TRYJPY) / S_TRYJPY × 100` | **誤差：正なら過大評価** |

**予測m座標の計算:**
```
m_pred[t] = m[t-1] + avg_delta_m_3m[t-1]
```

**予測期間:** 2022-05～2025-11（43カ月分）

**予測精度（構造安定期 2023-08～2025-11、28カ月）:**
- MAE（平均絶対誤差）: 2.34%
- RMSE（二乗平均平方根誤差）: 3.54%

#### m座標の計算式

**PPP乖離率:**
```
r_USD = 1.0  （USDは基準通貨）
r_JPY = S_USDJPY / PPP_JPY
r_TRY = S_USDTRY / PPP_TRY
```

**幾何平均:**
```
G = (r_USD × r_JPY × r_TRY)^(1/3)
```

**m座標（clr変換）:**
```
m[i] = ln(r_i / G)  （i = USD, JPY, TRY）
```

**為替レート逆算式:**
```
S(A/B) = PPP(A/B) × exp(m[A] - m[B])
```

#### データ品質

| 項目 | 状態 |
|------|------|
| 2022年PPP補間 | ✅ 完了（2021-2022年線形補間） |
| ゼロサム制約 | ✅ 充足（最大偏差 < 10^-15） |
| 欠損値 | ✅ なし（delta_mは最初の月のみNaN） |
| データ期間 | 47カ月（2022-01 ~ 2025-11） |
| 3カ月移動平均 | ✅ 計算済み（44カ月分、最初の2カ月はNaN） |

#### ⚠️ 重要な修正履歴（v2.0）

**修正内容:**
- **2022年1-12月のPPPを線形補間で修正**
- 修正前：2022年全月が固定値（JPY=92.5、TRY=4.975）
- 修正後：2021年値→2022年値を線形補間
  - JPY: 98.691 → 92.759（月次に分割）
  - TRY: 2.726 → 4.884（月次に分割）

**修正の影響:**
- ✅ **構造安定期の予測精度が改善**
  - MAE: 2.83% → **2.34%**（-0.49pp）
  - RMSE: 3.98% → **3.54%**（-0.44pp）

**データソース:**
- **PPP**: IMF WEO（2021, 2022, 2023年次値から線形補間）
  - 2021年: JPY=98.691, TRY=2.726
  - 2022年: JPY=92.759, TRY=4.884
  - 2023年: JPY=92.535, TRY=8.733
- **為替レート**: IMF IFS（月次平均）

**用途:**
- **バックテストの入力データ**
- 月次予測の基礎データ
- 論文の表4・表5の計算元
- 論文第7章「バックテストによる精度検証」

---
## 5. バックテスト方法論

### 5.1 予測手法

**基本方針:** 過去3カ月のm座標変動平均を翌月に外挿

**予測式:**
```python
# N+1月を予測（N月時点）
avg_Δm = (Δm[N-2] + Δm[N-1] + Δm[N]) / 3
m_predicted[N+1] = m[N] + avg_Δm
S_predicted[N+1] = PPP[N+1] × exp(m_predicted[N+1])
```

**特徴:**
- シンプルな移動平均モデル
- 短期トレンドを捉える
- 機械学習不使用（統計的アプローチ）

### 5.2 バックテスト実行方法

#### 全期間バックテスト

```bash
cd dataset
python backtest_with_rolling_avg.py --comprehensive
```

**出力:**
- `monthly_mci_complete_2022_2025.csv`に予測値と誤差を追加（25列に拡張）
- コンソール出力：各月の予測vs実績

#### 単月テスト

```bash
# 2024年10月→11月の予測をテスト
python backtest_with_rolling_avg.py --base-month 2024-10
```

### 5.3 結果分析

```bash
# 全期間分析
python analyze_rolling_avg_results.py

# 構造安定期のみ分析（2023-08以降）
python analyze_rolling_avg_results.py 2023-08
```

### 5.4 バックテスト結果

#### 全期間（2022-04 ~ 2025-11、43カ月）

| 通貨ペア | 件数 | 平均誤差 | MAE | RMSE |
|---------|------|---------|-----|------|
| USD/JPY | 43 | -9.15% | 14.66% | 25.63% |
| USD/TRY | 43 | -9.44% | 31.45% | 58.27% |
| TRY/JPY | 43 | +147.29% | 156.58% | 336.18% |
| **3ペア平均** | 43 | - | **67.56%** | **197.54%** |

**⚠️ 注意:** 全期間の大きな誤差は2022年の極端なレジームシフト期（ウクライナ戦争、世界的インフレ急騰、トルコリラ危機）を反映しています。この期間の誤差は300-900%に達しました。

#### 構造安定期（2023-08 ~ 2025-11、28カ月）⭐

| 通貨ペア | 件数 | MAE | RMSE | バイアス |
|---------|------|-----|------|---------|
| USD/JPY | 28 | **2.19%** | 3.23% | +0.03% |
| USD/TRY | 28 | **1.44%** | 2.72% | +0.68% |
| TRY/JPY | 28 | 3.38% | 4.46% | -0.57% |
| **3ペア平均** | 28 | **2.34%** | **3.54%** | - |

**評価:** 構造安定期において極めて高い予測精度を達成（MAE < 2.5%、RMSE < 4.0%）。ほぼ無バイアス（全ペアでバイアス < 1%）。

#### 誤差分布（構造安定期、28カ月）

**USD/JPY:**
- 0-1%: 11カ月（39.3%）
- 1-2%: 7カ月（25.0%）
- 2-3%: 3カ月（10.7%）
- 3-5%: 4カ月（14.3%）
- 5-10%: 3カ月（10.7%）
- 10%+: 0カ月（0.0%）

**USD/TRY:**
- 0-1%: 18カ月（64.3%）← 最も高精度
- 1-2%: 7カ月（25.0%）
- 2-3%: 1カ月（3.6%）

**TRY/JPY:**
- 0-1%: 5カ月（17.9%）
- 1-2%: 6カ月（21.4%）
- 2-3%: 6カ月（21.4%）

詳細は `BACKTEST_ANALYSIS.md` を参照。

---

## 6. 使用例

### 6.1 データ読み込み

```python
import pandas as pd
import numpy as np

# 完全版データの読み込み
df = pd.read_csv('monthly_mci_complete_2022_2025.csv')

# 最新月のm座標を確認
latest = df.iloc[-1]
print(f"{latest['date']}のm座標:")
print(f"  m[USD]: {latest['m_USD']:+.6f}")
print(f"  m[JPY]: {latest['m_JPY']:+.6f}")
print(f"  m[TRY]: {latest['m_TRY']:+.6f}")
print(f"  合計: {latest['m_USD'] + latest['m_JPY'] + latest['m_TRY']:.2e}")
```

**出力例:**
```
2025-11のm座標:
  m[USD]: +0.123456
  m[JPY]: -0.234567
  m[TRY]: +0.111111
  合計: -1.39e-16  # ゼロサム制約充足
```

### 6.2 翌月予測

```python
# 最新3カ月の平均変動で翌月を予測
last_3m_avg_usd = df['avg_delta_m_USD_3m'].iloc[-1]
last_3m_avg_jpy = df['avg_delta_m_JPY_3m'].iloc[-1]
last_3m_avg_try = df['avg_delta_m_TRY_3m'].iloc[-1]

# 翌月のm座標を予測
pred_m_usd = latest['m_USD'] + last_3m_avg_usd
pred_m_jpy = latest['m_JPY'] + last_3m_avg_jpy
pred_m_try = latest['m_TRY'] + last_3m_avg_try

# 翌月のPPP（仮に最新月と同じと仮定）
ppp_jpy_next = 93.52  # 2026年のIMF投影値
ppp_try_next = 17.50  # 2026年のIMF投影値

# 為替レートを逆算
pred_usdjpy = ppp_jpy_next * np.exp(pred_m_usd - pred_m_jpy)
pred_usdtry = ppp_try_next * np.exp(pred_m_usd - pred_m_try)
pred_tryjpy = pred_usdjpy / pred_usdtry

print(f"\n2025-12予測:")
print(f"  USD/JPY: {pred_usdjpy:.2f}")
print(f"  USD/TRY: {pred_usdtry:.2f}")
print(f"  TRY/JPY: {pred_tryjpy:.2f}")
```

### 6.3 ゼロサム制約検証

```python
# 全期間のゼロサム制約を検証
df['m_sum'] = df['m_USD'] + df['m_JPY'] + df['m_TRY']
max_deviation = df['m_sum'].abs().max()

print(f"ゼロサム制約検証:")
print(f"  最大偏差: {max_deviation:.2e}")
print(f"  制約充足: {'OK' if max_deviation < 1e-10 else 'NG'}")
```

### 6.4 長期トレンド可視化

```python
import matplotlib.pyplot as plt

# 年次データを読み込み
df_annual = pd.read_csv('annual_mci_2005_2024.csv')

# m座標の推移をプロット
plt.figure(figsize=(12, 6))
plt.plot(df_annual['year'], df_annual['m_USD'], 'o-', label='USD')
plt.plot(df_annual['year'], df_annual['m_JPY'], 's-', label='JPY')
plt.plot(df_annual['year'], df_annual['m_TRY'], '^-', label='TRY')
plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
plt.xlabel('Year')
plt.ylabel('m-coordinate')
plt.title('MCI Long-term Trend (2005-2024)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

---

## 7. データ更新手順

### 7.1 月次更新（毎月10日以降）

#### Step 1: 為替レートの取得

```bash
# IMF IFSから最新月の為替レートを取得
curl "https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.STA/ER/JP+TR/*.XDC_USD.ENDA.M" \
  > exchange_rates_latest.json
```

#### Step 2: データセットに追加

```python
import pandas as pd

# 既存データを読み込み
df = pd.read_csv('monthly_mci_complete_2022_2025.csv')

# 新しい月のデータを追加（例: 2025-12）
new_row = {
    'date': '2025-12',
    'S_USDJPY': 153.80,  # IMF IFSから取得
    'S_USDTRY': 35.20,   # IMF IFSから取得
    'S_TRYJPY': 153.80 / 35.20,
    'PPP_JPY': 93.52,    # 前月と同じ（年次更新まで）
    'PPP_TRY': 17.50,    # 前月と同じ（年次更新まで）
    # d値、m座標、delta_mを計算...
}

df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
df.to_csv('monthly_mci_complete_2022_2025.csv', index=False)
```

#### Step 3: 3カ月移動平均を再計算

```python
# 3カ月移動平均を再計算
df['avg_delta_m_USD_3m'] = df['delta_m_USD'].rolling(window=3, min_periods=3).mean()
df['avg_delta_m_JPY_3m'] = df['delta_m_JPY'].rolling(window=3, min_periods=3).mean()
df['avg_delta_m_TRY_3m'] = df['delta_m_TRY'].rolling(window=3, min_periods=3).mean()

df.to_csv('monthly_mci_complete_2022_2025.csv', index=False)
```

### 7.2 年次更新（4月・10月のWEO公表時）

#### Step 1: PPP投影値の取得

```bash
# IMF WEOから最新のPPP投影値を取得
curl "https://www.imf.org/external/datamapper/api/v1/PPPEX/JPN/TUR?periods=2024,2025,2026" \
  > ppp_latest.json
```

#### Step 2: データセット全体を再計算

```python
# PPP線形補間を再実施
# 2025年の月次データを2024→2025年の線形補間で更新
# m座標、delta_mを全て再計算
# ゼロサム制約を検証
```

詳細な実装は `fix_2022_ppp_interpolation.py` を参考。

### 7.3 バックテストの再実行

```bash
# データ更新後、バックテストを再実行
python backtest_with_rolling_avg.py --comprehensive

# 結果を分析
python analyze_rolling_avg_results.py 2023-08
```

---

## 8. 参考資料

### 8.1 関連ドキュメント

| ドキュメント | 説明 |
|------------|------|
| `BACKTEST_README.md` | バックテスト理論詳細 |
| `BACKTEST_ANALYSIS.md` | バックテスト定量的評価（日本語） |
| `BACKTEST_ANALYSIS_EN.md` | バックテスト定量的評価（英語） |
| `DATA_ACQUISITION_SPEC.md` | データ取得仕様書（完全版） |

### 8.2 IMF公式リソース

- [IMF Data Portal](https://data.imf.org)
- [IMF Exchange Rate Dataset](https://data.imf.org/en/datasets/IMF.STA:ER)
- [IMF WEO Database](https://www.imf.org/en/Publications/WEO/weo-database)
- [IMF API Portal](https://portal.api.imf.org/apis)

### 8.3 技術リソース

- [fgeerolf.com - IMF API Guide](https://fgeerolf.com/data/imf/api.html)
- [GitHub: codeforIATI/imf-exchangerates](https://github.com/codeforIATI/imf-exchangerates)
- [DBnomics - IMF/IFS](https://db.nomics.world/IMF/IFS)
- [pandasdmx Documentation](https://pandasdmx.readthedocs.io/)

### 8.4 理論的背景

- Aitchison, J. (1986). *The Statistical Analysis of Compositional Data*. Chapman & Hall.
- IMF (2024). *World Economic Outlook Database*, October 2024.
- PPP（購買力平価）の国際比較プログラム（ICP）

### 8.5 論文

- 証券アナリストジャーナル（投稿準備中）
- GitHub Pages: [MCI Project Documentation](https://github.com/...)

---

## 9. トラブルシューティング

### Q1: ゼロサム制約が充足されない

**原因:** 計算精度の問題、または誤った計算式

**対処法:**
```python
# 幾何平均を正確に計算
G = (r_USD * r_JPY * r_TRY) ** (1/3)

# m座標を計算
m_USD = np.log(r_USD / G)
m_JPY = np.log(r_JPY / G)
m_TRY = np.log(r_TRY / G)

# 検証（偏差 < 10^-15 であること）
assert abs(m_USD + m_JPY + m_TRY) < 1e-10
```

### Q2: APIからデータが取得できない

**原因:** エンドポイント変更、レート制限、ネットワークエラー

**対処法:**
1. 国コード（Alpha-2/Alpha-3）を確認
2. IMF Data Portalで手動検索
3. リトライ（最大3回）
4. DataHelp@imf.org に問い合わせ

### Q3: バックテスト精度が低い

**原因:** レジームシフト期、データ品質問題

**対処法:**
1. 対象期間を確認（構造安定期のみに限定）
2. PPP線形補間が正しく実施されているか確認
3. 3カ月移動平均が計算されているか確認

---

## 10. ライセンスと引用

### データライセンス

**IMFデータの利用規約:**
- 非商用利用: 原則自由
- 商用利用: IMFの利用規約を確認
- 出典表記: "Source: International Monetary Fund (IMF)" を推奨

### 引用方法

```
Mikan 3-Currency clr Index (MCI) Dataset
Source: International Monetary Fund (IMF) - IFS, WEO
Processing: [Your Name/Organization]
Version: 2.0 (2026-01-08)
```

---

## 改訂履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|---------|
| 1.0 | 2025-12-01 | 初版作成 |
| 2.0 | 2026-01-08 | 2022年PPP線形補間修正、バックテスト再実行、データ取得仕様統合 |

---

**メンテナンス:** このドキュメントは定期的に更新されます。最新版は GitHub リポジトリを参照してください。

**問い合わせ:** データに関する質問は Issue を作成してください。
