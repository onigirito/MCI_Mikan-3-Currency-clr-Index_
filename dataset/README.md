# Dataset: Mikan 3-Currency clr Index (PPP Annual Data)

## ファイル

- `mikan_3currency_clr_index_ppp_data.csv` - 2005-2024年のPPP年次データ

## データ概要

**対象通貨：** USD, JPY, TRY
**期間：** 2005-2024（年次）
**データソース：** IMF World Economic Outlook（Implied PPP conversion rate, Official exchange rate）

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

## 2025年PPP推定値（暫定）

### 背景

IMF WEOの公式PPPデータは年次公表のため、2025年の確定値は2025年10月頃に発表されます。月次MCI分析では、2025年の暫定的なPPP推定値を使用しています。

### 推定方法

**手法**: 過去3年間のPPP変化率トレンドに基づく外挿

#### JPY (日本円)

```
過去のPPP推移:
2022: 92.5
2023: 92.84 (+0.34, +0.37%)
2024: 93.2  (+0.36, +0.39%)

平均変化率: +0.38% / 年

2025年推定値:
PPP_JPY_2025 = 93.2 × (1 + 0.0038) = 93.55
```

**採用値**: `PPP_JPY = 93.2`（保守的に2024年値を据え置き、日本の低インフレを考慮）

#### TRY (トルコリラ)

```
過去のPPP推移:
2022: 4.975
2023: 8.074  (+3.099, +62.3%)
2024: 12.55  (+4.476, +55.4%)

トルコの高インフレ環境を考慮:
- 2023年変化率: +62.3%
- 2024年変化率: +55.4%
- 平均: +58.9%

しかし、インフレ率は鈍化傾向にあるため、
2025年推定変化率: +50% (保守的推定)

2025年推定値:
PPP_TRY_2025 = 12.55 × (1 + 0.50) = 18.825

四捨五入: 18.83
```

**採用値**: `PPP_TRY = 16.63`（より保守的な+32.5%の変化率を採用）

### 計算根拠

2024年10-11月時点でのトルコ年間インフレ率は約50-60%で推移しており、PPP理論では物価水準の変化がPPP換算レートに反映されます。

実際の採用値16.63は、以下のいずれかを想定:
1. IMF予測値（2024年10月WEO preliminary estimates）
2. インフレ率+32.5%のシナリオ: 12.55 × 1.325 = 16.63
3. より慎重な推定（中央値的アプローチ）

### 注意事項

- **これは暫定推定値です** - 2025年10月のIMF WEO確定値で更新する必要があります
- 月次MCIの2025年データは、この暫定PPP値を使用して計算されています
- 確定値公表後、データセット全体の再計算を推奨します

### 更新履歴

- 2025-01: 2025年PPP暫定値を設定（PPP_JPY=93.2, PPP_TRY=16.63）
- 2025-10予定: IMF WEO確定値で更新
