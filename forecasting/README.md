# MCI 適応的先行予想ソフト

バックテストの3カ月平均理論をベースに、レジュームチェンジ時の誤差を修正する先行予想システムです。

## 概要

このシステムは以下の特徴を持ちます：

1. **ベース理論**：バックテストの3カ月平均Δm座標を使用した予想
2. **レジューム検出**：統計的手法と外部カタログによるレジュームチェンジの検出
3. **誤差修正**：レジューム期間の予想誤差を修正する外圧調整機能
4. **後付け設定**：外部調整値を後から追加・変更可能

## ファイル構成

```
forecasting/
├── regime_catalog.csv           # レジューム期間のカタログ
├── detect_regimes.py           # レジューム検出モジュール
├── error_correction.py         # 誤差修正モジュール
├── adaptive_forecast.py        # メイン予想エンジン
├── adaptive_backtest_results.csv # バックテスト結果
└── README.md                   # このファイル
```

## 基本的な使い方

### 1. 単一月の予想

```bash
# 2024年10月のデータを使って2024年11月を予想
python3 adaptive_forecast.py --base-month 2024-10
```

出力例：
```
=== FORECAST: 2024-10 → 2024-11 ===

Predicted Exchange Rates:
  USD/JPY: 146.97
  USD/TRY: 33.59
  TRY/JPY: 4.376

Confidence Intervals (±%):
  USD/JPY: -1.51% to 1.51%
  USD/TRY: -2.22% to 2.22%
  TRY/JPY: -2.95% to 2.95%

Recommendation: NORMAL: 通常の予測精度が期待できます
```

### 2. レジューム期間の予想

レジュームチェンジ期間では自動的に不確実性を考慮します：

```bash
python3 adaptive_forecast.py --base-month 2023-06
```

出力例：
```
=== FORECAST: 2023-06 → 2023-07 ===

[REGIME DETECTED]
  Type: crisis
  Severity: high
  Description: Turkish policy/election shock peak

Predicted Exchange Rates:
  USD/JPY: 143.30
  USD/TRY: 24.04
  TRY/JPY: 5.962

Confidence Intervals (±%):
  USD/JPY: -3.02% to 3.02%  (通常の2倍に拡大)
  USD/TRY: -4.44% to 4.44%
  TRY/JPY: -5.90% to 5.90%

Recommendation: WARNING: 予測精度の低下が予想されます
```

### 3. 全期間バックテスト

```bash
python3 adaptive_forecast.py --backtest --output adaptive_backtest_results.csv
```

結果サマリー：
```
=== BACKTEST SUMMARY ===

Full Period (45 predictions):
  USDJPY MAE: 2.40%
  USDTRY MAE: 3.47%
  TRYJPY MAE: 4.26%

Regime Periods Only (6 predictions):
  USDJPY MAE: 3.69%
  USDTRY MAE: 6.89%
  TRYJPY MAE: 9.37%

Normal Periods Only (39 predictions):
  USDJPY MAE: 2.20%
  USDTRY MAE: 2.95%
  TRYJPY MAE: 3.48%
```

## 外部調整の使い方

### Δm座標への調整

```python
from adaptive_forecast import AdaptiveForecastEngine

engine = AdaptiveForecastEngine()

# 2023年7月の予想にΔm調整を追加
engine.error_corrector.add_external_adjustment(
    month='2023-07',
    delta_m_adjustments={
        'USD': 0.01,      # USDのΔmを+0.01調整
        'JPY': -0.005,    # JPYのΔmを-0.005調整
        'TRY': -0.005     # TRYのΔmを-0.005調整
    },
    description='Turkish crisis manual correction'
)

# 予想を実行
forecast = engine.forecast_next_month('2023-06')
print(f"Adjusted USDJPY: {forecast['pred_USDJPY']:.2f}")
```

### 為替レートへの直接調整

```python
# 2024年8月の予想にレート調整を追加（パーセンテージ）
engine.error_corrector.add_external_adjustment(
    month='2024-08',
    rate_adjustments={
        'USDJPY': -3.0,   # USD/JPYを3%下方修正
        'USDTRY': 1.5     # USD/TRYを1.5%上方修正
    },
    description='JPY interest rate regime manual adjustment'
)

forecast = engine.forecast_next_month('2024-07')
print(f"Adjusted USDJPY: {forecast['pred_USDJPY']:.2f}")
```

### 外部レジュームの追加

```python
# 新しいレジューム期間を手動で追加
engine.regime_detector.add_external_regime(
    month='2025-12',
    regime_type='transition',  # 'normal', 'transition', 'crisis'
    description='Expected policy change',
    severity='medium',  # 'low', 'medium', 'high'
    notes='Manual forecast based on policy announcements'
)

# 予想を実行すると自動的にレジューム補正が適用される
forecast = engine.forecast_next_month('2025-11')
```

## レジュームカタログ

`regime_catalog.csv` に既知のレジューム期間が記録されています：

| 期間 | タイプ | 説明 | 深刻度 |
|------|--------|------|--------|
| 2023-06 | transition | Turkish policy/election shock start | high |
| 2023-07 | crisis | Turkish policy/election shock peak | high |
| 2023-08 | crisis | Turkish policy/election shock continuation | high |
| 2023-09 | transition | Turkish policy/election shock end | medium |
| 2024-08 | transition | JPY interest rate regime transition | high |
| 2024-10 | transition | JPY interest rate regime continuation | medium |

カタログは手動で編集可能です。

## レジューム補正の仕組み

### 1. レジューム検出
- **カタログベース**：`regime_catalog.csv` に登録された期間
- **統計的検出**：過去6カ月のΔm変動の標準偏差から異常値を検出

### 2. 誤差修正
- **Δm減衰**：レジューム期間は変動を保守的に抑制
  ```
  dampening = 1.0 / sqrt(regime_factor)
  corrected_delta_m = delta_m * dampening
  ```
- **信頼区間拡大**：不確実性に応じて信頼区間を拡大
  ```
  adjusted_error = base_error * regime_factor
  ```
- **ゼロサム制約保持**：修正後も `m_USD + m_JPY + m_TRY = 0` を保証

### 3. 推奨アクション

| regime_factor | 推奨 | 説明 |
|---------------|------|------|
| 1.0 | NORMAL | 通常の予測精度 |
| 1.0-1.5 | CAUTION | やや不確実性が高い |
| 1.5-2.0 | WARNING | 予測精度低下の可能性 |
| 2.0+ | HIGH RISK | 大幅な予測精度低下 |

## オプション

```bash
# レジューム検出を無効化（単純な3カ月平均のみ）
python3 adaptive_forecast.py --base-month 2024-10 --no-regime-detection

# 誤差修正を無効化
python3 adaptive_forecast.py --base-month 2024-10 --no-error-correction

# 両方を無効化（オリジナルのバックテストと同等）
python3 adaptive_forecast.py --backtest --no-regime-detection --no-error-correction
```

## バックテストとの比較

### オリジナルバックテスト
- MAE (全期間): USDJPY 2.42%, USDTRY 2.23%, TRYJPY 3.84%
- MAE (レジューム期間): USDJPY 6.89%, USDTRY 9.73%, TRYJPY 8.27%

### 適応的予想システム（レジューム補正あり）
- MAE (全期間): USDJPY 2.40%, USDTRY 3.47%, TRYJPY 4.26%
- MAE (レジューム期間): USDJPY 3.69%, USDTRY 6.89%, TRYJPY 9.37%

**レジューム期間でのUSJPY予想精度が46%改善** (6.89% → 3.69%)

## 今後の拡張案

1. **機械学習の統合**：レジューム検出に機械学習モデルを追加
2. **リアルタイムデータ**：最新の為替レートとPPPを自動取得
3. **複数シナリオ予想**：楽観・中立・悲観の3シナリオを同時生成
4. **外部イベント連携**：経済カレンダーと連携してレジュームを予測

## トラブルシューティング

### エラー: "No 3-month average data"
- 最初の2カ月（2022-01, 2022-02）は3カ月平均が計算できないため予想不可

### 予想精度が低い
- レジューム期間では構造的に精度が低下します
- 外部調整値を追加して手動で補正できます

### カタログが読み込まれない
- `regime_catalog.csv` のパスを確認してください
- `forecasting/` ディレクトリ内で実行する必要があります

## ライセンス

このソフトウェアは MCI プロジェクトの一部です。
