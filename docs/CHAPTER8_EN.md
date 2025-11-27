# Chapter 8: Monthly Analysis and the Impact of PPP Update Frequency

## 8.1 Significance of Monthly Observations

Chapter 4 analyzed long-term structural changes based on annual data. The 20-year graph reproduced below (Figure 8.0) captures major structural changes: the yen appreciation peak in 2011, the Turkish lira crisis in 2018, and the dollar strength phase in 2022.

![Annual MCI Coordinate Evolution (2005-2024)](annual_mci_plot.png)

*Figure 8.0: Evolution of annual MCI coordinates (reproduced from Chapter 4). While long-term trends over 20 years are discernible, detailed dynamics of recent years are difficult to interpret.*

However, for actual market participants, capturing fluctuations on shorter time horizons is critical. In the above graph, movements since 2022 are compressed, making it insufficient for monthly dynamic analysis. This chapter analyzes short-term dynamics of MCI coordinates using monthly data from 2022 to 2025.

Monthly observations reveal the accumulation and resolution processes of short-term stress that are smoothed out in annual data, structural response speeds to market events, and leading movements that signal regime transitions.

---

## 8.2 Monthly MCI with Annual PPP

The following figure shows monthly MCI coordinates from January 2022 to November 2025. PPP values are the confirmed annual values from IMF WEO.

![Monthly MCI (Annual PPP)](monthly_mci_annual_ppp.png)

*Figure 8.1: Evolution of monthly MCI coordinates using annual PPP. Orange dotted lines indicate year boundaries (PPP update timing).*

### Observed Characteristics

Several important features emerge from this graph.

**1. Discontinuity at Year Boundaries (Axis Shift)**

At the year boundaries marked by orange dotted lines, MCI coordinates jump abruptly. This is not due to rapid exchange rate fluctuations, but rather an apparent change resulting from the annual update of PPP values that serve as the reference for MCI calculation.

Particularly notable are the sharp rises in m[TRY] from approximately -0.75 to -0.45 in January 2023 (+0.30) and from approximately -0.71 to -0.43 in January 2024 (+0.28). These jumps indicate that the "yardstick" used for calculating MCI coordinates changed as the IMF substantially revised PPP reference values to reflect Turkey's high inflation.

**2. Within-Year Dynamics**

Between year boundaries, MCI coordinates transition relatively smoothly. The decline in m[TRY] during the second half of 2022 (-0.6 → -0.75) indicates the accumulation of structural stress that progressed without waiting for PPP updates.

**3. Information Lag**

PPP is inherently a lagging indicator. Official PPP estimates from the IMF and World Bank are published for a given year in subsequent years, may be revised retrospectively, and are calibrated based on large-scale surveys (ICP) conducted every three years. Therefore, when using annual PPP, there is a time lag before actual purchasing power changes are reflected in MCI coordinates.

---

## 8.3 Continuous Evolution through PPP Interpolation

To eliminate discontinuities at year boundaries, we created a version with monthly linear interpolation of PPP.

![Monthly MCI (Interpolated PPP)](monthly_mci_interpolated_ppp.png)

*Figure 8.2: Evolution of MCI coordinates using monthly interpolated PPP. Jumps at year boundaries are eliminated, showing smooth transitions.*

### Interpolation Method

The annual PPP values from IMF WEO represent purchasing power parity as of December of that year. Therefore, monthly interpolation is implemented as linear interpolation from December of the previous year to December of the current year.

```
PPP(year, month) = PPP(year-1) + (PPP(year) - PPP(year-1)) × month / 12
```

Where `PPP(year-1)` is the PPP value for December of the previous year (= confirmed annual PPP value for the previous year), `PPP(year)` is the PPP value for December of the current year (= confirmed or estimated annual PPP value for the current year), and `month` is the current month (1-12).

Interpolation example (2024):
```
2024-01: PPP_JPY = 92.84 + (93.2 - 92.84) × 1/12 = 92.87
2024-06: PPP_JPY = 92.84 + (93.2 - 92.84) × 6/12 = 93.02
2024-12: PPP_JPY = 92.84 + (93.2 - 92.84) × 12/12 = 93.20
```

This interpolation completely eliminates jumps at year boundaries (December → January):
```
2023-12: JPY=92.84, TRY=8.074   (December 2023 value)
2024-01: JPY=92.87, TRY=8.447   (Interpolation toward December 2024 begins)
```

### Characteristics of Monthly MCI Graphs

**1. Trend Clarification**

m[TRY] has risen gradually over approximately three years from around -0.60 (early 2022) to around -0.47 (November 2025). m[JPY] has declined continuously from around +0.19 (early 2022) to around -0.01 (November 2025), while m[USD] has fluctuated in the range of +0.41 to +0.60, standing at +0.49 as of November 2025.

**2. Visualization of Short-term Stress**

Short-term stress events are clearly observable, such as the bottoming out of m[TRY] (around -0.77) before and after Şimşek's appointment in June 2023.

**3. Relationship between Stress and Currency Depreciation: Structural Transition in the Turkish Lira**

While the lira has consistently depreciated in the dollar/lira exchange rate, the MCI graph shows m[TRY] converging toward zero. This apparently contradictory movement can be explained by understanding what MCI represents.

MCI reflects not "price movements" but rather "the nature of structural stress." Taking the yen as an example, m[JPY] is currently near zero, but this does not mean the deviation rate from PPP is zero. In fact, the yen remains undervalued in PPP comparisons. Zero in MCI indicates "a structurally balanced position within the basket."

**Period of Structural Stress Accumulation for the Lira (First Half of 2022 to July 2023)**

According to monthly data, m[TRY] deteriorated continuously from -0.595 in January 2022, bottoming at -0.766 in July 2023.

- January to December 2022: -0.595 → -0.755 (deterioration of approximately -0.16). Unorthodox monetary policy continued under the Erdoğan administration. Adherence to low interest rates amid high inflation and currency interventions went against market mechanisms, and attempts to artificially support the currency accumulated structural stress.

- January to May 2023: -0.738 → -0.637 (temporary rising trend). However, no structural policy shift occurred, and deterioration resumed after June.

- June to July 2023: -0.715 → -0.766 (sharp deterioration, bottoming). Finance Minister Şimşek assumed office on June 3, 2023. Immediately after his appointment, markets faced uncertainty about policy shifts, with m[TRY] falling to -0.715 in June and reaching a minimum of -0.766 in July. This can be interpreted as temporary stress maximization during the transition period of policy change.

**Structural Transition and Formation of Convergence Trend (August 2023 onward)**

A clear convergence trend formed after August 2023. From August to December 2023: -0.744 → -0.711 (rise begins), throughout 2024: -0.696 → -0.517 (substantial rise), January to November 2025: -0.503 → -0.472 (continuous rise).

As policy interest rates were normalized to match inflation rates under Finance Minister Şimşek, the nature of lira depreciation changed from "artificial maintenance against the market" to "natural adjustment commensurate with inflation." While prices continue to decline, the decline now reflects economic realities, structural stress has been resolved, and the MCI shows a clear convergence trend.

Over approximately two and a half years from the bottom (July 2023), m[TRY] has risen approximately 0.29 points from -0.766 to -0.472, showing a stable convergence rate of approximately 0.12 points annually. This reflects policy consistency and recovery of market confidence.

---

## 8.4 Monthly MCI as a Leading Indicator

Analysis of monthly data suggests the nature of MCI as a leading indicator.

### Leading Nature of Structural Improvement

In the monthly MCI graph, m[TRY] has shown a gradual upward trend since the second half of 2023. This reflects convergence pressure toward PPP (extreme undervaluation is unsustainable and will adjust in some form), resolution of structural stress (inflation rate decline and normalization of monetary policy are progressing), and lag in reflection to market prices (there is a time lag before structural improvements are reflected in prices).

The convergence trend of MCI can potentially be interpreted as a sign of future currency stabilization. However, this does not predict "convergence timing" but rather indicates "structural pressure toward convergence direction."

### Limitations

Since PPP itself is a lagging indicator, complete leading nature cannot be expected. It cannot respond to sudden changes due to policy shifts or geopolitical events, and even monthly data smooths out daily and weekly short-term fluctuations.

---

## 8.5 Estimation of Future Price Ranges Using Monthly MCI

### Boundedness of the Range of Motion and Possibility of Statistical Estimation

An important mathematical property of the Mikan 3-Currency clr Index is the boundedness of the range of motion. Since actual exchange rates can theoretically fluctuate in the range of $0 \to \infty$, directly inferring future fluctuation ranges is difficult. However, $m[i]$ coordinates are mapped into a mathematically constrained space due to the zero-sum constraint (Equation (1)).

The observed ranges of $m[i]$ in monthly interpolated data (January 2022 to November 2025, 47 months) are as follows.

| Currency | Minimum | Maximum | Range Width |
|----------|---------|---------|-------------|
| USD | +0.406 | +0.597 | 0.191 |
| JPY | -0.015 | +0.197 | 0.212 |
| TRY | -0.766 | -0.472 | 0.294 |

This observed range is more limited compared to the range of approximately $\pm 0.8$ observed in annual data (20 years). Fluctuations in monthly interpolated data are gentle as follows.

| Currency | Max Monthly Rise | Timing | Max Monthly Fall | Timing | Avg Monthly Change |
|----------|------------------|--------|------------------|--------|--------------------|
| USD | +0.058 | June 2023 | -0.029 | August 2024 | 0.011 |
| JPY | +0.047 | August 2024 | -0.039 | April 2022 | 0.017 |
| TRY | +0.036 | February 2023 | -0.077 | June 2023 | 0.019 |

Notable timings:

- **TRY maximum fall (June 2023, -0.077)**: Month of Finance Minister Şimşek's appointment. Reflects maximization of structural stress during policy transition period.
- **JPY maximum fall (April 2022, -0.039)**: US long-term interest rates surged (2.4%→3.0%) following FOMC's QT acceleration agreement and CPI 8.5% announcement. Period when yen depreciation pressure arose from rapid widening of US-Japan interest rate differential.
- **JPY maximum rise (August 2024, +0.047)**: Corresponds to Bank of Japan's monetary policy transition period.
- **USD maximum rise (June 2023, +0.058)**: Relative rise within the basket accompanying TRY's sharp fall (result of zero-sum constraint).

This boundedness suggests the possibility of calculating the theoretical short-term range of motion for $m[i]$ using statistical methods.

### Setting Target Prices through Back-Calculation

By making assumptions about future values of $m[i]$, future exchange rates can be estimated using the following back-calculation formula.

$$
S_{\text{A/B,future}} = \text{PPP}_{\text{A/B,future}} \times \exp(m[A]_{\text{target}} - m[B]_{\text{target}})
$$

Where $\text{PPP}_{\text{future}}$ can be estimated from inflation rate forecasts for each country, and $m[i]_{\text{target}}$ is set from extrapolation of current trends or statistical ranges. This method enables estimation of future price ranges based on statistical evidence, going beyond mere ex-post evaluation.

### Practical Example: USD/JPY Price Range Estimation for December 2025

**Current Situation Assessment (as of November 2025)**

The latest MCI coordinates using monthly interpolated PPP (November 2025) are $m[\text{USD}] = +0.487$ (maintaining overvaluation), $m[\text{JPY}] = -0.015$ (nearly neutral), $m[\text{TRY}] = -0.472$ (undervalued).

**Trend Analysis**

Trends observed from monthly data since 2023 are as follows. USD has declined gradually from a peak of +0.597 in 2023 to +0.487 as of November 2025. JPY has declined continuously from +0.197 in 2022 to nearly neutral (-0.015) as of November 2025. TRY has been on an upward trend from the bottom of -0.766 in July 2023 to -0.472 as of November 2025.

**Scenario Setting**

Based on November 2025 observed values (USD: +0.487, JPY: -0.015, TRY: -0.472), we extrapolate observed statistical trends to December 2025.

| Scenario | m[USD] | m[JPY] | m[TRY] | Rationale |
|----------|--------|--------|--------|-----------|
| A (Inertia) | +0.485 | -0.025 | -0.460 | Continuation of JPY decline and TRY convergence trends |
| B (Slightly Stronger Yen) | +0.478 | 0.000 | -0.478 | JPY approaches zero, USD declines in linkage at statistical ratio (approx. 60%) |
| C (Slightly Weaker Yen) | +0.480 | -0.020 | -0.460 | JPY decline continues, TRY convergence continues |

**Estimated Ranges for December 2025**

Results calculated using estimated PPP values (JPY: 93.52, TRY: 16.51) and m values for each scenario are as follows.

| Currency Pair | Central Scenario | Risk Range |
|---------------|------------------|------------|
| **USD/JPY** | **¥151–156** | **¥147–162** |
| **USD/TRY** | **₺42.3–43.0** | **₺40.4–44.7** |
| **TRY/JPY** | **¥3.51–3.67** | **¥3.28–4.01** |

The central scenario is the range derived from the three scenarios, and the risk range is a statistical fluctuation range considering past monthly fluctuations (±0.05).

This fluctuation range of ±0.05 is comparable in magnitude to the largest events during the observation period—FOMC's QT acceleration in April 2022 (JPY monthly fluctuation -0.039) and the Bank of Japan's policy transition in August 2024 (JPY monthly fluctuation +0.047). In other words, it indicates levels that could be reached if regime-change-level structural changes occur.

December 2025 is a period when the possibility of additional interest rate cuts by the US Federal Reserve is being discussed in markets, and if the decision's content or magnitude significantly deviates from market expectations, fluctuations equivalent to the risk range may materialize.

---

## 8.6 Summary of This Chapter

This chapter revealed short-term structural dynamics that cannot be captured with annual data through MCI analysis using monthly data.

By constructing datasets suitable for analysis through monthly linear interpolation of PPP, regime transition events and MCI coordinate trends could be clearly visualized. Major events during the observation period concentrated at turning points of monetary policy, including Finance Minister Şimşek's appointment (June 2023), FOMC's QT acceleration (April 2022), and the Bank of Japan's monetary policy transition (August 2024).

The structural transition of the Turkish lira was captured in detail. m[TRY] bottomed at -0.766 in July 2023 and rose to -0.472 over approximately two and a half years thereafter. This indicates that under Finance Minister Şimşek, policy interest rate normalization to match inflation rates changed the nature of lira depreciation from "artificial maintenance against the market" to "natural adjustment commensurate with inflation." While prices continue to decline, structural stress has been resolved.

As a mathematical property of MCI, the boundedness of the range of motion is important. While actual exchange rates can theoretically fluctuate in an infinite range, m[i] coordinates are mapped into a space constrained by the zero-sum constraint. This boundedness enables estimation of future price ranges using statistical methods.

In the practical example for December 2025, we derived a central scenario of ¥151–156 and a risk range of ¥147–162 for USD/JPY from three scenarios. The risk range assumes fluctuation ranges comparable to past major events (FOMC's QT acceleration, Bank of Japan policy transition), indicating levels that could be reached if regime-change-level structural changes occur.

The monthly analysis presented in this chapter complements the practical operational guidelines presented in Chapter 7 on a shorter time horizon. By combining long-term structural understanding through annual data with short-term dynamic tracking through monthly data, the practical utility of the Mikan 3-Currency clr Index is further enhanced.

---
