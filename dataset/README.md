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
