# IMF WEO PPP予測値取得指示書（AI Agent用）

## タスク概要
IMF World Economic Outlook (October 2025) から、日本とトルコの**Implied PPP conversion rate (PPPEX)** の2026-2030年の予測値を取得してください。

## 対象データ

### 取得すべき指標
- **指標名**: Implied PPP conversion rate
- **指標コード**: PPPEX
- **単位**: National currency per current international dollar

### 対象国
1. **Japan (JPN)**
   - 既知値: 2025年 = 93.52
   - 必要: 2026, 2027, 2028, 2029, 2030

2. **Turkey (TUR)**
   - 既知値: 2025年 = 16.51
   - 必要: 2026, 2027, 2028, 2029, 2030

### データソース
- **IMF World Economic Outlook (October 2025)**
- URL: https://www.imf.org/external/datamapper/PPPEX@WEO

## 実行手順

### ステップ1: データアクセス

以下のURLにアクセスして、インタラクティブデータマッパーから情報を取得してください：

```
https://www.imf.org/external/datamapper/PPPEX@WEO
```

または、IMF Data Portalを使用：

```
https://data.imf.org/en/datasets/IMF.RES:WEO
```

### ステップ2: 日本（JPN）のデータ取得

1. 国選択: Japan (JPN)
2. 指標: PPPEX (Implied PPP conversion rate)
3. 年範囲: 2020-2030 (特に2026-2030に注目)
4. 以下の値を取得:
   - PPP_JPY_2026 = ?
   - PPP_JPY_2027 = ?
   - PPP_JPY_2028 = ?
   - PPP_JPY_2029 = ?
   - PPP_JPY_2030 = ?

### ステップ3: トルコ（TUR）のデータ取得

1. 国選択: Turkey (TUR)
2. 指標: PPPEX (Implied PPP conversion rate)
3. 年範囲: 2020-2030 (特に2026-2030に注目)
4. 以下の値を取得:
   - PPP_TRY_2026 = ?
   - PPP_TRY_2027 = ?
   - PPP_TRY_2028 = ?
   - PPP_TRY_2029 = ?
   - PPP_TRY_2030 = ?

### ステップ4: 結果の報告

以下のフォーマットで報告してください：

```
## IMF WEO October 2025 - Implied PPP Conversion Rate (PPPEX)

### Japan (JPN)
| Year | PPP_JPY | YoY Change | YoY % |
|------|---------|------------|-------|
| 2025 | 93.52   | (baseline) | -     |
| 2026 | [値]    | [差分]     | [%]   |
| 2027 | [値]    | [差分]     | [%]   |
| 2028 | [値]    | [差分]     | [%]   |
| 2029 | [値]    | [差分]     | [%]   |
| 2030 | [値]    | [差分]     | [%]   |

### Turkey (TUR)
| Year | PPP_TRY | YoY Change | YoY % |
|------|---------|------------|-------|
| 2025 | 16.51   | (baseline) | -     |
| 2026 | [値]    | [差分]     | [%]   |
| 2027 | [値]    | [差分]     | [%]   |
| 2028 | [値]    | [差分]     | [%]   |
| 2029 | [値]    | [差分]     | [%]   |
| 2030 | [値]    | [差分]     | [%]   |
```

## 重要な確認事項

1. **データの存在確認**: 2026-2030年の予測値が実際に公開されているか確認してください
2. **データの種別**: "Estimates"（推定値）なのか"Projections"（予測値）なのか明記してください
3. **データ更新日**: IMF WEO October 2025であることを確認してください
4. **予測期間**: もし2026-2030年のデータがない場合、何年まで利用可能か報告してください

## 代替アクセス方法

もし上記URLでデータが取得できない場合、以下の方法を試してください：

### 方法A: IMF WEO Database Download
```
https://www.imf.org/en/Publications/WEO/weo-database/2025/October
```
→ "Download WEO Data" → Country: JPN, TUR / Indicator: PPPEX

### 方法B: Direct Country Profiles
- Japan: https://www.imf.org/external/datamapper/profile/JPN
- Turkey: https://www.imf.org/external/datamapper/profile/TUR

### 方法C: IMF WEO Statistical Appendix
```
https://www.imf.org/-/media/Files/Publications/WEO/2025/October/English/statsappendix.ashx
```
→ PDFから該当テーブルを探す（Table形式でPPPEXを含むもの）

## トラブルシューティング

### Q1: 2026-2030年のデータが見つからない
A: IMF WEOは通常5年先まで予測を提供していますが、指標によって異なります。利用可能な最新年を報告してください。

### Q2: データマッパーでインタラクティブな操作が必要
A: WebブラウザのDeveloper Toolsを使ってAPI呼び出しを確認するか、データベースのダウンロード機能を使用してください。

### Q3: TurkeyとTürkiyeの表記
A: IMFデータベースでは "Turkey" または "Türkiye" の両方の表記が使われている可能性があります。両方試してください。

## 期待される成果物

1. **2026-2030年の各年のPPP値（JPYとTRY）**
2. **データソースの確認（IMF WEO October 2025であること）**
3. **予測値の妥当性チェック**:
   - 日本: 年率+0.3-0.4%程度の緩やかな上昇トレンド
   - トルコ: 高インフレだが鈍化傾向（2025年は+31.6%）

## 出力形式

最終的に、以下のCSV形式でも出力してください：

```csv
country,year,PPP_value,yoy_change,yoy_pct,data_source
Japan,2025,93.52,,,IMF WEO Oct 2025
Japan,2026,[値],[差分],[%],IMF WEO Oct 2025
Japan,2027,[値],[差分],[%],IMF WEO Oct 2025
Japan,2028,[値],[差分],[%],IMF WEO Oct 2025
Japan,2029,[値],[差分],[%],IMF WEO Oct 2025
Japan,2030,[値],[差分],[%],IMF WEO Oct 2025
Turkey,2025,16.51,,,IMF WEO Oct 2025
Turkey,2026,[値],[差分],[%],IMF WEO Oct 2025
Turkey,2027,[値],[差分],[%],IMF WEO Oct 2025
Turkey,2028,[値],[差分],[%],IMF WEO Oct 2025
Turkey,2029,[値],[差分],[%],IMF WEO Oct 2025
Turkey,2030,[値],[差分],[%],IMF WEO Oct 2025
```

---

## このタスクの背景

このデータは **Mikan 3-Currency clr Index** プロジェクトで、USD/JPY/TRYの3通貨間の購買力平価乖離率を分析するために使用されます。予測値があれば、将来の月次MCI計算に活用できます。

## 実行者へのメッセージ

このタスクは、IMFの公開データベースから情報を取得するものです。Webスクレイピング機能やAPI呼び出し機能を持つAIエージェント（Grok, GPT with browsing, Perplexity等）であれば実行可能なはずです。

取得できた情報を上記フォーマットで報告してください。もしデータが存在しない場合は、その旨を明確に報告してください。

Good luck! 🚀
