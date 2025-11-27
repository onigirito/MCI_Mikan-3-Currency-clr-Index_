# Dataset: Mikan 3-Currency clr Index

## ファイル一覧

### 1. 年次PPP・年次MCI（公式データ）
- **`annual_mci_2005_2024.csv`**
  - 期間: 2005-2024年（年次）
  - PPP: IMF WEO年次確定値
  - MCI: 年平均為替レートから算出
  - 用途: 長期トレンド分析、論文の主要データ

### 2. 年次PPP・月次MCI（固定PPP版）
- **`monthly_mci_fixed_ppp_2022_2025.csv`**
  - 期間: 2022-01～2025-11（月次、47ヶ月）
  - PPP: 年次固定（年内は同一PPP値を使用）
  - MCI: 月次為替レートから算出
  - 特徴: `PPP_changed`フラグでPPP更新月を明示、`D_mTRY`（TRY座標の月次変化）を含む
  - 用途: 短期変動分析、月次価格推定

### 3. 月次PPP・月次MCI（補間版）
- **`monthly_mci_interpolated_ppp_2022_2025.csv`**
  - 期間: 2022-01～2025-11（月次）
  - PPP: 年次PPPを月次で線形補間
  - MCI: 補間PPP + 月次為替レートから算出
  - 用途: より滑らかな月次分析（実験的）

### 4. 最新月次データ
  - 用途: クイックリファレンス

### 5. 入力データ
- **`monthly_exchange_rates_2022_2025.csv`** - 月次為替レート入力データ（元データ）

---

## データ概要

**対象通貨：** USD, JPY, TRY

### データソース

#### 年次データ（2005-2024）
- **PPP（購買力平価）**: IMF World Economic Outlook (WEO)
  - Implied PPP conversion rate (PPPEX)
  - 単位: LCU per international dollar
- **為替レート**: IMF International Financial Statistics (IFS)
  - Official exchange rate, period average (年次平均)
  - 単位: LCU per USD

#### 月次データ（2022-2025）
- **PPP（購買力平価）**: IMF WEO年次値を使用
  - 年内固定方式: 年次PPP値を月内で一定として使用
  - 補間方式: 年次PPP値を月次で線形補間（実験的）
- **為替レート**: IMF International Financial Statistics (IFS)
  - Official exchange rate, period average (月次平均)
  - 単位: LCU per USD
  - 月次為替レート（S_USDJPY, S_USDTRY）は実際の市場月次平均レートを使用

**注**: 全データソースをIMFに統一することで、PPP（IMF WEO）と為替レート（IMF IFS）の整合性を確保しています。年次データと月次データの為替レート平均値は完全に一致しています。

## 列の説明

| 列名 | 説明 |
|------|------|
| `year` | 年（西暦） |
| `S_USDJPY` | 年平均為替レート USD/JPY |
| `S_USDTRY` | 年平均為替レート USD/TRY |
| `PPP_JPY` | PPP換算レート（JPY per intl$） |
| `PPP_TRY` | PPP換算レート（TRY per intl$） |
| `d_USDJPY` | USD/JPY のPPP乖離率 = ln(S_USDJPY / PPP_JPY) |
| `d_USDTRY` | USD/TRY のPPP乖離率 = ln(S_USDTRY / PPP_TRY) |
| `m_USD` | Mikan 3-Currency clr Index 座標（USD） |
| `m_JPY` | Mikan 3-Currency clr Index 座標（JPY） |
| `m_TRY` | Mikan 3-Currency clr Index 座標（TRY） |
| `S_TRYJPY` | クロスレート TRY/JPY = S_USDJPY / S_USDTRY |
| `PPP_TRYJPY` | PPPクロスレート = PPP_JPY / PPP_TRY |
| `d_TRYJPY` | TRY/JPY のPPP乖離率 = ln(S_TRYJPY / PPP_TRYJPY) |

## 計算式

### Mikan 3-Currency clr Index 座標

```
m_USD = (d_USDJPY + d_USDTRY) / 3
m_JPY = (-2·d_USDJPY + d_USDTRY) / 3
m_TRY = (d_USDJPY - 2·d_USDTRY) / 3
```

### 制約条件

```
m_USD + m_JPY + m_TRY = 0  (常に成立)
```

## 詳細仕様

詳細な算出方法については、`../docs/specification_ppp_annual.md` を参照してください。

---

## 2025年PPP推定値（IMF WEO October 2025）

### 背景

IMF WEOの公式PPPデータは年次公表のため、2025年の確定値は2026年10月頃に発表されます。本データセットでは、**IMF World Economic Outlook (October 2025)** の投影値（projections）を使用しています。

### 採用値

#### JPY (日本円)

**IMF WEO October 2025投影値**: `PPP_JPY = 93.52`

```
過去のPPP推移:
2022: 92.5
2023: 92.84 (+0.34, +0.37%)
2024: 93.2  (+0.36, +0.39%)
2025: 93.52 (+0.32, +0.34%)  ← IMF WEO October 2025

変化率: +0.34% (2024→2025)
```

日本の低インフレ環境を反映し、緩やかな上昇トレンドが継続しています。

#### TRY (トルコリラ)

**IMF WEO October 2025投影値**: `PPP_TRY = 16.51`

```
過去のPPP推移:
2022: 4.975
2023: 8.074  (+3.099, +62.3%)
2024: 12.55  (+4.476, +55.4%)
2025: 16.51  (+3.96,  +31.6%)  ← IMF WEO October 2025

変化率: +31.6% (2024→2025)
```

トルコの高インフレ環境を反映していますが、インフレ率は鈍化傾向にあり、2024年の+55.4%から2025年は+31.6%に低下しています。

### データソース

- **Japan (JPN)**: IMF WEO October 2025, Implied PPP conversion rate
  - Source: https://www.imf.org/external/datamapper/profile/JPN
- **Turkey (TUR)**: IMF WEO October 2025, Implied PPP conversion rate
  - Source: https://www.imf.org/external/datamapper/profile/TUR
  - ICP 2021ベンチマーク基準、インフレ調整済み

### 市場レートとの乖離（参考）

2025年11月時点での為替レート（月平均）と比較:
- **USD/JPY**: 市場レート ≈ 154.34 vs PPP 93.52 → 乖離率 ≈ +50.4% (円安)
- **USD/TRY**: 市場レート ≈ 42.2 vs PPP 16.51 → 乖離率 ≈ +69.6% (リラ安)

### 注意事項

- **これはIMF投影値です** - 2026年10月のIMF WEO確定値（2025年実績）で更新する必要があります
- 月次MCIの2025年データは、このIMF投影PPP値を使用して計算されています
- 確定値公表後、データセット全体の再計算を推奨します

### 更新履歴

- 2025-01: 2025年PPP暫定値を設定（PPP_JPY=93.2, PPP_TRY=16.63）
- 2025-11: IMF WEO October 2025投影値に更新（PPP_JPY=93.52, PPP_TRY=16.51）
- 2026-10予定: IMF WEO確定値で更新
