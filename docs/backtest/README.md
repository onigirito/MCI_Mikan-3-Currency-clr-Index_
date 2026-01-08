# ⚠️ バックテストドキュメント移動のお知らせ / Backtest Documentation Moved

**このフォルダのドキュメントとスクリプトは [`dataset/`](../../dataset/) フォルダに移動しました。**

**The documents and scripts in this folder have been moved to the [`dataset/`](../../dataset/) folder.**

---

## 📂 新しい場所 / New Location

バックテスト関連の全てのドキュメントとスクリプトは、データセットと統合されました：

All backtest-related documents and scripts have been integrated with the dataset:

### ドキュメント / Documentation

- **[統合ドキュメント / Integrated Documentation](../../dataset/README.md)**
  - データ取得からバックテストまで全て記載 / Covers everything from data acquisition to backtesting
  - CSV列の詳細説明を含む / Includes detailed CSV column descriptions
  - IMF API仕様、国コードマッピング / IMF API specifications, country code mapping

- **[バックテスト分析（日本語）/ Backtest Analysis (Japanese)](../../dataset/BACKTEST_ANALYSIS.md)**
  - 包括的な結果分析 / Comprehensive results analysis

- **[バックテスト分析（English）/ Backtest Analysis (English)](../../dataset/BACKTEST_ANALYSIS_EN.md)**
  - 包括的な結果分析 / Comprehensive results analysis

### スクリプトとデータ / Scripts and Data

- **[バックテスト実行 / Backtest Execution](../../dataset/backtest_with_rolling_avg.py)**
  ```bash
  cd dataset
  python backtest_with_rolling_avg.py --comprehensive
  ```

- **[結果分析 / Results Analysis](../../dataset/analyze_rolling_avg_results.py)**
  ```bash
  python analyze_rolling_avg_results.py 2023-08
  ```

- **[月次MCI完全版データ / Monthly MCI Complete Data](../../dataset/monthly_mci_complete_2022_2025.csv)**
  - バックテスト入力データと予測結果を統合（v2.0修正済み、25列）
  - Backtest input data and prediction results integrated (v2.0 corrected, 25 columns)
  - 43カ月分の予測値・誤差を含む / Includes 43 months of predictions and errors

---

## 📊 最新のバックテスト結果 / Latest Backtest Results

**Version:** 2.0 (2026-01-08) - 2022年PPP線形補間修正版 / 2022 PPP interpolation corrected

### 構造安定期（2023-08～2025-11、28カ月）/ Stable Period (Aug 2023 to Nov 2025, 28 months)

| Pair / ペア | MAE | RMSE | Bias / バイアス |
|------------|-----|------|----------------|
| USD/JPY | **2.19%** | 3.23% | +0.03% |
| USD/TRY | **1.44%** | 2.72% | +0.68% |
| TRY/JPY | 3.38% | 4.46% | -0.57% |
| **3ペア平均 / 3-pair average** | **2.34%** | **3.54%** | - |

**評価 / Assessment:** 極めて高い予測精度 / Excellent prediction accuracy

---

## 🔄 移動した理由 / Reason for Moving

バックテストはデータセットと密接に関連しているため、`dataset/`フォルダに統合し、一箇所で管理することにしました。

Since backtesting is closely related to the dataset, we have integrated it into the `dataset/` folder for centralized management.

**利点 / Benefits:**
- データとバックテストの一元管理 / Centralized data and backtest management
- CSV列の説明とバックテスト手法が同じ場所 / CSV column descriptions and backtest methods in one place
- データ取得からバックテストまでの全工程が一つのドキュメントに / Entire process from data acquisition to backtesting in one document

---

**詳細は以下を参照してください / For details, please refer to:**

👉 **[dataset/README.md](../../dataset/README.md)** - 包括的なドキュメント / Comprehensive documentation

---

**Last Updated:** 2026-01-08
