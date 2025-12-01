---
layout: default
title: "MCI Backtest Quantitative Evaluation (English)"
description: "Comprehensive quantitative analysis of MCI backtest results (2022-03 to 2025-11, 45 observations)"
lang: en
---

# MCI Price Prediction Backtest: Quantitative Evaluation

**Period**: 2022-03 to 2025-11 (45 observations)
**Analysis Target**: `backtest_rolling_avg_results.csv`

---

## 1. Prerequisites and Settings

### 1.1 Target Currency Pairs

- **USDJPY**: US Dollar / Japanese Yen
- **USDTRY**: US Dollar / Turkish Lira
- **TRYJPY**: Turkish Lira / Japanese Yen

### 1.2 Data Structure

The following variables are recorded for each observation:

- **base_month (N)**: Final month used for prediction
- **target_month (N+1)**: Target month for 1-month-ahead prediction
- **pred_XXX**: Predicted value
- **actual_XXX**: Actual value
- **error_pct_XXX**: Prediction error rate = (pred/actual - 1) × 100 [%]
- **avg_delta_m_USD, JPY, TRY**: Simple average of m-coordinate changes over the most recent 3 months

### 1.3 Zero-Sum Constraint of m-Coordinates

The m-coordinates are calculated based on CoDA/CLR (Compositional Data Analysis / Centered Log-Ratio) premises, and the following holds for each observation:

```
avg_delta_m_USD + avg_delta_m_JPY + avg_delta_m_TRY ≈ 0
```

Observed value: Maximum deviation ≈ 2.0×10⁻¹⁶ (within numerical error range)

---

## 2. Full Period (45 Months) Accuracy

### 2.1 Summary Statistics

| Pair    | N  | Mean Error | MAE   | RMSE  | Error≦2% | 2-5%  | >5%  | Max Error |
|---------|----|-----------:|------:|------:|---------:|------:|-----:|----------:|
| USDJPY  | 45 | +0.00%     | 2.42% | 3.32% | 53%      | 33%   | 13%  | 8.86%     |
| USDTRY  | 45 | +0.17%     | 2.23% | 3.65% | 67%      | 22%   | 11%  | 15.15%    |
| TRYJPY  | 45 | -0.03%     | 3.84% | 4.97% | 36%      | 38%   | 27%  | 14.00%    |

### 2.2 Key Observations

#### Bias

Mean errors across all currency pairs are within ±0.2%, indicating no systematic prediction bias.

#### MAE (Mean Absolute Error)

- **USDJPY / USDTRY**: 2.2-2.4%
  - Practically acceptable level for monthly 1-month-ahead predictions

- **TRYJPY**: 3.8%
  - Larger error than the two USD pairs (due to structural factors discussed later)

#### Large Prediction Errors (|error| > 5%)

- USDJPY: 6/45 (13%)
- USDTRY: 5/45 (11%)
- TRYJPY: 12/45 (27%)

These large errors are concentrated in specific months (see Chapter 3), suggesting structural rather than random factors.

---

## 3. Regime Transitions and Error Concentration

### 3.1 Identification of Regime Transition Months

The following periods are identified as "regime transition months":

#### Turkish Policy/Election Shock
- 2023-06, 2023-07, 2023-08, 2023-09 (4 months)

#### JPY Interest Rate Regime Transition
- 2024-08, 2024-10 (2 months)

**Total**: 6 months analyzed as regime transition periods

### 3.2 Accuracy During Regime Transitions

#### Regime Transition Months Only (6 months)

| Pair    | N | Mean Error | MAE   | RMSE   | Error≦2% | 2-5%  | >5%  | Max Error |
|---------|---|-----------:|------:|-------:|---------:|------:|-----:|----------:|
| USDJPY  | 6 | -0.01%     | 3.87% | 5.00%  | 33%      | 33%   | 33%  | 8.86%     |
| USDTRY  | 6 | -0.37%     | 6.89% | 8.52%  | 33%      | 17%   | 50%  | 15.15%    |
| TRYJPY  | 6 | -0.11%     | 9.73% | 10.07% | 0%       | 33%   | 67%  | 14.00%    |

**Observations**:
- Prediction errors significantly expand for USDTRY and TRYJPY
- During the 4 months of Turkish shock + 2 months of JPY rate transition, extrapolation of the 3-month average Δm fails to capture market fluctuations

#### Excluding Regime Transition Months (39 months)

| Pair    | N  | Mean Error | MAE   | RMSE  | Error≦2% | 2-5%  | >5%  | Max Error |
|---------|----|-----------:|------:|------:|---------:|------:|-----:|----------:|
| USDJPY  | 39 | +0.00%     | 2.20% | 2.97% | 56%      | 33%   | 10%  | 7.71%     |
| USDTRY  | 39 | +0.25%     | 1.51% | 2.05% | 72%      | 23%   | 5%   | 6.02%     |
| TRYJPY  | 39 | -0.20%     | 2.95% | 3.67% | 41%      | 44%   | 15%  | 8.76%     |

### 3.3 Insights from Regime Analysis

1. **Normal Period Accuracy**
   - USDTRY: MAE ≈ 1.5% (significant accuracy improvement)
   - USDJPY: MAE ≈ 2.2% (improved from full period average)
   - TRYJPY: MAE 3.84% → 2.95% (improved but still larger than other pairs)

2. **Primary Model Limitation**

   The main weakness of this model is **not the MCI structure itself**, but rather the scenario setting of "directly extrapolating the most recent 3 months' Δm" being **non-adaptive to regime transitions**.

   During regime-stable periods, especially for USDTRY, high prediction accuracy confirms the validity of the MCI structure itself.

---

## 4. Zero-Sum Constraint Verification

### 4.1 Theoretical Requirement

The change in m-coordinates (Δm) must satisfy the zero-sum constraint:

```
Δm_USD + Δm_JPY + Δm_TRY = 0
```

### 4.2 Empirical Verification

For `avg_delta_m_USD + avg_delta_m_JPY + avg_delta_m_TRY` in each observation:

- **Mean**: 5.9×10⁻¹⁸
- **Standard Deviation**: 8.4×10⁻¹⁷
- **Maximum Absolute Value**: 2.0×10⁻¹⁶

### 4.3 Conclusion

These values are more than 10 orders of magnitude smaller than typical numerical tolerance (e.g., 10⁻⁴), indicating that the zero-sum constraint is **numerically satisfied with strict precision**.

Therefore:
- The 3-month average of m-coordinate differences (Δm) maintains the zero-sum numerically
- The predicted m constructed by adding this to m_N also maintains the zero-sum
- **The possibility that zero-sum breakdown in predicted m is a source of error is excluded**

---

## 5. Structural Analysis of TRYJPY Error

### 5.1 Composite Error Structure

Verification of the relationship between TRYJPY error and errors in the two USD pairs:

```
error_pct_TRYJPY ≈ error_pct_USDJPY - error_pct_USDTRY
```

**Empirical Correlation**:
- Correlation coefficient: **0.998**
- Mean absolute difference: **0.15%**
- Maximum deviation: approximately 2.1%

**Interpretation**:
TRYJPY error is almost completely described as "USDJPY error - USDTRY error". That is, when errors in the two USD pairs are each around 2-3%, in months where the signs do not align, the difference manifests as TRYJPY error.

### 5.2 Level Effect

TRYJPY fluctuates around 3-4 yen, and even fluctuations of 0.1-0.2 yen result in error rates of approximately 3-6% on a 3.5 yen basis.

Even with the same m-coordinate fluctuation, **currency pairs with smaller levels show larger percentage errors**, creating a display bias.

### 5.3 Factors in TRYJPY Error

The observed MAE of 3.84% (2.95% after regime exclusion) is a composite result of three factors:

1. **Differential Structure**: Composition of errors from two USD pairs
2. **Low Level Effect**: Magnification of percentage display at small nominal values
3. **Regime Impact**: Susceptibility to shocks from both Turkey and JPY

---

## 6. Summary

### 6.1 Basic Accuracy Over Full Period

- **USDJPY / USDTRY**: MAE 2.2-2.4%
- **TRYJPY**: MAE 3.8%
- **Bias**: Within ±0.2% for all pairs (virtually unbiased)

### 6.2 Impact of Regime Transitions

During Turkish regime (2023-06-09) and JPY rate regime (2024-08, 10), MAE for USDTRY and TRYJPY expanded to 7-10%.

Excluding regime transition months:
- **USDTRY**: MAE ≈ 1.5%
- **USDJPY**: MAE ≈ 2.2%
- **TRYJPY**: MAE ≈ 3.0%

During normal periods, particularly high prediction accuracy is demonstrated for USDTRY.

### 6.3 Structural Consistency

The zero-sum constraint of m-coordinates is numerically satisfied with strict precision (deviation < 10⁻¹⁵), and errors are **attributed to fixed scenario settings** rather than breakdown of the m-structure.

### 6.4 Nature of TRYJPY Error

Structural magnification due to error differential of two USD pairs + low level effect + dual regime impact, not an independent prediction error.

### 6.5 Main Conclusion

**The primary limitation of this model is not the MCI structure itself, but rather that the scenario setting of "extrapolating the most recent 3 months' Δm" is non-adaptive to regime transitions.**

High accuracy during regime-stable periods (especially USDTRY MAE 1.5%) demonstrates the validity of the MCI structure. Future improvement directions include introducing regime detection mechanisms and adaptive scenario generation.

---

**Analysis Date**: 2025-12-01
**Data Source**: `backtest_rolling_avg_results.csv`
