# Purchasing Power Parity Analysis Based on the Mikan 3-Currency clr Index

**Subtitle**: Construction and Time-Series Analysis of a Relative Evaluation Index Using clr Transformation for USD, JPY, and TRY

**Author**: Yukihiro Honda

**Date**: November 22, 2025

---

## Abstract

This paper proposes a novel relative evaluation index called the "Mikan 3-Currency clr Index" for three currencies—US Dollar (USD), Japanese Yen (JPY), and Turkish Lira (TRY)—based on Purchasing Power Parity (PPP) theory. By applying an approach analogous to the centered log-ratio (clr) transformation from Compositional Data Analysis (CoDA), this index expresses PPP deviations in an orthogonalized form, providing a balanced quantification of the "overvaluation/undervaluation" of each currency. Empirical analysis using 20 years of data (2005–2024) demonstrates that this index clearly captures the structural movements of each currency. Furthermore, we argue that this method provides multi-currency balance information not obtainable from simple bilateral PPP comparisons, with potential applications in policy analysis and investment decisions.

**Keywords**: Purchasing Power Parity, Exchange Rate, Compositional Data Analysis, clr Transformation, Currency Valuation, USD/JPY/TRY

---

## Table of Contents

1. [Chapter 1: Introduction](#chapter-1-introduction)
2. [Chapter 2: Theoretical Framework](#chapter-2-theoretical-framework)
3. [Chapter 3: Data and Methods](#chapter-3-data-and-methods)
4. [Chapter 4: Empirical Analysis: Time-Series Interpretation](#chapter-4-empirical-analysis)
5. [Chapter 5: Comparison with Simple PPP Analysis](#chapter-5-comparison-with-simple-ppp-analysis)
6. [Chapter 6: Regime Shifts and Currency Structure Realignment](#chapter-6-regime-shifts)
7. [Chapter 7: Practical Guidelines](#chapter-7-practical-guidelines)
8. [Chapter 8: Monthly Analysis and PPP Update Frequency](#chapter-8-monthly-analysis)
9. [References](#references)

---

# Chapter 1: Introduction

## 1.1 Research Background and Motivation

Measuring currency valuation levels is a critical issue in international financial markets for investment decisions, policy formulation, and risk management. Particularly in multi-currency environments that include emerging market currencies, there is an increasing need for objective methods to assess whether each currency is "overvalued" or "undervalued."

Traditionally, bilateral comparisons based on Purchasing Power Parity (PPP) have been mainstream. However, in real international financial markets, multiple currencies interact simultaneously, and bilateral comparisons alone cannot capture the full picture. For example, when the dollar is surging against both USD/JPY and USD/TRY, it is difficult to determine from bilateral indicators alone whether this reflects "dollar strength" or "weakness in the yen and lira."

Furthermore, when dealing with multiple currencies, conventional methods where the sum of each currency's valuation does not necessarily equal zero cannot consistently represent the relative relationships between currencies—a mathematical problem.

## 1.2 Limitations of Existing Methods

Conventional currency evaluation methods have the following limitations:

### 1.2.1 Limitations of Bilateral Comparison

Simple PPP deviation rates (e.g., $d_{\text{USDJPY}} = \ln(S_{\text{USDJPY}} / \text{PPP}_{\text{JPY}})$) only show the relative relationship between USD and JPY and cannot simultaneously evaluate other currencies.

### 1.2.2 Lack of Independence

When calculating each currency pair's deviation rate independently, the following inconsistency arises:

- $d_{\text{USDJPY}}, d_{\text{USDTRY}}, d_{\text{TRYJPY}}$ each have independent values, but from a triangular arbitrage perspective, $d_{\text{TRYJPY}} = d_{\text{USDTRY}} - d_{\text{USDJPY}}$ should hold

### 1.2.3 Difficulty in Visualizing the Overall Picture

When monitoring multiple bilateral indicators simultaneously, it is difficult to intuitively understand overall structural changes (e.g., isolated movement of a specific currency vs. an overall shift).

### 1.2.4 Lack of Zero-Sum Constraint

Within a closed currency basket, there should be a mathematically guaranteed relationship (zero-sum property) where if one currency is overvalued, another must be undervalued—but conventional methods do not satisfy this.

## 1.3 Proposal of the Mikan 3-Currency clr Index

This research proposes the **Mikan 3-Currency clr Index** to overcome these limitations. This method has the following characteristics:

### 1.3.1 Application of Compositional Data Analysis (CoDA)

Currency evaluation is treated as compositional data, adopting a mathematical framework similar to the centered log-ratio (clr) transformation. This ensures that the sum of each currency's relative valuation $m[i]$ is always zero (zero-sum constraint):

$$
m[\text{USD}] + m[\text{JPY}] + m[\text{TRY}] = 0
$$

### 1.3.2 Simultaneous Three-Currency Evaluation

USD, JPY, and TRY are evaluated simultaneously, expressing each currency's "relative overvaluation/undervaluation within the basket" in a single coordinate system.

### 1.3.3 Versatile Framework

This method is not limited to PPP; by replacing the reference rate $K_i$, it can accommodate various valuation standards:

- Real Effective Exchange Rate (REER)
- Big Mac Index
- Unit Labor Cost (ULC) based fair rates

### 1.3.4 Ease of Visual Understanding

The relative positions of three currencies can be visualized on a 2D plane (projection onto simplex space), allowing intuitive grasp of structural changes over time.

## 1.4 Research Objectives and Contributions

The objectives of this paper are as follows:

1. **Establish theoretical framework**: Clarify the mathematical definition and properties of the Mikan 3-Currency clr Index

2. **Conduct empirical analysis**: Perform empirical analysis for USD, JPY, and TRY using annual PPP data (2005–2024)

3. **Present economic interpretation**: Verify how the calculated index values correspond to actual economic events (yen appreciation, Turkish lira crisis, dollar strength, etc.)

4. **Compare with existing methods**: Demonstrate the advantages of this method over simple PPP deviation analysis

5. **Provide practical guidelines**: Propose applications in financial practice

This research contributes by providing a new framework for currency evaluation in multi-currency environments, making it possible to explicitly analyze relative structures between currencies that could not be captured by conventional bilateral comparisons.

## 1.5 Paper Structure

This paper is organized as follows:

- **Chapter 2**: Details the theoretical framework and mathematical definitions of the Mikan 3-Currency clr Index. Explains the basic formula (Equation 1), zero-sum constraint, and mathematical properties of the three-currency decomposition.

- **Chapter 3**: Explains data and methodology. Shows the data source (World Bank WDI), PPP deviation calculation procedures, and statistical characteristics.

- **Chapter 4**: Conducts empirical analysis for 2005–2024, analyzing the time-series structure and index behavior during major economic events (2011 super-yen-high period, 2018 Turkish lira crisis, 2022 dollar strength, etc.).

- **Chapter 5**: Compares with simple PPP deviation analysis, demonstrating the advantages of the Mikan 3-Currency clr Index. Particularly verifies the relationship between differences in $m[i]$ and bilateral deviation rates $d_{ij}$.

- **Chapter 6**: Analyzes regime shifts and currency structure realignment. Identifies periods of major structural change (2011 super-yen-high, 2013 Abenomics, 2018 lira crisis, 2022 dollar strength) and discusses their economic background.

- **Chapter 7**: Provides practical operational guidelines. Proposes applications for investment decisions, risk management, and policy analysis.

- **Chapter 8**: Analyzes monthly data and the effects of PPP update frequency on MCI interpretation.

---

# Chapter 2: Theoretical Framework and Mathematical Definitions

## 2.1 PPP Deviation and Bilateral Distance Definition

First, we formalize the basic PPP concept and bilateral deviation. Purchasing Power Parity (PPP) is defined as "the exchange rate that equalizes the price levels of two countries." For currencies A and B, let $P_A$ be the price level of currency A (e.g., consumer price index) and $P_B$ be the price level of currency B. The exchange rate $S_{A/B}^{PPP}$ (rate in currency B units per 1 currency A) at which absolute PPP holds is:

$$S_{A/B}^{PPP} = \frac{P_A}{P_B}$$

With the actual nominal exchange rate as $S_{A/B}^{\text{act}}$, we define the PPP deviation rate $d_{A\rightarrow B}$ in logarithmic form:

$$d_{A\rightarrow B} \equiv \ln \frac{S_{A/B}^{\text{act}}}{S_{A/B}^{PPP}} = \ln S_{A/B}^{\text{act}} - \ln \frac{P_A}{P_B}$$

Under this definition, $d_{A\rightarrow B} > 0$ means "the actual rate shows currency A as stronger/currency B as weaker than PPP," indicating currency B is undervalued and currency A is overvalued. Conversely, $d_{A\rightarrow B} < 0$ indicates currency B is overvalued and currency A is undervalued.

In this study, we analyze USD, JPY, and TRY, conventionally treating USD as the base currency (currency A), and calculating PPP deviations with JPY (currency B) and TRY (currency C):

- $d_{USD\rightarrow JPY}$ (PPP deviation of yen against dollar)
- $d_{USD\rightarrow TRY}$ (PPP deviation of Turkish lira against dollar)

---

## 2.2 The Mikan Theorem: Zero-Sum Relationship Among Three Currencies

The **Mikan Theorem** is the proposition that the relative value indicators $m[i]$ for three currencies follow a zero-sum conservation law. In other words, the sum of the three $m[i]$ values is always zero. To satisfy this proposition, we define $m[i]$ from the bilateral deviations $d$ as follows:

$$
\begin{pmatrix}
m[\text{USD}] \\
m[\text{JPY}] \\
m[\text{TRY}]
\end{pmatrix}
\equiv
\begin{pmatrix}
\frac{d_{USD\rightarrow JPY} + d_{USD\rightarrow TRY}}{3} \\
\frac{-2\,d_{USD\rightarrow JPY} + d_{USD\rightarrow TRY}}{3} \\
\frac{d_{USD\rightarrow JPY} - 2\,d_{USD\rightarrow TRY}}{3}
\end{pmatrix}. \tag{1}
$$

This definition strictly guarantees that $m[\text{USD}] + m[\text{JPY}] + m[\text{TRY}] = 0$ (indeed, adding the right-hand sides of equation (1) yields a numerator of $(d_{UJ}+d_{UT}) + (-2d_{UJ}+d_{UT}) + (d_{UJ}-2d_{UT}) = 0$). Here, for brevity, we denote $d_{UJ} \equiv d_{USD\rightarrow JPY}$ and $d_{UT} \equiv d_{USD\rightarrow TRY}$.

The $m[i]$ defined in equation (1) are mispricing indicators corresponding to USD, JPY, and TRY respectively. A **negative value** indicates that the currency is relatively **undervalued** (valued low) within the basket, while a **positive value** indicates it is **overvalued** (valued high).

For example, if $m[\text{JPY}] < 0$, JPY is valued lower than other currencies in the basket (its value has fallen too much relative to others). Conversely, if $m[\text{JPY}] > 0$, JPY is relatively overvalued.

The crucial point is that these three indicators always sum to zero, so the overvaluation of one currency necessarily balances with the undervaluation of others. This can be called the **"dynamic balance among three currencies"**—like mikan (mandarin orange) segments pressing against each other to form a ring.

---

## 2.3 Difference Relationships and Correspondence to Bilateral PPP Deviations

To make definition (1) intuitively understandable, we interpret it from the relationship with $d$. Taking differences between pairs yields:

$$m[\text{USD}] - m[\text{JPY}] = \frac{(d_{UJ}+d_{UT})}{3} - \frac{(-2d_{UJ} + d_{UT})}{3} = d_{UJ},$$

$$m[\text{USD}] - m[\text{TRY}] = \frac{(d_{UJ}+d_{UT})}{3} - \frac{(d_{UJ} - 2d_{UT})}{3} = d_{UT},$$

$$m[\text{JPY}] - m[\text{TRY}] = \frac{(-2d_{UJ} + d_{UT})}{3} - \frac{(d_{UJ} - 2d_{UT})}{3} = d_{UT} - d_{UJ}.$$

Thus, the model's indicators $m[i]$ satisfy the following difference relationships:

- $m[\text{USD}] - m[\text{JPY}] = d_{USD\rightarrow JPY}$
- $m[\text{USD}] - m[\text{TRY}] = d_{USD\rightarrow TRY}$
- $m[\text{JPY}] - m[\text{TRY}] = d_{USD\rightarrow TRY} - d_{USD\rightarrow JPY}$ (this equals the direct PPP deviation of JPY against TRY)

Or equivalently:

- $m[\text{JPY}] - m[\text{USD}] = -d_{USD\rightarrow JPY}$
- $m[\text{TRY}] - m[\text{USD}] = -d_{USD\rightarrow TRY}$

In this way, the difference between each $m[i]$ corresponds to (or equals the sign-reversed version of) the corresponding bilateral PPP deviation $d$.

For example, since $m[\text{USD}] - m[\text{JPY}] = d_{USD\rightarrow JPY}$, if $d_{USD\rightarrow JPY}$ is positive, then $m[\text{USD}] > m[\text{JPY}]$, meaning USD is more **overvalued** than JPY (yen depreciation/dollar appreciation)—this is reflected in the $m$ indicators.

Meanwhile, an increase in $m[\text{USD}]$ (movement toward overvaluation) necessarily causes a decrease in other currencies' $m$ values (movement toward undervaluation), so the total mispricing across the three currencies is conserved. This suggests that during significant Turkish lira fluctuations, the dollar and yen were forced to adjust in opposite directions to maintain the three-way balance.

---

## 2.4 Connection with clr Transformation and CoDA

The definition (1) of $m[i]$ above can also be understood in the context of centered log-ratio (clr) transformation. The clr transformation is an operation that takes the logarithm of each component of a positive-element vector (composition) divided by its geometric mean, and the resulting vector has the property that its sum is zero.

In general, for a composition $x=(x_1,x_2,\dots,x_D)$, letting $g(x) = (x_1 x_2 \cdots x_D)^{1/D}$ be the geometric mean, the clr transformation is defined as:

$$\mathrm{clr}(x)_i = \ln \frac{x_i}{g(x)}$$

Here, $\sum_{i=1}^D \ln\frac{x_i}{g(x)} = \ln \frac{x_1 x_2 \cdots x_D}{(x_1 x_2 \cdots x_D)} = 0$, so the output always sums to zero. This is a fundamental technique in Compositional Data Analysis (CoDA) proposed by Aitchison, providing a geometric framework for properly handling ratio data.

Let us apply the clr transformation to our three-currency model. As a measure of undervaluation corresponding to PPP deviation with USD as the base, we define for each currency $i$: $K_i = \frac{S_{USD/i}^{\text{act}}}{S_{USD/i}^{PPP}}$. $K_i$ indicates "how much cheaper currency $i$ is against the dollar at actual rates," where $K_i > 1$ means currency $i$ is undervalued against the dollar, and $K_i < 1$ means it is overvalued. Indeed, $\ln K_i = d_{USD\rightarrow i}$, so $K_i$ is the exponential form of the PPP deviation.

Setting $x=(K_{USD}, K_{JPY}, K_{TRY})$, the clr transformation $\mathrm{clr}(x)$ for each component is:

$$\mathrm{clr}(x)_i = \ln K_i - \frac{1}{3}(\ln K_{USD} + \ln K_{JPY} + \ln K_{TRY})$$

Since $\ln K_{USD} = d_{USD\rightarrow USD} = 0$ (deviation of dollar against itself is 0), this expression exactly matches definition (1) of $m[i]$. That is:

$$m[i] = \mathrm{clr}(K_{USD}, K_{JPY}, K_{TRY})_i$$

This result shows that our model is constructed according to the CoDA framework. Specifically, we obtain the zero-sum $m[i]$ by applying the clr transformation to the "composition of currency values (degrees of undervaluation) $K_i$." In Aitchison geometry, compositions are represented as points on the simplex, and in clr transformation space, they are projected onto Euclidean space. Therefore, the $m[i]$ vector can essentially be viewed as the Euclidean space representation of the "PPP deviation composition."

In this context, the zero-sum relationship shown by the Mikan Theorem is guaranteed as linear dependence (sum equals zero) in clr space. Moreover, the fact that difference relationships correspond to bilateral deviations means that differences in clr space correspond to log-ratios.

From the above, this model can be described as a reformulation of PPP theory in the context of compositional data—a new approach connecting conventional exchange rate analysis with insights from CoDA and clr transformation. This method yields an indicator system that shows the relative positioning of three currencies at a glance, and subsequent chapters demonstrate its application to real data and analysis results.

---

## 2.5 Choice of PPP Data Source and Invariance in MCI

### 2.5.1 The Problem

PPP data can be obtained from multiple sources:

- IMF WEO (Implied PPP conversion rate)
- World Bank WDI (PA.NUS.PPP)
- OECD PPP Programme

Systematic differences of about 1-2% exist between these sources. This section mathematically examines the impact of such differences on MCI interpretation.

### 2.5.2 Absorption by Zero-Sum Structure

A core property of MCI is the following zero-sum constraint:

$$m[\text{USD}] + m[\text{JPY}] + m[\text{TRY}] = 0$$

Due to this constraint, even if PPP reference values shift overall in "level," the relative positional relationships within the basket are preserved.

Specifically, examining the relative position within the basket (e.g., TRY vs JPY):

$$m[\text{TRY}] - m[\text{JPY}] = \frac{(d_{UJ} - 2d_{UT})}{3} - \frac{(-2d_{UJ} + d_{UT})}{3} = d_{UJ} - d_{UT}$$

This relative position is determined solely by the **difference in bilateral deviation rates**, not by absolute PPP levels.

### 2.5.3 Analysis of Data Source Difference Impact

**Case 1: Common-Direction Small Shift (Realistic Scenario)**

Consider when all currencies' PPP shifts by $\epsilon$ (about 1-2%) in the same direction:

$$\text{PPP}'_i = \text{PPP}_i \cdot (1 + \epsilon)$$

The deviation rate becomes:

$$d'_{A \rightarrow i} = \ln\frac{S}{\text{PPP}'_i} = \ln\frac{S}{\text{PPP}_i} - \ln(1+\epsilon) = d_{A \rightarrow i} - \epsilon'$$

While each $m[i]$ is affected, the relative positions within the basket $m[i] - m[j]$ are determined by differences in $d$, so the common term $\epsilon'$ cancels out.

**Case 2: Currency-Specific Large Divergent Shifts (Hypothetical Scenario)**

If each currency shifts in different directions by 5-10%, the relative positional relationships break down, affecting MCI interpretation.

### 2.5.4 Practical Implications

Real data source differences (1-2%, common direction) are at a level that can be ignored for MCI interpretation.

What matters is:

1. **Consistency**: Using the same source continuously across time series
2. **Observing changes**: Emphasizing time-series changes over absolute levels

The "0" in MCI is not an absolute numerical value but a concept representing an **equilibrium state**, and minor shifts in the reference point are absorbed by the zero-sum structure. This is the mathematical expression of the fact that MCI measures "states" rather than "values."

---

# Chapter 3: Data and Calculation Methods

## 3.1 Data Overview

Exchange rate and PPP data for USD, JPY, and TRY from 2005 to 2024 were used for analysis.

### 3.1.1 Data Sources

**PPP (Purchasing Power Parity):**

- **Source**: IMF World Economic Outlook (WEO)
- **Indicator**: Implied PPP conversion rate (PPPEX)
- **Unit**: LCU per international dollar
- **Target**: Japan (JPN), Turkey (TUR)

**Exchange Rates:**

- **Source**: World Bank WDI / IMF IFS
- **Indicator**: PA.NUS.FCRF (Official exchange rate, period average)
- **Unit**: LCU per USD
- **Target**: USD/JPY, USD/TRY annual average rates

### 3.1.2 Nature of PPP Data

The PPP used in this analysis is the **absolute PPP** conversion factor based on the International Comparison Program (ICP). Unlike relative PPP estimates using CPI, this represents "local currency units per 1 international dollar" calculated by directly comparing price levels across countries.

The IMF WEO Implied PPP conversion rate is broadly consistent with World Bank WDI (PA.NUS.PPP) and OECD PPP Programme, with systematic differences of about 1-2%. However, as shown in Section 2.5, these differences do not substantially affect MCI interpretation.

### 3.1.3 Data Characteristics

| Item | Value |
|------|-------|
| Observation period | 2005-2024 (20 years) |
| Frequency | Annual |
| Number of currencies | 3 (USD, JPY, TRY) |
| Number of observations | 20 |

Japan's PPP conversion factor remained around 100 JPY/international dollar during the 2010s and declined to around 93 in the early 2020s. Meanwhile, Turkey's PPP conversion factor rose dramatically from about 1.5 TRY/international dollar around 2010 to approximately 12.5 TRY by 2024 due to high inflation.

Note that Turkey experienced high inflation and currency revaluation (redenomination in 2005) during the analysis period, resulting in non-linear movements in long-term price indices and exchange rates.

---

## 3.2 Calculation Methods and Statistics

From the above data, bilateral PPP deviations $d_{USD\rightarrow JPY}$ and $d_{USD\rightarrow TRY}$ were calculated for each year, and $m[\text{USD}], m[\text{JPY}], m[\text{TRY}]$ were computed based on Formula (1).

**Restatement of Formula (1)**:

$$
\begin{pmatrix}
m[\text{USD}] \\
m[\text{JPY}] \\
m[\text{TRY}]
\end{pmatrix}
=
\begin{pmatrix}
\frac{d_{USD\rightarrow JPY} + d_{USD\rightarrow TRY}}{3} \\
\frac{-2\,d_{USD\rightarrow JPY} + d_{USD\rightarrow TRY}}{3} \\
\frac{d_{USD\rightarrow JPY} - 2\,d_{USD\rightarrow TRY}}{3}
\end{pmatrix}
$$

The mean and standard deviation of each currency's $m$ value over the 20-year analysis period (2005-2024, 20 annual observations) yielded the following statistics:

### Mean Values

- **$m[\text{USD}]$**: Mean approximately **+0.27**, standard deviation approximately **0.15**
- **$m[\text{JPY}]$**: Mean approximately **+0.28**, standard deviation approximately **0.10**
- **$m[\text{TRY}]$**: Mean approximately **-0.55**, standard deviation approximately **0.12**

### Interpretation

Thus, USD and JPY are **positive on average** over the period, while TRY is **negative on average**.

- **Positive value** = Overvalued (highly valued)
- **Negative value** = Undervalued (lowly valued)

Therefore:

- **USD and JPY showed an overvaluation tendency** on average over the period
- **TRY showed a chronic undervaluation tendency**

This reflects that throughout the analysis period, the Turkish lira was chronically undervalued relative to PPP (the actual exchange rate depreciated far more than warranted by domestic price increases). Meanwhile, USD and JPY were relatively overvalued, though their absolute values were smaller than TRY's deviation.

### Comparison of Standard Deviations

Comparing the standard deviations of $m$ for the three currencies:

- **USD has the largest variation** (standard deviation 0.15)
- **TRY is second largest** (standard deviation 0.12)
- **JPY is smallest** (standard deviation 0.10)

In terms of standard deviation ratios, USD shows about 1.5 times the variation of JPY, and TRY shows about 1.2 times that of JPY. This means that the US dollar experienced relatively large exchange rate fluctuations during the period (especially the 2022 dollar strength phase), while the yen was relatively stable with smaller variation. The Turkish lira fluctuated due to sharp declines in 2018 and 2021 as discussed later, but remained within a certain range in terms of $m$ values.

### Correlation Relationships

Note that the three currencies' $m$ values satisfy the relationship $m[\text{USD}]+m[\text{JPY}]+m[\text{TRY}]=0$ each year, so among the three time series, only two are independent. For example, in years when $m[\text{USD}]$ and $m[\text{TRY}]$ fluctuate significantly, $m[\text{JPY}]$ tends to move accordingly (swinging in the opposite direction).

Looking at series correlations over the entire period:

- **$m[\text{USD}]$ and $m[\text{TRY}]$**: Strong negative correlation (correlation coefficient approximately **-0.73**)
- **$m[\text{USD}]$ and $m[\text{JPY}]$**: Negative correlation (correlation coefficient approximately **-0.58**)
- **$m[\text{JPY}]$ and $m[\text{TRY}]$**: Weak negative correlation (correlation coefficient approximately **-0.13**)

The strong negative correlation between $m[\text{USD}]$ and $m[\text{TRY}]$ suggests that particularly during significant Turkish lira fluctuations, the dollar was forced to adjust in the opposite direction to maintain the three-way balance. That is, when the lira moves strongly toward undervaluation ($m[\text{TRY}]$ becomes more negative), the dollar relatively shifts toward overvaluation ($m[\text{USD}]$ becomes more positive).

Meanwhile, the weak correlation between $m[\text{JPY}]$ and $m[\text{TRY}]$ (approximately -0.13) suggests that there is little direct dynamic relationship between the yen and lira, and rather an indirect relationship mediated through the dollar is dominant.

---

## 3.3 Data Validity Confirmation

The calculated $m$ values were validated on the following points:

### Zero-Sum Constraint Confirmation

For all 20 years (2005-2024), it was confirmed that $m[\text{USD}] + m[\text{JPY}] + m[\text{TRY}] = 0$ holds numerically (strictly 0 except for rounding errors).

### Difference Relationship Confirmation

For any year, the following relationships were confirmed:

- $m[\text{USD}] - m[\text{JPY}] = d_{USD\rightarrow JPY}$
- $m[\text{USD}] - m[\text{TRY}] = d_{USD\rightarrow TRY}$
- $m[\text{JPY}] - m[\text{TRY}] = d_{USD\rightarrow TRY} - d_{USD\rightarrow JPY}$

This ensures that $m$ indicators are consistent with bilateral PPP deviations.

### Economic Validity Confirmation

During major regime transition periods (2011 super-yen-high period, 2018 Turkish lira crisis, 2022 dollar strength phase), $m$ values were confirmed to show signs consistent with economic reality.

**Examples**:
- 2011 (super-yen-high period): $m[\text{JPY}] \approx +0.41$ → Yen is overvalued (correctly reflects yen appreciation)
- 2018 (lira crisis): $m[\text{TRY}] \approx -0.70$ → Lira is undervalued (correctly reflects crash)
- 2022 (dollar strength): $m[\text{USD}] \approx +0.52$ → Dollar is overvalued (correctly reflects dollar strength)

---

## 3.4 Data Availability

The data used in this analysis and the calculated $m$ values are published in the following formats to ensure reproducibility and transparency:

- **Dataset**: `mikan_3currency_clr_index_ppp_data.csv` (all data for 2005-2024)
- **Specification**: Detailed calculation method specifications (`specification_ppp_annual.md`)
- **Verification script**: Python script for formula verification

This enables third-party verification and extension to other periods or currencies.

---

## Summary

This chapter calculated the Mikan 3-Currency clr Index ($m[\text{USD}], m[\text{JPY}], m[\text{TRY}]$) from exchange rate and price data for USD, JPY, and TRY over 20 years (2005-2024).

Statistical analysis results:

1. **USD and JPY showed overvaluation tendency** on average (mean +0.27, +0.28)
2. **TRY showed chronic undervaluation tendency** (mean -0.55)
3. **USD had the largest variation**, JPY the smallest
4. **Strong negative correlation between USD and TRY** (-0.73)

The following chapter examines year-by-year trends in detail regarding these statistical tendencies.

---

# Chapter 4: Empirical Analysis Results: Time-Series Interpretation

## 4.1 Overview

This chapter analyzes the trajectory of MCI coordinates from 2005 to 2024, interpreting them in relation to major economic events.

## 4.2 Major Period Analysis

### 4.2.1 2011: Super Yen-High Period

| Currency | m[i] Value | Interpretation |
|----------|------------|----------------|
| USD | +0.076 | Near average |
| JPY | **+0.410** | Significantly overvalued |
| TRY | -0.486 | Undervalued |

**Background**:
- March 2011: Great East Japan Earthquake → Repatriation expectations push yen higher
- August 2011: US debt ceiling issue → Dollar weakness
- Result: USD/JPY reaches historical low of 75 yen level

### 4.2.2 2018: Turkish Lira Crisis

| Currency | m[i] Value | Interpretation |
|----------|------------|----------------|
| USD | +0.382 | Overvalued |
| JPY | +0.323 | Overvalued |
| TRY | **-0.705** | Severely undervalued |

**Background**:
- US-Turkey diplomatic tensions (Pastor Brunson issue)
- Fed rate hike cycle → Emerging market capital outflow
- Turkey central bank's delayed response → Loss of confidence

### 4.2.3 2022: Dollar Strength Period

| Currency | m[i] Value | Interpretation |
|----------|------------|----------------|
| USD | **+0.518** | Most overvalued |
| JPY | +0.167 | Below average |
| TRY | -0.685 | Severely undervalued |

**Background**:
- Fed aggressive rate hikes (0% → 4.5%)
- BOJ's yield curve control maintenance → JPY weakness
- Energy crisis → Emerging market instability

### 4.2.4 2024: Current State

| Currency | m[i] Value | Interpretation |
|----------|------------|----------------|
| USD | +0.483 | High position |
| JPY | -0.003 | Near average |
| TRY | -0.480 | Undervalued but improving |

**Characteristics**:
- Yen reached near-average position
- Lira improved significantly from crisis period
- Dollar maintains high position

---

## 4.3 Visual Analysis

The time-series chart clearly shows:

1. **2011 Peak**: m[JPY] reached historical maximum
2. **2018 Trough**: m[TRY] reached historical minimum
3. **2022 Peak**: m[USD] reached historical maximum
4. **Recent Trend**: Three currencies converging toward equilibrium

---

# Chapter 5: Comparison with Simple PPP Analysis

## 5.1 Comparison Objectives

This chapter compares simple bilateral PPP deviation analysis with MCI analysis, demonstrating the advantages of MCI.

## 5.2 Information Provided by Simple PPP Analysis

Simple PPP deviation rates:
- $d_{\text{USDJPY}}$: USD/JPY deviation
- $d_{\text{USDTRY}}$: USD/TRY deviation

**Limitations**:
- Cannot directly compare JPY and TRY
- Cannot determine "overall balance"
- Depends on base currency selection

## 5.3 Additional Information from MCI

MCI provides the following additional information:

### 5.3.1 Relative Position Within Basket

MCI shows each currency's position within the 3-currency basket:
- Who is floating highest (overvalued)?
- Who is sinking lowest (undervalued)?
- Who is in the middle?

### 5.3.2 Structure Visualization

MCI allows intuitive understanding of:
- Distance between currencies
- Movement patterns (divergence/convergence)
- Relative change speed

### 5.3.3 Zero-Sum Guaranteed

MCI always satisfies:
$$m[\text{USD}] + m[\text{JPY}] + m[\text{TRY}] = 0$$

This mathematically guarantees the "closed basket" constraint.

---

## 5.4 Mathematical Relationship

The relationship between MCI and bilateral deviation:

$$m[i] - m[j] = d_{i \rightarrow j}$$

This means:
- MCI **includes** bilateral deviation information
- MCI **adds** basket balance information
- Bilateral deviation is a **partial view** of MCI

---

# Chapter 6: Regime Shifts and Currency Structure Realignment

## 6.1 Definition of Structural Change

We define "regime shift" as follows:
- Sustained change in the relative position of specific currencies
- Change in the distance relationship between currencies
- Transition to a new equilibrium state

## 6.2 Major Regime Shifts

### 6.2.1 2011: JPY Dominance Period

**Features**:
- m[JPY] reaches maximum (+0.410)
- m[USD] reaches minimum (+0.076)
- JPY/USD spread maximizes

**Economic Background**:
- Post-earthquake yen buying
- US QE2 → Dollar weakness
- Europe debt crisis → Safe-haven demand for yen

### 6.2.2 2013: Abenomics Shift

**Features**:
- m[JPY] sharply declines (+0.410 → +0.256)
- m[USD] rises (+0.076 → +0.170)
- Regime change through aggressive monetary easing

**Economic Background**:
- BOJ's quantitative and qualitative monetary easing (QQE)
- 2% inflation target announcement
- Rapid yen depreciation (80 yen → 100 yen level)

### 6.2.3 2018: Turkish Lira Crisis

**Features**:
- m[TRY] plunges to -0.705
- TRY isolated from other currencies
- Stress concentrates in TRY

**Economic Background**:
- US-Turkey diplomatic friction
- Insufficient central bank response
- Capital flight from emerging markets

### 6.2.4 2022: Dollar One-Strong Period

**Features**:
- m[USD] reaches historical maximum (+0.518)
- m[JPY] declines, approaches m[TRY]
- USD isolated in "floating" position

**Economic Background**:
- Fed aggressive tightening
- BOJ's continued easing
- Energy crisis impact

---

## 6.3 Detection of Regime Shifts

MCI enables detection of the following:

1. **Crossover**: When m[i] and m[j] cross
   - Example: 2022, m[JPY] approaching m[TRY]

2. **Spread Change**: Change in distance between specific currencies
   - Example: 2018, m[USD]-m[TRY] expansion

3. **Volatility Concentration**: Increased volatility in specific currencies
   - Example: m[TRY]'s high volatility period

---

# Chapter 7: Practical Guidelines

## 7.1 Overview

This chapter provides guidelines for using MCI in practice. Appropriate use of MCI can support investment decisions, risk management, and policy analysis.

## 7.2 Signal Interpretation

### 7.2.1 Extreme Value Signals

| Signal | Condition | Interpretation |
|--------|-----------|----------------|
| Strong Overvaluation | m[i] > +0.4 | Strong mean-reversion pressure |
| Strong Undervaluation | m[i] < -0.6 | Strong mean-reversion pressure |
| Neutral | -0.2 < m[i] < +0.2 | Near equilibrium |

### 7.2.2 Movement Direction Signals

| Signal | Condition | Interpretation |
|--------|-----------|----------------|
| Convergence | All m[i] approaching 0 | Stress dissipation |
| Divergence | m[i] spread expanding | Stress accumulation |
| Isolation | One currency separating | Event concentration |

## 7.3 Investment Applications

### 7.3.1 Long-Term Strategic Allocation

MCI can be used as a reference for long-term currency allocation:
- Reduce weight of currencies with high m[i]
- Increase weight of currencies with low m[i]
- Expect mean-reversion over long horizons

### 7.3.2 Risk Management

MCI is useful for risk monitoring:
- Alert when spread expands
- Hedge when volatility concentrates
- Adjust positions at regime shifts

## 7.4 Limitations and Cautions

### 7.4.1 What MCI Does NOT Predict

- Short-term price movements
- Timing of mean reversion
- Impact of external shocks

### 7.4.2 Combination with Other Indicators

MCI should be used with:
- Interest rate differentials
- Capital flow data
- Political/geopolitical factors
- Technical analysis

### 7.4.3 Basket Dependency

MCI values depend on the selected 3-currency basket:
- Results change with different currency combinations
- "JPY's position in G3" differs from "JPY's position in USD-JPY-TRY"

---

# Chapter 8: Monthly Analysis and PPP Update Frequency

## 8.1 Significance of Monthly Observation

Chapter 4 analyzed long-term structural changes based on annual data. The 20-year graph (Figure 8.0) shown below captures major structural changes: the 2011 yen appreciation peak, the 2018 Turkish lira crisis, and the 2022 dollar strength period.

However, for actual market participants, capturing movements on shorter time scales is important. This chapter uses monthly data from 2022 to 2025 to analyze short-term dynamics of MCI coordinates.

Monthly observation reveals:
1. Short-term stress accumulation/release processes smoothed out in annual data
2. Structural response speed to market events
3. Leading movements signaling regime transitions

---

## 8.2 Monthly MCI Using Annual PPP

The figure below shows monthly MCI coordinates from January 2022 to November 2025, using each year's confirmed PPP values (IMF WEO).

### Observed Features

Several important features can be read from this graph:

**1. Discontinuity at Year Boundaries (Axis Shift)**

At year boundaries marked by orange dotted lines, MCI coordinates jump sharply. **This is not because exchange rates fluctuated dramatically, but because the PPP values (the "axis" for MCI calculation) were annually updated—a superficial change.**

Particularly notable:
- **January 2023**: m[TRY] jumps from about -0.75 to -0.45 (+0.30)
- **January 2024**: m[TRY] jumps from about -0.71 to -0.43 (+0.28)

These jumps indicate that **the "measuring stick" for calculating MCI coordinates changed** due to the IMF significantly revising PPP benchmark values to reflect Turkey's high inflation. Note that the Turkish lira did not surge in the foreign exchange market.

**2. Intra-Year Dynamics**

Between year boundaries, MCI coordinates transition relatively smoothly. The decline in m[TRY] in late 2022 (-0.6 → -0.75) shows structural stress accumulation progressing without waiting for PPP updates.

**3. Information Lag**

PPP is inherently a lagging indicator. IMF and World Bank official PPP estimates:
- Are published after the relevant year
- May be revised retroactively
- Are calibrated based on large-scale surveys (ICP) conducted every three years

Therefore, when using annual PPP, there is a time lag before actual purchasing power changes are reflected in MCI coordinates.

---

## 8.3 Continuous Transition Through PPP Interpolation

To eliminate discontinuity at year boundaries, we created a version with monthly linear interpolation of PPP. The following figure shows the results.

### Interpolation Method

Monthly PPP interpolation was performed as follows:

```
PPP(t) = PPP(year_start) + (PPP(year_end) - PPP(year_start)) × (month - 1) / 12
```

Where:
- `year_start`: Confirmed PPP value for the current year
- `year_end`: Confirmed (or estimated) PPP value for the next year
- `month`: Current month (1-12)

This linear interpolation allows PPP to change gradually each month, eliminating sharp jumps at year boundaries.

### Features of Interpolated Graph

**1. Smooth Transition**

Year-boundary jumps disappear, and MCI coordinates more faithfully reflect actual market movements.

**2. Trend Clarification**

- m[TRY]: Gradual improvement from around -0.6 to around -0.3 over about 3 years
- m[JPY]: Continuous yen depreciation trend reflected, from around +0.2 to around -0.1
- m[USD]: Relatively stable around +0.4

**3. Visualization of Short-Term Stress**

Short-term stress events like the m[TRY] plunge around May 2023 (-0.35 → -0.50) can be more clearly observed.

**4. Relationship Between Stress and Currency Depreciation**

In USD/TRY exchange, the lira continues to depreciate consistently. However, the MCI graph shows m[TRY] converging toward zero (improving). This seemingly contradictory movement can be explained by understanding the essence of what MCI shows.

What MCI reflects is not "price movements" but "the state of structural stress." Taking the yen as an example, m[JPY] is currently near zero, but this does not mean the PPP deviation rate is zero. In fact, the yen remains undervalued by PPP comparison. Zero in MCI indicates "a structurally balanced position within the basket."

For the lira, before 2020, unorthodox monetary policy under the Erdogan administration (insistence on low interest rates despite high inflation and foreign exchange intervention) continued, attempting to artificially support the currency against market mechanisms. As a result, structural stress accumulated and MCI swung deeply into negative territory (bottoming at -0.78 in 2020).

In June 2023, Finance Minister Şimşek took office and normalization toward policy rates matching inflation proceeded. This changed the nature of lira depreciation from "artificial maintenance against the market" to "natural adjustment matching inflation." Prices continue to fall, but as this decline reflects economic reality, structural stress has been released, and MCI shows a clear convergence trend.

Meanwhile, gradual improvement is also seen in 2021-2022, but the factors for improvement during this period are complex. Whether this is the "measuring stick catch-up" effect of PPP estimates themselves being adjusted to more accurately reflect Turkey's actual inflation, or structural stress release after the 2018 shock, cannot be completely separated.

---

## 8.4 Comparison and Interpretation of Both Methods

### Usage Guidelines

| Aspect | Annual PPP | Interpolated PPP |
|--------|------------|------------------|
| **Data Fidelity** | Based on official statistics | Includes estimates |
| **Continuity** | Discontinuous at year boundaries | Continuous |
| **Application** | Rigorous analysis, academic research | Trend analysis, visualization |
| **Ease of Interpretation** | Requires jump explanation | Intuitive |

### Preservation of Economic Meaning

Importantly, regardless of which method is used, the following properties are preserved:

1. **Zero-Sum Constraint**: $m[\text{USD}] + m[\text{JPY}] + m[\text{TRY}] = 0$
2. **Relative Order**: Overvaluation/undervaluation relationships among the 3 currencies are maintained
3. **Long-Term Trends**: Consistency with annual data

The interpolated version provides "visual smoothness," but both are equivalent for fundamental structural analysis.

---

## 8.5 Monthly MCI as a Leading Indicator

Monthly data analysis suggests the leading indicator properties of MCI.

### Leading Nature of Structural Improvement

In the interpolated graph, m[TRY] shows a gradual improvement trend from late 2023. This indicates:

1. **PPP Convergence Pressure**: Extremely undervalued states are unsustainable and will be adjusted somehow
2. **Structural Stress Release**: Inflation rate decline and monetary policy normalization progressing
3. **Market Price Reflection Delay**: Time lag before structural improvement is reflected in prices

The MCI improvement trend may be interpretable as a sign of future currency stabilization. However, this does not predict "when convergence will occur" but rather indicates "structural pressure toward convergence."

### Limitations

- Complete leading nature cannot be expected since PPP itself is a lagging indicator
- Cannot respond to sudden changes from policy changes or geopolitical events
- Even monthly data smooths out daily/weekly short-term fluctuations

---

## 8.6 Chapter Summary

Monthly analysis yielded the following insights:

1. **PPP Update Frequency Impact**: Using annual PPP causes MCI coordinates to jump at year boundaries, making short-term interpretation difficult
2. **Effectiveness of Interpolation**: Monthly interpolated PPP provides smooth transitions, facilitating trend analysis
3. **Equivalence of Both Methods**: For fundamental structural analysis, both methods provide equivalent information
4. **Leading Indicator Potential**: Monthly MCI improvement trends may suggest future price adjustments

The monthly analysis presented in this chapter complements the practical operational guidelines from Chapter 7 on a shorter time scale. Combining long-term structural understanding through annual data with short-term dynamic tracking through monthly data further enhances the practicality of the Mikan 3-Currency clr Index.

---

# References

## Purchasing Power Parity (PPP) and Exchange Rate Determination Theory

1. **Cassel, G. (1918).** "Abnormal Deviations in International Exchanges," *Economic Journal*, 28(112), 413–415.
   - Classic paper first systematically presenting the PPP concept

2. **Rogoff, K. (1996).** "The Purchasing Power Parity Puzzle," *Journal of Economic Literature*, 34(2), 647–668.
   - Important paper discussing why deviations from PPP persist for long periods (PPP puzzle)

3. **Taylor, A. M., & Taylor, M. P. (2004).** "The Purchasing Power Parity Debate," *Journal of Economic Perspectives*, 18(4), 135–158.
   - Survey of PPP theory's historical development and empirical research

## Compositional Data Analysis (CoDA)

4. **Aitchison, J. (1986).** *The Statistical Analysis of Compositional Data*. Chapman & Hall.
   - Foundational text of CoDA

5. **Egozcue, J. J., Pawlowsky-Glahn, V., Mateu-Figueras, G., & Barceló-Vidal, C. (2003).** "Isometric Logratio Transformations for Compositional Data Analysis," *Mathematical Geology*, 35(3), 279–300.
   - Detailed paper on geometric properties of clr/ilr transformations

## Data Sources

6. **World Bank (2024).** *World Development Indicators*. https://databank.worldbank.org/
   - PPP conversion factors and official exchange rates

7. **International Monetary Fund (IMF) (2024).** *World Economic Outlook Database*. https://www.imf.org/en/Publications/WEO

## Currency Crises and Emerging Markets

8. **Kaminsky, G. L., & Reinhart, C. M. (1999).** "The Twin Crises: The Causes of Banking and Balance-of-Payments Problems," *American Economic Review*, 89(3), 473–500.

9. **Reinhart, C. M., & Rogoff, K. S. (2009).** *This Time Is Different: Eight Centuries of Financial Folly*. Princeton University Press.

---

## Data Citation Format

Formal citations for datasets used in this study:

**World Bank (2024).** *World Development Indicators: PPP conversion factor, GDP (LCU per international $)* [Data file]. Retrieved from https://databank.worldbank.org/source/world-development-indicators

**World Bank (2024).** *World Development Indicators: Official exchange rate (LCU per US$, period average)* [Data file]. Retrieved from https://databank.worldbank.org/source/world-development-indicators

---

## Notes

This reference list covers major literature related to the theoretical background, empirical analysis, and application potential of the Mikan 3-Currency clr Index.

- **Purchasing Power Parity (PPP)**: From Cassel (1918) to Rogoff (1996) and Taylor & Taylor (2004), including theoretical development and "PPP puzzle" discussion
- **Compositional Data Analysis (CoDA)**: From Aitchison (1986)'s foundational theory to Egozcue et al. (2003)'s mathematical formulation of clr transformation
- **Empirical Analysis**: Explicitly citing public data sources including World Bank WDI, BIS, and IMF
- **Time Series/Regime Analysis**: Structural change detection methods by Hamilton (1989) and Perron (1989)
- **Currency Crises**: Twin crises research by Kaminsky & Reinhart (1999), Turkish crisis precedent studies
