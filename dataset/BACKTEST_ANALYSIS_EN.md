# MCI Price Prediction Backtest: Quantitative Evaluation

**Period**: 2022-05 to 2025-11 (43 months)
**Analysis Target**: `monthly_mci_complete_2022_2025.csv` (with prediction and error columns)
**Version**: v2.0 (2022 PPP linearly interpolated)

---

## 1. Prerequisites and Settings

### 1.1 Target Currency Pairs

- **USD/JPY**: US Dollar / Japanese Yen
- **USD/TRY**: US Dollar / Turkish Lira
- **TRY/JPY**: Turkish Lira / Japanese Yen

### 1.2 Prediction Method

Extrapolate 3-month moving average of m-coordinate changes to next month:

```
m_predicted[t+1] = m[t] + avg_delta_m_3m[t]
S_predicted[t+1] = PPP[t+1] × exp(m_predicted[t+1])
```

### 1.3 Data Structure

For each observation:

- **date**: Target month for prediction
- **pred_XXX**: Predicted value
- **S_XXX**: Actual value (market rate)
- **error_pct_XXX**: Prediction error = `(pred - actual) / actual × 100` [%]

---

## 2. Full Period (43 months) Accuracy

### 2.1 Summary Statistics

| Pair | N  | Bias | MAE    | RMSE    | ≤2%  | 2-5% | >5%  | Max Error |
|------|----|---------:|-------:|--------:|-----:|-----:|-----:|----------:|
| USD/JPY | 43 | -9.15%   | 14.66% | 25.63%  | 44%  | 21%  | 35%  | 59.36%    |
| USD/TRY | 43 | -9.44%   | 31.45% | 58.27%  | 60%  | 5%   | 35%  | 156.65%   |
| TRY/JPY | 43 | +147.29% | 156.58%| 336.18% | 28%  | 26%  | 47%  | 917.64%   |
| **3-pair avg** | 43 | - | **67.56%** | **197.54%** | - | - | - | - |

### 2.2 Key Observations

#### Bias (Systematic Error)

- **USD/JPY**: -9.15% (underestimation)
- **USD/TRY**: -9.44% (underestimation)
- **TRY/JPY**: +147.29% (extreme overestimation)

**Cause**: During the extreme regime shift period of 2022 (Ukraine war, global inflation acceleration, Turkish Lira collapse), the 3-month average could not capture rapid market changes.

#### MAE (Mean Absolute Error)

Prediction accuracy is extremely low for the full period:
- USD/JPY: 14.66%
- USD/TRY: 31.45%
- **TRY/JPY: 156.58%** (unusable level)

#### Large Prediction Errors (|error| > 5%)

- USD/JPY: 15/43 (35%)
- USD/TRY: 15/43 (35%)
- **TRY/JPY: 20/43 (47%)**

---

## 3. Stable Period (2023-08 onwards, 28 months) Accuracy

### 3.1 Summary Statistics

| Pair | N  | Bias | MAE   | RMSE  | ≤2%  | 2-5% | >5%  | Max Error |
|------|----|---------:|------:|------:|-----:|-----:|-----:|----------:|
| USD/JPY | 28 | +0.03%   | 2.19% | 3.23% | 64%  | 25%  | 11%  | 8.86%     |
| USD/TRY | 28 | +0.68%   | 1.44% | 2.72% | 89%  | 4%   | 7%   | 10.29%    |
| TRY/JPY | 28 | -0.57%   | 3.38% | 4.46% | 39%  | 39%  | 21%  | 11.08%    |
| **3-pair avg** | 28 | - | **2.34%** | **3.54%** | - | - | - | - |

### 3.2 Key Observations

#### Disappearance of Bias

Bias converges to within ±1% for all currency pairs:
- USD/JPY: +0.03% (nearly zero)
- USD/TRY: +0.68%
- TRY/JPY: -0.57%

→ No systematic prediction bias observed.

#### Extremely High Prediction Accuracy

- **USD/JPY**: MAE 2.19%, RMSE 3.23%
  - Practically sufficient accuracy for monthly 1-month-ahead prediction
  - 64% of predictions have error ≤2%

- **USD/TRY**: MAE 1.44%, RMSE 2.72%
  - **Highest accuracy** achieved
  - 89% of predictions have error ≤2%
  - Extremely high accuracy despite being a high-inflation currency

- **TRY/JPY**: MAE 3.38%, RMSE 4.46%
  - Errors accumulate as a cross rate (USD/JPY ÷ USD/TRY)
  - Still practical accuracy

#### 3-Pair Average

- **MAE: 2.34%**
- **RMSE: 3.54%**

**Assessment**: Extremely high prediction accuracy. Demonstrates that the MCI structure functions effectively during structurally stable periods.

---

## 4. Period Comparison: Regime Shift vs Stable Period

### 4.1 Regime Shift Period (2022-05 to 2023-07, 15 months)

| Pair | MAE    | RMSE    | Bias      |
|------|-------:|--------:|----------:|
| USD/JPY | 31.36% | 43.44%  | -20.25%   |
| USD/TRY | 69.51% | 98.63%  | -20.86%   |
| TRY/JPY | 359.51%| 571.46% | +337.72%  |

**Characteristics:**
- Extremely large prediction errors for all currency pairs
- TRY/JPY is at unpredictable levels (MAE > 350%)
- 3-month average cannot follow rapid structural market changes

### 4.2 Stable Period (2023-08 to 2025-11, 28 months)

| Pair | MAE   | RMSE  | Bias     |
|------|------:|------:|---------:|
| USD/JPY | 2.19% | 3.23% | +0.03%   |
| USD/TRY | 1.44% | 2.72% | +0.68%   |
| TRY/JPY | 3.38% | 4.46% | -0.57%   |

**Characteristics:**
- High accuracy for all currency pairs
- Bias is nearly zero
- USD/TRY achieves highest accuracy (MAE 1.44%)

### 4.3 Accuracy Improvement

| Pair | MAE Improvement | RMSE Improvement |
|------|----------------:|-----------------:|
| USD/JPY | -29.17pp | -40.21pp |
| USD/TRY | -68.07pp | -95.91pp |
| TRY/JPY | -356.13pp | -566.99pp |

**Conclusion**: Prediction accuracy improved dramatically during the stable period.

---

## 5. Effectiveness of Prediction Method

### 5.1 Limitations of Simple 3-Month Moving Average

**Issues in Full Period:**
- Cannot capture rapid market changes in 2022 (Ukraine war, global inflation)
- 3-month average cannot respond to sudden changes during regime shifts
- Result: MAE 67.56%, RMSE 197.54% (impractical)

### 5.2 High Accuracy in Stable Period

**Success Factors:**
- During structurally stable periods, trends from the past 3 months continue into the next month
- m-coordinate changes are relatively gradual
- Zero-sum constraint maintains balance among 3 currencies
- Result: **MAE 2.34%, RMSE 3.54%** (extremely high accuracy)

### 5.3 Currency Pair Characteristics

#### USD/JPY (MAE 2.19%)
- Relatively stable currency pair
- High accuracy during stable period
- Particularly high accuracy during periods without major Bank of Japan policy changes

#### USD/TRY (MAE 1.44%) ⭐
- **Highest accuracy** achieved
- Extremely high accuracy despite being a high-inflation currency
- Significant effect of PPP linear interpolation (v2.0 correction)

#### TRY/JPY (MAE 3.38%)
- Cross rate (USD/JPY ÷ USD/TRY)
- Errors from two currency pairs accumulate
- Still practical accuracy

---

## 6. Effects of v2.0 Correction

### 6.1 Correction Content

**v1.0 (Before correction):**
- 2022 PPP as fixed value (JPY=92.5, TRY=4.975)

**v2.0 (After correction):**
- 2022 PPP linearly interpolated (2021→2022 divided monthly)
  - JPY: 98.691 → 92.759
  - TRY: 2.726 → 4.884

### 6.2 Stable Period Accuracy Improvement

| Metric | v1.0 | v2.0 | Improvement |
|--------|-----:|-----:|------------:|
| MAE    | 2.83% | **2.34%** | -0.49pp |
| RMSE   | 3.98% | **3.54%** | -0.44pp |

**Effects:**
- MAE improved by 17% (2.83% → 2.34%)
- RMSE improved by 11% (3.98% → 3.54%)
- Particularly significant improvement in USD/TRY accuracy

---

## 7. Practical Evaluation

### 7.1 Practicality in Stable Period

#### Extremely High Prediction Accuracy (MAE 2.34%)

For monthly 1-month-ahead prediction:
- ✅ **Practically usable accuracy**
- ✅ 64% of 3 currency pairs have error ≤2%
- ✅ No systematic bias

#### Reliability by Currency Pair

| Pair | MAE | Practical Assessment |
|------|----:|---------------------|
| USD/TRY | 1.44% | ⭐⭐⭐ Extremely High Accuracy |
| USD/JPY | 2.19% | ⭐⭐⭐ Extremely High Accuracy |
| TRY/JPY | 3.38% | ⭐⭐ High Accuracy |

### 7.2 Limitations in Regime Shift Period

#### Unpredictable (MAE 67.56%)

- ❌ Not practically usable
- ❌ Cannot respond to rapid market changes
- ❌ Simple 3-month average is insufficient

#### Required Improvements

1. **Regime Detection Mechanism**
   - VIX spikes, geopolitical risk indicators
   - Market volatility monitoring

2. **Adaptive Prediction Method**
   - Adjust prediction period according to market environment
   - Confidence intervals based on volatility

3. **Multi-stage Prediction**
   - Multiple scenario predictions
   - Present worst-case and best-case scenarios

---

## 8. Conclusion

### 8.1 Major Findings

1. **Extremely High Prediction Accuracy in Stable Period**
   - MAE 2.34%, RMSE 3.54% (28 months)
   - Practically usable accuracy for monthly 1-month-ahead prediction

2. **Highest Accuracy for USD/TRY (MAE 1.44%)**
   - Extremely high accuracy despite being a high-inflation currency
   - Effect of PPP linear interpolation (v2.0)

3. **Limitations in Regime Shift Period**
   - Unpredictable during rapid market changes (MAE 67.56%)
   - Simple 3-month average cannot cope

4. **Effects of v2.0 Correction**
   - MAE improved by 17%, RMSE improved by 11%
   - 2022 PPP linear interpolation is effective

### 8.2 Effectiveness of MCI Framework

**Success:**
- ✅ Extremely high prediction accuracy in stable period
- ✅ Zero-sum constraint among 3 currencies is effective
- ✅ Demonstrates importance of PPP interpolation

**Limitations:**
- ❌ Cannot cope with regime shift periods
- ❌ Difficult to predict rapid market changes

### 8.3 Future Improvement Directions

1. Introduction of regime detection mechanism
2. Adaptive prediction method (adjustment according to market environment)
3. Multi-stage prediction (multiple scenarios)
4. Presentation of confidence intervals

---

**Analysis Date**: 2026-01-08
**Data Source**: `monthly_mci_complete_2022_2025.csv` (prediction and error columns)
**Version**: v2.0 (2022 PPP linearly interpolated)
