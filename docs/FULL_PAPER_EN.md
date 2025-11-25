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
2. [Chapter 2: Theoretical Framework and Mathematical Definitions](#chapter-2-theoretical-framework-and-mathematical-definitions)
3. [Chapter 3: Data and Calculation Methods](#chapter-3-data-and-calculation-methods)
4. [Chapter 4: Empirical Analysis and Time-Series Structure](#chapter-4-empirical-analysis-and-time-series-structure)
5. [Chapter 5: Comparison with Simple PPP](#chapter-5-comparison-with-simple-ppp)
6. [Chapter 6: Regime Shifts and Currency Structure Realignment](#chapter-6-regime-shifts-and-currency-structure-realignment)
7. [Chapter 7: Practical Guidelines](#chapter-7-practical-guidelines)
8. [Chapter 8: Monthly Analysis and PPP Update Frequency](#chapter-8-monthly-analysis-and-ppp-update-frequency)
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

- **GitHub Repository**: https://github.com/onigirito/MCI_Mikan-3-Currency-clr-Index_
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

# Chapter 4: Empirical Analysis and Time-Series Structure

This chapter analyzes the trajectory of MCI coordinates over 20 years from 2005 to 2024. The following figure shows the annual progression of the $m$ indicator for each currency.

![Annual MCI Coordinate Progression (2005-2024)](annual_mci_plot.png)

*Figure 4.1: Annual MCI coordinate progression. Blue line represents m[USD], red line represents m[JPY], green line represents m[TRY]. Positive values indicate overvaluation (relatively highly valued within the basket), negative values indicate undervaluation (relatively lowly valued). The sum of all three currencies is always zero.*

From this figure, three major regime transition points can be visually confirmed: the 2011 yen appreciation peak, the 2018 Turkish lira crisis, and the 2022 dollar strength phase. The following sections analyze each period in detail.

---

## 4.1 2005-2010: Yen Appreciation Phase and Lira Stability Period

Around the analysis starting point of 2005, the US dollar and Japanese yen appeared to be trading at rates close to PPP. In fact, the actual USD/JPY rate in 2005 was approximately 110 JPY/USD, and the OECD's estimated PPP rate for that year was around 120 JPY/USD—not a large difference ($d_{USD\rightarrow JPY} \approx -0.19$, approximately 19% yen overvaluation).

Meanwhile, the Turkish lira implemented redenomination in 2005, beginning the stable new lira regime, with the actual rate against the dollar at approximately 1.34 TRY/USD. In terms of price levels, Turkey has lower prices than the US, so the PPP rate was estimated to be slightly lower than the actual rate (e.g., around 0.67 TRY/USD), resulting in $d_{USD\rightarrow TRY} \approx +0.69$ (approximately 99% lira undervaluation).

The $m$ indicators calculated from the above for 2005 were:

- **$m[\text{USD}] \approx +0.165$** (slightly overvalued)
- **$m[\text{JPY}] \approx +0.358$** (overvalued)
- **$m[\text{TRY}] \approx -0.523$** (undervalued)

- Positive value = Overvalued
- Negative value = Undervalued

Thus, in 2005, both USD and JPY were on the overvalued side, with the yen significantly overvalued (strong yen state) and the lira undervalued. However, the deviation in 2005 was not as large as in later years, and the positional relationships among the three currencies were relatively balanced.

Subsequently, from 2006 to 2007, dollar weakness progressed due to the US twin deficit problem, and the yen was also in a low range under carry trade pressure given ultra-low interest rates. In 2007, the rate was around 1 USD = 117.75 JPY, slightly on the yen-weak side compared to the estimated PPP (approximately 124 JPY/USD) at the time, resulting in $d_{USD\rightarrow JPY} \approx -0.053$ (yen slightly overvalued but improved from 2005). Similarly, the lira trading around 1 USD = 1.30 TRY saw its gap with PPP narrow due to price increases, with $d_{USD\rightarrow TRY} \approx +0.57$. As a result, the $m$ values around 2007 were:

- **$m[\text{USD}] \approx +0.172$**
- **$m[\text{JPY}] \approx +0.225$**
- **$m[\text{TRY}] \approx -0.397$**

USD and JPY were both slightly on the overvalued side, with TRY correspondingly on the undervalued side, but the differences among the three were still small—a stable period where, in terms of the Mikan Theorem ring, the three currency points were positioned almost equidistantly near the ring.

However, **the Lehman Shock of 2008** dramatically changed the situation. The rapid global risk-off caused the yen to surge, with USD/JPY advancing to the 103.36 JPY level. This was the result of the yen being bought as a safe-haven asset while carry trade unwinding increased actual demand for yen. Since the PPP rate at the time was still estimated at around 120 JPY, the yen reached a level approximately 16% overvalued against the dollar ($d_{USD\rightarrow JPY} \approx -0.156$).

Meanwhile, the Turkish lira was also sold during the same crisis, trading around 1 USD = 1.30 TRY. Considering Turkey's high inflation, the PPP rate at this point was estimated at around 0.81 TRY/USD, meaning the lira fell into approximately 60% undervaluation ($d_{USD\rightarrow TRY} \approx +0.47$).

These changes are reflected in the $m$ indicators. At 2008:

- **$m[\text{USD}] \approx +0.106$** (moderately overvalued)
- **$m[\text{JPY}] \approx +0.262$** (overvalued)
- **$m[\text{TRY}] \approx -0.368$** (undervalued)

The $m$ configuration during the Lehman Shock period shows JPY overvalued, TRY undervalued, and USD roughly in the middle. Indeed, $m[\text{JPY}] - m[\text{TRY}] \approx 0.262 - (-0.368) = 0.630$, meaning the JPY/TRY rate deviated approximately 87% from PPP (an extreme divergence of strong yen/weak lira). Thus, 2008-2009 was a regime where the three-currency balance tilted dramatically, with the yen extremely strong and the lira extremely weak.

**In 2009**, yen appreciation progressed further, rising to 1 USD = 93.57 JPY. $d_{USD\rightarrow JPY} \approx -0.243$, and the yen reached approximately 22% overvaluation. As a result:

- **$m[\text{USD}] \approx +0.120$**
- **$m[\text{JPY}] \approx +0.363$** (significantly overvalued)
- **$m[\text{TRY}] \approx -0.482$** (significantly undervalued)

The yen shifted further toward overvaluation, and the lira also shifted toward undervaluation.

---

## 4.2 2010-2016: Era of Yen Appreciation Correction and Gradual Lira Decline

After 2009, countries attempted recovery from the crisis through monetary easing and policy responses, and exchange rates somewhat regained stability. The US maintained ultra-low interest rates under quantitative easing (QE) policy, and the dollar remained soft until around 2011. Meanwhile, in Japan, the currency remained elevated relative to others under continuing deflation, **reaching the strongest post-war level of 1 USD = 79.81 JPY in 2011**. This was still significant yen overvaluation far above PPP, reaching $d_{USD\rightarrow JPY} \approx -0.334$ (approximately 28% yen overvaluation).

As a result, $m[\text{JPY}]$ recorded extreme positive values during this period. For 2011:

- **$m[\text{USD}] \approx +0.076$** (slightly overvalued)
- **$m[\text{JPY}] \approx +0.410$** (extremely overvalued)
- **$m[\text{TRY}] \approx -0.486$** (significantly undervalued)

Both dollar and lira became undervalued relative to the yen, creating balance. In terms of the Mikan ring, the yen's point greatly deviated to the overvalued side of the ring, with the other two currencies clustered small on the opposite side.

However, **this situation changed dramatically from 2013 onward**. With the Bank of Japan's launch of Quantitative and Qualitative Easing (QQE), a major shift toward yen weakness occurred, with USD/JPY rising more than 50% from the 80 yen range to temporarily the 120 yen range in 2013-2015. As a result, at 2013:

- **$m[\text{USD}] \approx +0.170$**
- **$m[\text{JPY}] \approx +0.256$** (overvalued but declining)
- **$m[\text{TRY}] \approx -0.426$** (undervalued)

The yen's extreme overvaluation began to ease.

**By 2015**, the actual rate swung to the yen-weak side at 121.04 JPY against the yen's PPP rate against the dollar (approximately 108 JPY/USD), and the long-standing yen overvaluation was nearly resolved. $d_{USD\rightarrow JPY} \approx +0.117$ (approximately 12% yen weakness), and $m[\text{JPY}]$ dropped significantly from +0.410 in 2011 to +0.199.

- **$m[\text{USD}] \approx +0.317$** (overvalued)
- **$m[\text{JPY}] \approx +0.199$** (overvalued but improved)
- **$m[\text{TRY}] \approx -0.516$** (undervalued)

The dollar was somewhat weak globally during this period under the influence of continued quantitative easing, but **within this basket**, it strengthened relatively against the yen, so $m[\text{USD}]$ rose from +0.076 in 2011 to +0.317 in 2015, making the dollar the overvalued side within the basket.

Regarding the Turkish lira, the early 2010s saw a gradual declining trend. Despite high inflation (around 10% annually), lira weakness was relatively gradual, and there were suggestions that the real exchange rate remained elevated. In fact, rates around 1 USD = 1.5 TRY only exceeded 2 TRY by 2013, and while Turkey's cumulative inflation was large during the period, the deviation from PPP rate expanded gradually without a sudden divergence. $d_{USD\rightarrow TRY}$ rose from around +0.56 in 2011 to around +0.83 (approximately 130% lira undervaluation) in 2015, but this was a gradual movement that was largely priced in by the market. During this period, $m[\text{TRY}]$ declined from around -0.49 to around -0.52 (further toward undervaluation), and TRY's undervaluation sense strengthened somewhat.

Overall, looking at the progression of $m$ indicators through the mid-2010s, we can see that JPY and USD roles reversed around 2011, and TRY's undervaluation tendency gradually strengthened. The configuration of "significantly overvalued yen / somewhat overvalued dollar / undervalued lira" in 2011 changed to "overvalued (improved) yen / overvalued dollar / undervalued lira" by 2015.

---

## 4.3 2017-2018: Emergence of the Turkish Lira Crisis

From 2016 onward, the structure of the analysis targets transformed dramatically again. The epicenter was the **Turkish lira's sharp decline**.

From **2017** to 2018, currency selling accelerated in Turkey against the backdrop of current account deficit expansion, political instability, and loss of central bank credibility, and the lira experienced a historic crash against the dollar. Rates around 1 USD = 3.65 TRY at the beginning of 2017 plunged to momentarily over 7 TRY by August 2018.

**2017** situation:

- **$m[\text{USD}] \approx +0.345$** (overvalued)
- **$m[\text{JPY}] \approx +0.280$** (overvalued)
- **$m[\text{TRY}] \approx -0.625$** (significantly undervalued)

Turkey's inflation rate also surged during this period, reaching around 20% annually by 2018, but the pace of exchange rate decline exceeded even that, and the deviation from PPP rate expanded to unprecedented levels.

Looking closely at **2018**, the estimated 2018 average PPP was approximately 1.63 TRY/USD while the actual average rate was approximately 4.84 TRY/USD, resulting in $d_{USD\rightarrow TRY} = \ln(4.84/1.63) \approx +1.086$, meaning the lira was in an extreme state of approximately 196% undervaluation in real value terms.

According to the Mikan Theorem, this deviation manifests as a sharp drop in $m[\text{TRY}]$. Indeed, the $m$ values for 2018 were:

- **$m[\text{USD}] \approx +0.382$** (overvalued)
- **$m[\text{JPY}] \approx +0.323$** (overvalued)
- **$m[\text{TRY}] \approx -0.705$** (extremely undervalued)

Due to the lira's crash, $m[\text{TRY}]$ dropped sharply from around -0.52 in 2015 to -0.71 (toward extreme undervaluation). Meanwhile, $m[\text{USD}]$ and $m[\text{JPY}]$ shifted relatively toward the overvalued direction.

The dollar particularly rose as a safe-haven asset during the Turkey crisis, causing $m[\text{USD}]$ to rise to around +0.38 (dollar overvalued). The yen similarly saw its relative valuation rise, but the swing was not as large as the dollar's (the yen in 2018 was roughly at or slightly above PPP).

Reinterpreting this 2018 situation through the Mikan Theorem ring, **the lira's point moved greatly to the undervalued side of the ring**, with the dollar and yen points gathering on the opposite (overvalued) side. Indeed, $m[\text{TRY}] - m[\text{JPY}] \approx -0.705 - 0.323 = -1.028$, meaning the JPY/TRY exchange rate deviated significantly from PPP (the Turkish lira was approximately 180% undervalued against the yen in real terms).

This was precisely a phase where the structural positional relationship between TRY and JPY (as well as USD) fundamentally changed. In other words, **2018 was a major regime transition point in this analysis period**, the year when TRY's role transformed from "somewhat undervalued emerging market currency" to "extremely undervalued unstable currency." That distortion was absorbed by the other two currencies, creating a configuration where the dollar was positioned as a relatively strong currency and the yen as a quasi-safe-haven asset.

---

## 4.4 2019-2024: New Equilibrium After the Crash and Further Fluctuations

From 2019 onward, the global economy experienced major shocks including US-China trade friction and the pandemic (COVID-19), and major currencies fluctuated, but within this analysis basket, **TRY's extreme weakness continued to stand out**.

### 2019-2020: Further Lira Decline

From 2019 to 2020, the Turkish lira temporarily stabilized but entered a declining trend again from late 2020.

**2019**:
- **$m[\text{USD}] \approx +0.394$** (overvalued)
- **$m[\text{JPY}] \approx +0.340$** (overvalued)
- **$m[\text{TRY}] \approx -0.734$** (extremely undervalued)

**2020** (COVID-19 pandemic):
- **$m[\text{USD}] \approx +0.419$** (significantly overvalued)
- **$m[\text{JPY}] \approx +0.361$** (significantly overvalued)
- **$m[\text{TRY}] \approx -0.781$** (extremely undervalued)

In 2020, $m[\text{TRY}]$ dropped to -0.78, reaching the most undervalued level during the analysis period.

### 2021: Deepening Currency Crisis

In **2021**, repeated rate cuts by the central bank and policy distrust led to a currency crisis-like crash. When rates reached around 1 USD = 8.89 TRY at the end of 2021, lira credit concerns peaked in the market, and the government took extraordinary measures including deposit protection schemes.

- **$m[\text{USD}] \approx +0.429$** (significantly overvalued)
- **$m[\text{JPY}] \approx +0.323$** (overvalued)
- **$m[\text{TRY}] \approx -0.753$** (extremely undervalued)

### 2022: Dollar Strength / Yen Weakness Phase

Prices also surged from late 2021 through 2022, with the 2022 inflation rate recording over 70% annually. But lira weakness progressed even faster, with the 2022 average actual rate at approximately 16.57 TRY/USD against PPP estimate of around 5.0 TRY/USD, reaching $d_{USD\rightarrow TRY} = \ln(16.57/5.0) \approx +1.20$. This was one of the largest deviation margins during the analysis period.

Meanwhile, **the US dollar rapidly gained value from the global monetary tightening (Fed rate hike) stance**, with the dollar index (DXY) reaching a 20-year high in 2022. The yen, meanwhile, weakened independently due to the Bank of Japan's stance of maintaining low interest rates, with yen weakness progressing to nearly 1 USD = 131.46 JPY in 2022.

In response to these movements, **2022 saw divergent fortunes for the dollar and yen** within this three-currency basket. Yen weakness means upward deviation from the yen's PPP (actual rate > PPP), resulting in $d_{USD\rightarrow JPY} = \ln(131.46/92.5) \approx +0.35$ (approximately 42% yen weakness).

**2022 $m$ indicators**:

- **$m[\text{USD}] \approx +0.518$** (**extremely overvalued**)
- **$m[\text{JPY}] \approx +0.167$** (overvalued)
- **$m[\text{TRY}] \approx -0.685$** (extremely undervalued)

Dollar strength is partly autonomous movement as the reserve currency, but manifests as overvaluation against yen and lira, with $m[\text{USD}]$ shifting even further positive (toward overvaluation).

The characteristic of this year is that **not only TRY but also JPY deviated upward from PPP (opposite to 2011)**. That is, with the dollar standing alone strong against the other two currencies and the yen also being sold due to domestic factors, the following new configuration emerged:

- **USD extremely overvalued** ($m[\text{USD}] = +0.518$, maximum during analysis period)
- **JPY moderately overvalued** ($m[\text{JPY}] = +0.167$, lowest since 2015)
- **TRY extremely undervalued** ($m[\text{TRY}] = -0.685$)

USD runs away within the basket, JPY remains in overvalued territory but TRY's extreme undervaluation satisfies the zero-sum constraint.

In terms of the Mikan Theorem ring, the dollar's point greatly deviates to the overvalued side of the ring, with yen and lira each in different positions. The distance between JPY and TRY itself is also large ($m[\text{JPY}] - m[\text{TRY}] \approx 0.167 - (-0.685) = 0.852$), so the deviation between them is also large.

### 2023: Adjustment Phase

Entering **2023**, financial suppression measures for regime maintenance in Turkey temporarily worked, and the lira stabilized for several months. However, when policy direction changed after the presidential election, exchange rate adjustment occurred, with USD/TRY surging from June and exceeding 23.77 TRY/USD by year-end 2023. Inflation also re-accelerated, reaching nearly 50% by year-end.

Meanwhile, the US dollar entered a slight adjustment phase against major currencies from mid-2023, and the yen recovered somewhat but remained in the weak range around 140 JPY/USD.

**2023 $m$ indicators**:

- **$m[\text{USD}] \approx +0.498$** (significantly overvalued)
- **$m[\text{JPY}] \approx +0.084$** (slightly overvalued)
- **$m[\text{TRY}] \approx -0.582$** (extremely undervalued)

Though not as extreme as 2022, the configuration of "significantly undervalued TRY / overvalued USD / moderately overvalued JPY" continued.

### 2024: Current Situation

Regarding **2024**, the Turkish central bank's shift to significant rate hikes from the beginning of the year has calmed lira decline, but given the high prices and negative real interest rates, fundamental stability is expected to take time.

**2024 $m$ indicators**:

- **$m[\text{USD}] \approx +0.483$** (significantly overvalued)
- **$m[\text{JPY}] \approx -0.003$** (nearly neutral)
- **$m[\text{TRY}] \approx -0.480$** (significantly undervalued)

2024 became the year when the yen first turned negative (to the undervalued side). This was because yen weakness progressed further, reaching $d_{USD\rightarrow JPY} \approx +0.49$ (approximately 63% yen weakness).

---

## 4.5 Summary of Time-Series Analysis

From the above time-series analysis from 2005 to 2024, **three major turning points—2011, 2018, and 2022**—emerged.

### Regime Transition Points

1. **2011**: Regime transition of the yen through correction of super-yen-high
   - $m[\text{JPY}]$ improved from extreme +0.41 overvaluation to +0.20 by 2015

2. **2018**: Regime transition of the lira through the Turkish lira crisis
   - $m[\text{TRY}]$ dropped sharply from -0.52 to -0.71 (toward extreme undervaluation)

3. **2022**: Unipolar dollar overvaluation phase due to changes in global financial environment
   - $m[\text{USD}]$ rose to +0.52 (maximum during analysis period)

### Structural Changes for Each Currency

In each of these phases, this paper's indicator $m[i]$ clearly captured the structural changes. Especially regarding post-2018, TRY's $m$ has greatly deviated from its previous range (around -0.4 to -0.5) and become entrenched at low levels of -0.7 or below, which can be evaluated as **having entered a new regime**.

Furthermore, as a side effect, USD's $m$ has also shifted from its stable period (around +0.1 to +0.3) to +0.4 to +0.5, suggesting that the dollar's position within the basket has relatively changed.

For the yen, due to special circumstances (long-term low inflation and policy differences), it dropped significantly from positive territory to near zero around 2022, but has been slightly corrected since 2023, and appears to be moving subordinately to dollar/lira movements in the medium term.

Thus, this model makes it possible to describe changes in each currency's structural role along the time axis, and the following chapter further considers its characteristics through comparison with simple PPP models

---

# Chapter 5: Comparison with Simple PPP

This chapter compares the analysis results based on the Mikan Theorem proposed in this paper with conventional simple PPP-based analysis results. A representative example of simple PPP analysis is the method of directly using bilateral purchasing power parity deviation as an indicator. Here, we focus on two currencies—the Japanese yen and Turkish lira—as an example, calculating the JPY/TRY PPP deviation indicator for comparison.

---

## 5.1 Definition of Bilateral PPP Deviation

When considering the PPP deviation between JPY and TRY, this dataset defines the deviation on a **TRY/JPY** (how many yen per 1 Turkish lira) rate basis. Denoting this as $d_{\text{TRY/JPY}}$:

$$d_{\text{TRY/JPY}} = \ln \frac{S_{\text{TRY/JPY}}^{\text{act}}}{S_{\text{TRY/JPY}}^{PPP}}$$

Where:
- $S_{\text{TRY/JPY}}^{\text{act}} = S_{\text{USD/JPY}}^{\text{act}} / S_{\text{USD/TRY}}^{\text{act}}$ (actual cross rate)
- $S_{\text{TRY/JPY}}^{PPP} = \text{PPP}_{JPY} / \text{PPP}_{TRY}$ (PPP-based cross rate)

Transforming this equation:

$$d_{\text{TRY/JPY}} = \ln S_{\text{USD/JPY}}^{\text{act}} - \ln S_{\text{USD/TRY}}^{\text{act}} - (\ln \text{PPP}_{JPY} - \ln \text{PPP}_{TRY})$$

$$= \left(\ln \frac{S_{\text{USD/JPY}}^{\text{act}}}{\text{PPP}_{JPY}}\right) - \left(\ln \frac{S_{\text{USD/TRY}}^{\text{act}}}{\text{PPP}_{TRY}}\right)$$

$$= d_{USD\rightarrow JPY} - d_{USD\rightarrow TRY}$$

In other words, **the TRY/JPY PPP deviation can be expressed as the difference between USD/JPY and USD/TRY PPP deviations**.

### Sign Interpretation

- **$d_{\text{TRY/JPY}} > 0$**: TRY/JPY actual rate is higher than PPP → Turkish lira is overvalued against yen
- **$d_{\text{TRY/JPY}} < 0$**: TRY/JPY actual rate is lower than PPP → Turkish lira is undervalued against yen

---

## 5.2 Relationship with the Mikan Theorem Model

As derived in Chapter 2, the $m[i]$ of the Mikan Theorem model satisfies the following difference relationships:

$$m[\text{USD}] - m[\text{JPY}] = d_{USD\rightarrow JPY}$$
$$m[\text{USD}] - m[\text{TRY}] = d_{USD\rightarrow TRY}$$

Taking the difference between JPY and TRY from these equations:

$$m[\text{JPY}] - m[\text{TRY}] = (m[\text{USD}] - m[\text{TRY}]) - (m[\text{USD}] - m[\text{JPY}])$$

$$= d_{USD\rightarrow TRY} - d_{USD\rightarrow JPY}$$

$$= -d_{\text{TRY/JPY}}$$

Therefore, **the Mikan Theorem model's $m[\text{JPY}] - m[\text{TRY}]$ equals the sign-reversed simple PPP indicator $d_{\text{TRY/JPY}}$**.

This relationship is important. Because while both models return matching values for bilateral deviation, they differ in how information is expressed.

---

## 5.3 Comparison Using Concrete Examples

Let us compare both methods using actual data.

### 2007 Example

In 2007, the yen was slightly undervalued ($d_{USD\rightarrow JPY} \approx -0.053$) and the lira was also somewhat undervalued ($d_{USD\rightarrow TRY} \approx +0.569$):

**Simple PPP indicator**:
$$d_{\text{TRY/JPY}} = d_{USD\rightarrow JPY} - d_{USD\rightarrow TRY} \approx -0.053 - 0.569 = -0.622$$

This indicates a situation where "the Turkish lira is approximately 54% undervalued against the yen" ($e^{-0.622} \approx 0.54$).

**Mikan Theorem model**:
- $m[\text{USD}] \approx +0.172$ (dollar slightly overvalued)
- $m[\text{JPY}] \approx +0.225$ (yen slightly overvalued)
- $m[\text{TRY}] \approx -0.397$ (lira undervalued)

Taking the difference:
$$m[\text{JPY}] - m[\text{TRY}] \approx 0.225 - (-0.397) = 0.622 = -d_{\text{TRY/JPY}}$$

Both match except for sign.

### Interpretation Differences

**Simple PPP** yields a **single value** $d_{\text{TRY/JPY}} = -0.622$ from which we can conclude "lira is undervalued against yen," but **we cannot see each currency's relationship to USD separately**.

**The Mikan Theorem model** expresses the value corresponding to $d_{\text{TRY/JPY}}$ as the difference $m[\text{JPY}] - m[\text{TRY}] = 0.622$, and further visualizes the breakdown as individual $m[\text{JPY}]$ and $m[\text{TRY}]$ levels.

In fact, at 2007:
- $m[\text{JPY}] = +0.225$ → **yen is slightly overvalued**
- $m[\text{TRY}] = -0.397$ → **lira is undervalued**

We can individually read that "the yen is valued somewhat high" and "the lira is valued low." Understanding that these combine to produce the bilateral deviation of 0.622 makes **clear how much each currency contributes to the deviation**.

---

### 2009 Example (Post-Lehman Shock)

In 2009, the yen surged and the lira declined:

**Simple PPP indicator**:
$$d_{\text{TRY/JPY}} = d_{USD\rightarrow JPY} - d_{USD\rightarrow TRY} \approx -0.243 - 0.602 = -0.845$$

This indicates an extreme situation where "the Turkish lira is approximately 57% undervalued against the yen."

**Mikan Theorem model**:
- $m[\text{USD}] \approx +0.120$
- $m[\text{JPY}] \approx +0.363$ (**yen significantly overvalued**)
- $m[\text{TRY}] \approx -0.482$ (**lira significantly undervalued**)

$$m[\text{JPY}] - m[\text{TRY}] \approx 0.363 - (-0.482) = 0.845 = -d_{\text{TRY/JPY}}$$

### Interpretive Advantage

Simple PPP shows from $d_{\text{TRY/JPY}} = -0.845$ only that there is a "large deviation between yen and lira," but the breakdown is invisible.

The Mikan Theorem model clearly separates:
- **Extreme yen overvaluation** ($m[\text{JPY}] = +0.363$, reflecting post-Lehman yen strength)
- **Significant lira undervaluation** ($m[\text{TRY}] = -0.482$, reflecting emerging market selloff)

These **two factors** are clearly separated. For example, even if $d_{\text{TRY/JPY}}$ is a large negative in some year, whether the breakdown is "yen near neutral with lira extremely undervalued" or "lira neutral but yen extremely overvalued" would have different policy implications. This model helps discern that difference.

---

### 2018 Example (Turkish Lira Crisis)

In 2018, $d_{\text{TRY/JPY}} = d_{USD\rightarrow JPY} - d_{USD\rightarrow TRY} \approx 0.058 - 1.086 = -1.028$, yielding a negative sign with very large absolute value (approximately 1.03).

This means "the yen is abnormally overvalued against the Turkish lira" (conversely, the lira is approximately 64% undervalued against the yen, $e^{-1.028} \approx 0.36$)—seemingly counterintuitive content. However, the reality is that **the lira's decline was larger than the yen's this year**, so the yen was only relatively overvalued.

**The Mikan Theorem model** shows for 2018:
- $m[\text{USD}] \approx +0.382$ (dollar overvalued)
- $m[\text{JPY}] \approx +0.323$ (yen overvalued)
- $m[\text{TRY}] \approx -0.705$ (**lira extremely undervalued**)

$$m[\text{JPY}] - m[\text{TRY}] \approx 0.323 - (-0.705) = 1.028 = -d_{\text{TRY/JPY}}$$

What **simple PPP** shows only as "extreme yen-high/lira-low deviation" is shown in **this model as the breakdown: "the yen is also on the overvalued side, but the lira's undervaluation is even more severe."**

This breakdown information is considered important for investors and policy authorities analyzing causes during exchange rate abnormalities. In other words, what simple PPP shows only as "distortion between two currencies" is **decomposed in this model into "the structure of which currency is causing the distortion."**

---

## 5.4 Quantitative Comparison and Consistency

As described above, the Mikan Theorem model and simple PPP model return matching values for bilateral deviation, but this model is superior from the perspective of simultaneous multi-currency comparison.

For example, this model can **display all three pairs USD-JPY, USD-TRY, JPY-TRY relationships at once** (as a set of $m[\text{USD}], m[\text{JPY}], m[\text{TRY}]$).

On the other hand, simple PPP analysis requires calculating three bilateral indicators separately, necessitating consideration of their consistency. In fact, the following relationship should hold:

$$d_{\text{TRY/JPY}} = d_{USD\rightarrow JPY} - d_{USD\rightarrow TRY}$$

However, they may not strictly match due to data errors, etc. This model incorporates this consistency condition from the beginning, so it can **analyze three currencies in a form where bilateral inconsistencies do not exist**.

Even for actual data, if there are PPP estimation errors or asynchronicity, simple PPP indicators may contain contradictions, but $m[i]$ has the property of absorbing such contradictions (since the sum is forced to zero at each time point, errors do not accumulate unilaterally).

---

## 5.5 Differences in Visual Interpretation

Bilateral PPP deviation $d$ is a single value, typically shown on a time-series chart.

In contrast, this model's $m$ consists of 3 variables, and can conceivably be visualized through 2D plots (e.g., a plane plot with $m[\text{USD}]$ on the x-axis and $m[\text{JPY}]$ on the y-axis). This connects to the concept of the "Mikan Theorem ring," and **plotting the positions of 3 points should immediately show which currency is relatively high and which is low**.

With simple PPP, separate graphs must be drawn for each bilateral combination, making it inferior in visual comprehensiveness. This model's advantage lies in **being able to express multi-currency relationships in a single frame**.

For example, when visualizing the 2018 Turkish lira crisis situation:

**Simple PPP** requires:
- USD/JPY deviation graph
- USD/TRY deviation graph
- TRY/JPY deviation graph

—three independent graphs.

**The Mikan Theorem model** requires:
- Arrangement of 3 points (USD, JPY, TRY) on a 2D plane

—**one plot** to grasp the overall picture. On this plot, TRY's point is positioned far on the undervalued side (negative region), while USD and JPY points are positioned close together on the overvalued side (positive region), visible at a glance.

---

## 5.6 Summary

From the above, compared to simple PPP analysis, this model:

1. **Enables factor decomposition of bilateral deviation**
2. **Provides a consistent framework for handling multiple currencies simultaneously**
3. **Can show relationships visually and structurally**

and thus can be said to be superior in these respects.

However, simple PPP analysis is also useful as individual bilateral evaluation, and reading it together with this model's results deepens understanding. In fact, using each time point's $m[i]$ derived in previous chapters, bilateral PPP deviations can easily be reproduced—**the two are complementary**.

---

# Chapter 6: Regime Shifts and Currency Structure Realignment

## 6.1 Purpose of Regime Analysis

This chapter analyzes **regime shifts** in the three-currency structure through time-series changes in the Mikan 3-Currency clr Index over 20 years from 2005 to 2024.

A regime shift refers to a period when the structure of relative currency valuations qualitatively changes. It signifies not mere numerical fluctuation, but a changing of the guard in terms of "which currency is structurally overvalued/undervalued."

## 6.2 Overview of the Entire Observation Period

### 6.2.1 Long-term Trends of Three Currencies

Statistical characteristics for 2005-2024 (see Chapter 3):

- **m[USD]**: Mean +0.27 (standard deviation 0.15)
  → Positioned in **positive territory** (overvalued side) throughout observation period

- **m[JPY]**: Mean +0.28 (standard deviation 0.10)
  → **Positive territory** in first half of observation period, but declined to near zero by 2024

- **m[TRY]**: Mean -0.55 (standard deviation 0.12)
  → Positioned in **negative territory** (undervalued side) throughout entire period, with expanding undervaluation

### 6.2.2 Major Structural Characteristics

- **Negative correlation between USD and JPY** (r = -0.58): When USD becomes overvalued, JPY tends to become undervalued
- **TRY's isolation** (USD-TRY: r = -0.73, JPY-TRY: r = -0.13): Lira shows independent movement
- **Structural change around 2013**: Transition from JPY-led period to USD-led period

## 6.3 Regime Classification and Major Transition Points

The observation period is divided into the following four regimes:

| Regime | Period | Characteristics | Lead Currency |
|--------|--------|-----------------|---------------|
| **I. JPY-Led Period** | 2005-2012 | Yen most overvalued, lira most undervalued | JPY |
| **II. Transition Period** | 2013-2017 | Handover from yen to dollar | USD ↔ JPY |
| **III. USD-Led Period** | 2018-2021 | Dollar most overvalued, lira crisis deepens | USD |
| **IV. Extreme USD High/JPY Plunge Period** | 2022-2024 | Extreme dollar overvaluation, yen neutralization | USD |

---

## 6.4 Regime I: JPY-Led Period (2005-2012)

### 6.4.1 Structural Characteristics

This period was when **m[JPY] was the highest among the three currencies** (most overvalued), a time when the yen was structurally highly valued.

**Representative values**:

| Year | m[USD] | m[JPY] | m[TRY] | Most Overvalued |
|------|--------|--------|--------|-----------------|
| 2005 | +0.165 | **+0.358** | -0.523 | JPY |
| 2008 | +0.106 | **+0.262** | -0.368 | JPY |
| 2011 | +0.076 | **+0.410** | -0.486 | JPY |
| 2012 | +0.092 | **+0.401** | -0.493 | JPY |

### 6.4.2 2011: Peak of Super Yen-High Period

**2011** was the super yen-high period following the Great East Japan Earthquake, and m[JPY] recorded **+0.410**, the highest value for the entire observation period.

- m[USD] = +0.076 (lowest level)
- m[JPY] = **+0.410** (peak)
- m[TRY] = -0.486 (undervalued maintained)

This structure indicates that risk-off flight to the yen as a safe asset caused the yen to become extremely overvalued within the basket.

### 6.4.3 Economic Background

- **2005-2007**: Limited yen weakness pressure from Japan's zero interest rate policy and carry trade
- **2008-2009**: Yen buying pressure from risk-off following Lehman Shock
- **2010-2012**: Yen strength reaches extreme through European debt crisis and Great East Japan Earthquake

---

## 6.5 Regime II: Transition Period (2013-2017)

### 6.5.1 Structural Transformation by Abenomics

The first major regime shift occurred in **2012→2013**. The magnitude of change during this period was among the largest in the observation period:

- **m[JPY]**: +0.401 → +0.256 (-0.145 large decline)
- Annual data shows gradual change, but reflects the rapid yen depreciation in early 2013 (BOJ's unprecedented easing)

**Post-2013 structure**:

| Year | m[USD] | m[JPY] | m[TRY] | Most Overvalued |
|------|--------|--------|--------|-----------------|
| 2013 | +0.170 | +0.256 | -0.426 | JPY → USD transition |
| 2014 | +0.226 | +0.231 | -0.456 | JPY/USD balanced |
| 2015 | **+0.317** | +0.199 | -0.516 | **USD** |
| 2016 | +0.295 | +0.279 | -0.573 | **USD** |
| 2017 | +0.345 | +0.280 | -0.625 | **USD** |

### 6.5.2 Changing of the Guard

From **2015** onward, m[USD] > m[JPY] became established, and **the dollar seized the position of structurally most overvalued**.

- 2015: m[USD] = **+0.317** > m[JPY] = +0.199
- This difference (approximately 0.12) indicates clear structural change

### 6.5.3 Economic Background

- **April 2013**: BOJ's Quantitative and Qualitative Easing (QQE) begins
- **2014-2015**: US monetary normalization discussion begins, Japan-US monetary policy direction divergence
- **2016-2017**: Trump administration inaugurated, dollar strength becomes established

---

## 6.6 Regime III: USD-Led Period (2018-2021)

### 6.6.1 Structural Characteristics

This period was when **m[USD] was clearly the highest**, and **the Turkish lira's structural vulnerability** became evident.

**Representative values**:

| Year | m[USD] | m[JPY] | m[TRY] | Most Overvalued | Notes |
|------|--------|--------|--------|-----------------|-------|
| 2018 | **+0.382** | +0.323 | **-0.705** | USD | Lira crisis |
| 2019 | **+0.394** | +0.340 | -0.734 | USD | Lira undervaluation continues |
| 2020 | **+0.419** | +0.361 | **-0.781** | USD | COVID-19 |
| 2021 | **+0.429** | +0.323 | **-0.753** | USD | Dollar strength persists |

### 6.6.2 2018: Turkish Lira Crisis

**2018** recorded m[TRY] at **-0.705**, an extreme undervaluation level. This is the second largest undervaluation in the observation period (the maximum was -0.781 in 2020).

**Structural impact**:

- The lira crash made its isolation within the three-currency basket definitive
- Dollar and yen became relatively overvalued (m[USD] = +0.382, m[JPY] = +0.323)
- After this year, m[TRY] always remains in deep undervaluation territory below -0.68

### 6.6.3 2020: COVID-19 and Maximum Lira Undervaluation

**2020** recorded m[TRY] = **-0.781**, the **most undervalued** state of the entire observation period.

Simultaneously, m[USD] = +0.419, m[JPY] = +0.361, showing both hard currencies becoming overvalued, indicating risk aversion and emerging market currency selling proceeding simultaneously.

### 6.6.4 Economic Background

- **August 2018**: Turkish central bank independence concerns, lira crash from diplomatic conflict with US
- **2019-2020**: Turkey's inflation acceleration, central bank's unorthodox monetary policy
- **March 2020-**: Risk-off from COVID-19, comprehensive emerging market currency weakness
- **2021**: Coexistence of US monetary easing continuation and dollar strength

---

## 6.7 Regime IV: Extreme USD High/JPY Plunge Period (2022-2024)

### 6.7.1 Structural Characteristics

This period was when **m[USD] recorded the maximum value for the observation period**, while **m[JPY] rapidly declined**.

**Representative values**:

| Year | m[USD] | m[JPY] | m[TRY] | Most Overvalued | Notes |
|------|--------|--------|--------|-----------------|-------|
| 2022 | **+0.518** | +0.167 | -0.685 | USD | Observation period maximum |
| 2023 | +0.498 | +0.084 | -0.582 | USD | Yen's sharp decline |
| 2024 | +0.483 | **-0.003** | -0.480 | USD | Yen neutralization |

### 6.7.2 2022: Extreme Dollar Strength

**2022's** m[USD] = **+0.518** is the **maximum overvaluation level** in the 20-year observation period.

Year-over-year change was also notable:

- **2021→2022**: m[USD] rose +0.429 → +0.518 (+0.089 increase)
- **2021→2022**: m[JPY] fell +0.323 → +0.167 (-0.156 decline)

This rapid structural change reflects the **extreme divergence in Japan-US monetary policy**:

- US: Rapid rate hikes (starting March 2022, cumulative +4.25% within the year)
- Japan: YCC (Yield Curve Control) continuation, monetary easing maintained

### 6.7.3 2023-2024: Yen Neutralization

In **2024**, m[JPY] = **-0.003**, nearly zero, and the yen reached a **neutral** position (neither overvalued nor undervalued) within the basket.

This is the first time since 2005, indicating structural transition:

- **2005-2022**: m[JPY] was always positive (overvalued side)
- **2024**: m[JPY] ≈ 0 (neutral)

**2023-2024 changes**:

| Currency | 2023→2024 Change | Interpretation |
|----------|------------------|----------------|
| USD | +0.498 → +0.483 (-0.015) | Slight decline (high level maintained) |
| JPY | +0.084 → -0.003 (-0.087) | Sharp decline (neutralization) |
| TRY | -0.582 → -0.480 (+0.102) | Undervaluation easing |

### 6.7.4 Structural Meaning of Regime IV

The essence of this regime is **bipolarization of the three-currency structure**:

1. **Extreme dollar overvaluation** (m[USD] ≈ +0.5)
2. **Yen neutralization** (m[JPY] ≈ 0)
3. **Structural lira undervaluation** (m[TRY] ≈ -0.5)

Due to the zero-sum constraint, the extreme symmetric structure m[USD] ≈ -m[TRY] has emerged. The yen is positioned between both, serving the role of "relative reference point."

### 6.7.5 Economic Background

- **2022**: Fed's rapid rate hikes, BOJ's YCC maintenance, USD/JPY breaches 150 yen
- **2023**: BOJ YCC modification (ceiling raised), signs of yen carry unwinding
- **2024**: BOJ monetary policy normalization discussion, dollar strength continues

---

## 6.8 Quantitative Detection of Regime Shifts

### 6.8.1 Identification of Large-Scale Fluctuations

"Large-scale fluctuations" where |Δm[i]| > 0.10 year-over-year are concentrated in the following periods:

| Period | Maximum Change | Primary Currency | Content |
|--------|----------------|------------------|---------|
| 2006→2007 | 0.101 | TRY +0.101 | Short-term lira overvaluation |
| 2008→2009 | 0.114 | JPY +0.101 | Yen appreciation acceleration |
| **2012→2013** | **0.145** | **JPY -0.145** | **Abenomics transition** |
| **2021→2022** | **0.156** | **JPY -0.156** | **Japan-US policy divergence** |
| 2022→2023 | 0.103 | TRY +0.103 | Lira undervaluation easing |
| 2023→2024 | 0.102 | TRY +0.102 | Continued lira undervaluation easing |

Particularly, **2012→2013** and **2021→2022** are notable as structural transition points.

### 6.8.2 Lineage of Lead Currency

Progression of the "most overvalued currency" over 20 years:

- **2005-2014**: JPY (JPY-led period)
- **2015-present**: USD (USD-led period)

This changing of the guard is attributable to the **2012→2013 structural transition**.

---

## 6.9 Trajectory in Three-Currency Relative Space

### 6.9.1 Projection onto 2D Simplex

Due to the three-currency zero-sum constraint, (m[USD], m[JPY], m[TRY]) can be visualized as a trajectory on a 2D plane (see Chapter 4 for details).

**Major trajectory patterns**:

1. **2005-2012**: Stable structure with yen positioned at top of ring (overvalued side), lira at bottom (undervalued side)
2. **2012→2013**: Yen rapidly moves downward, dollar moves upward (changing of the guard)
3. **2013-2021**: Dollar settles at top, yen fluctuates in middle region
4. **2018**: Lira protrudes to extreme bottom of ring (most undervalued)
5. **2021→2022**: Dollar reaches extreme top of ring (most overvalued), yen plunges
6. **2022→2024**: Yen approaches near zero (ring center), lira gradually rises

### 6.9.2 Emergence of Structural Symmetry (2024)

**2024's** structure shows the following approximate symmetry:

```
m[USD] ≈ +0.48
m[JPY] ≈ 0
m[TRY] ≈ -0.48
```

This means the dollar and lira are **nearly symmetrically separated**, with the yen functioning as a **neutral reference point**.

This structure suggests that "bipolarization" within the three-currency basket has reached its extreme.

---

## 6.10 Implications of Regime Analysis

### 6.10.1 Regime Persistence and Transition Precursors

- **Regime I (JPY-led period)** persisted for approximately 7 years
- **Regime II (Transition period)** was a transitional phase of approximately 5 years
- **Regime III (USD-led period)** lasted approximately 4 years before moving to the next stage
- **Regime IV (Extreme USD high/JPY plunge period)** is currently ongoing (3rd year)

Precursors of regime transition can be detected as **sudden increases in year-over-year change magnitude** (|Δm[i]| > 0.10).

### 6.10.2 Correspondence Between Monetary Policy and Structural Change

Major regime transitions all correspond to **significant changes in central bank monetary policy**:

- **2013**: BOJ QQE begins → From JPY-led to USD-led
- **2022**: Fed rapid rate hikes vs. BOJ YCC maintenance → To extreme USD high/JPY plunge

This shows that the Mikan 3-Currency clr Index sensitively reflects relative monetary policy stances.

### 6.10.3 Independence of Emerging Market Currency (TRY)

The lira (TRY) was positioned on the **always undervalued side** throughout the entire observation period, showing independent movement from hard currencies (USD, JPY).

Particularly after 2018, it has been fixed in deep undervaluation territory with m[TRY] < -0.68, indicating continuing **structural vulnerability**.

### 6.10.4 Future Outlook

How the 2024 structure (extreme USD high / JPY neutral / TRY undervalued) will develop depends on the following factors:

1. **Continuation of Japan-US monetary policy convergence/divergence**
2. **Progress of Turkey's monetary policy normalization**
3. **Changes in global dollar supply/demand (DXY, etc.)**

Particularly, with the yen now neutralized, the next regime shift may occur in the form of the "USD vs. TRY" bipolar structure breaking down.

---

# Chapter 7: Practical Guidelines

## 7.1 Purpose of This Chapter

This chapter provides **practical guidelines** for using the Mikan 3-Currency clr Index in real-world applications. We discuss specific methods for investment decisions, risk management, and portfolio allocation, as well as operational considerations.

---

## 7.2 Basic Interpretation of the Index

$m[i] > 0$ indicates overvaluation, and $m[i] < 0$ indicates undervaluation (see Section 2.2 for details).

### 7.2.1 Importance of the Zero-Sum Constraint

The following relationship always holds:

$$
m[\text{USD}](t) + m[\text{JPY}](t) + m[\text{TRY}](t) = 0
$$

This guarantees the relative relationship that "if one currency becomes overvalued, other currencies become undervalued."

**Example (2024)**:
- m[USD] = +0.483 (overvalued)
- m[JPY] = -0.003 (neutral)
- m[TRY] = -0.480 (undervalued)
- Total = 0.000 ✓

The dollar being extremely overvalued means the lira is undervalued, with the yen in an intermediate position.

---

## 7.3 Application to Investment Decisions

### 7.3.1 Basic Investment Strategy

The basic strategy based on the Mikan 3-Currency clr Index follows the concept of **mean reversion**:

**Strategy Principles**:

1. **When $m_i(t)$ is largely positive (overvalued)** → Expected to revert to mean in the future → Consider **sell position**
2. **When $m_i(t)$ is largely negative (undervalued)** → Expected to revert to mean in the future → Consider **buy position**
3. **When $m_i(t) \approx 0$ (neutral)** → No position, or continue observation

### 7.3.2 Threshold Settings

Thresholds need to be set to determine "largely positive/negative." Recommended values based on 2005–2024 statistics (see Chapter 3):

| Currency | Mean | Std Dev | +1σ Threshold | +2σ Threshold | -1σ Threshold | -2σ Threshold |
|----------|------|---------|---------------|---------------|---------------|---------------|
| USD | +0.27 | 0.15 | +0.42 | +0.57 | +0.12 | -0.03 |
| JPY | +0.28 | 0.10 | +0.38 | +0.48 | +0.18 | +0.08 |
| TRY | -0.55 | 0.12 | -0.43 | -0.31 | -0.67 | -0.79 |

**Recommended Thresholds**:
- **Conservative strategy**: Take positions only when exceeding ±2σ
- **Aggressive strategy**: Take positions when exceeding ±1σ

### 7.3.3 Specific Signal Examples

#### Example 1: 2022 Dollar (Extremely Overvalued)

- **Situation**: m[USD] = +0.518 (+2.5σ above mean of +0.27)
- **Signal**: Sell dollar (sell USD/JPY, sell USD/TRY)
- **Rationale**: Historically extreme overvaluation level. Mean reversion expected
- **Actual outcome**: Decreased to +0.498 in 2023, +0.483 in 2024 (reversion began)

#### Example 2: 2020 Lira (Extremely Undervalued)

- **Situation**: m[TRY] = -0.781 (exceeding -2σ from mean of -0.55)
- **Signal**: Buy lira (buy TRY/JPY)?
- **Caution**: However, remained at -0.753 in 2021, -0.685 in 2022 (undervaluation continued)
- **Lesson**: When structural vulnerabilities exist, mean reversion may be delayed or fail to materialize

#### Example 3: 2024 Yen (Neutral)

- **Situation**: m[JPY] = -0.003 (approximately zero)
- **Signal**: Position unclear. Continue observation
- **Consideration**: While deviating downward from long-term mean (+0.28), neutral in absolute terms

### 7.3.4 Pair Trade Strategy

Pair trades utilizing **relative differences** among the three currencies:

**Strategy Example**: When m[USD] - m[JPY] is extremely large

- **2022**: m[USD] - m[JPY] = 0.518 - 0.167 = **+0.351**
- **Signal**: Sell USD/JPY (sell dollar, buy yen)
- **Rationale**: Expecting this spread to narrow (dollar weakening/yen strengthening, or both currencies becoming undervalued simultaneously)

**Notes**:
- Pair trades bet on **changes in the spread**, not absolute levels of either currency
- Profit is achieved if the spread narrows, even if both currencies become overvalued/undervalued simultaneously

---

## 7.4 Risk Management

### 7.4.1 Volatility Monitoring

The rate of change in $m_i(t)$ (Δm_i) indicates the speed of currency valuation changes.

**Distribution of Annual Rate of Change (Absolute Value) for 2005–2024**:

| Currency | Mean Change | Max Change | Max Change Year |
|----------|-------------|------------|-----------------|
| USD | 0.048 | 0.089 | 2021→2022 |
| JPY | 0.050 | 0.156 | 2021→2022 |
| TRY | 0.056 | 0.114 | 2008→2009 |

**Risk Management Guidelines**:

1. When **|Δm_i| > 0.10** occurs, high probability of regime transition → Reduce position size
2. **Consecutive large changes** (|Δm_i| > 0.08 for 2 consecutive years) suggest structural change → Review strategy

### 7.4.2 Stop-Loss Settings

Even in mean-reversion strategies, stop-losses are essential to limit losses.

**Recommended Settings**:

- **Close position if adverse movement exceeds +0.15**
- Example: After taking a dollar short position at m[USD] = +0.50, cut losses if m[USD] rises to +0.65

### 7.4.3 Leverage Limits

This method is based on annual data for long-term evaluation, and short-term movements in the opposite direction can be large.

**Recommended Leverage**:
- **When using annual data**: 1x to 2x
- **When using high-frequency data** (future extension): 2x to 5x

Excessive leverage increases the risk of forced liquidation before mean reversion is realized.

---

## 7.5 Portfolio Allocation

### 7.5.1 Basic Policy for Dynamic Allocation

Dynamically adjust currency exposure based on $m_i(t)$.

**Allocation Rules (Example)**:

1. **Undervalued currencies (m_i < -1σ)**: **Increase** weight
2. **Currencies in neutral zone (-1σ < m_i < +1σ)**: **Equal** weight
3. **Overvalued currencies (m_i > +1σ)**: **Reduce** weight

### 7.5.2 Specific Example: 3-Currency Diversified Investment

**2024 Situation**:
- m[USD] = +0.483 (+1.4σ, overvalued)
- m[JPY] = -0.003 (neutral)
- m[TRY] = -0.480 (+0.6σ, slightly undervalued)

**Allocation Proposal**:
- USD: 20% (low weight due to overvaluation)
- JPY: 40% (moderate due to neutral)
- TRY: 40% (moderate considering structural risk despite undervaluation)

**Note**: Although TRY is undervalued, avoid excessive concentration due to structural vulnerabilities (see Chapter 6).

### 7.5.3 Application to Hedging Strategies

When multinational corporations or institutional investors hedge currency risk, they can adjust hedge ratios with reference to $m_i(t)$.

**Hedge Ratio Adjustment Rules**:

| m_i Level | Hedge Ratio for Home Currency Exposure |
|-----------|----------------------------------------|
| m_i > +2σ (extremely overvalued) | 80%–100% (high hedge ratio) |
| +1σ < m_i < +2σ (overvalued) | 50%–80% |
| -1σ < m_i < +1σ (neutral zone) | 30%–50% (standard) |
| m_i < -1σ (undervalued) | 0%–30% (low hedge ratio) |

**Rationale**: Overvalued currencies have higher future depreciation risk, so increase hedge ratio. Undervalued currencies have appreciation potential, so reduce hedge ratio.

---

## 7.6 Timing Strategies

### 7.6.1 Entry Timing

**Conservative Approach**:
- After reaching extreme levels (±2σ), enter after **signs of reversal** appear
- Example of signs: Change in opposite direction from previous period (sign reversal of Δm_i)

**Aggressive Approach**:
- Enter immediately upon reaching ±1σ
- Captures more opportunities but higher drawdown risk

### 7.6.2 Exit Timing

**Profit Taking**:
- Take profit when m_i reverts to near the mean (mean ± 0.5σ)
- Example: Short entry at m[USD] = +0.50 → Take profit when it decreases to +0.35

**Stop Loss**:
- Cut losses when adverse movement exceeds a threshold (e.g., +0.15)
- Or review when fundamentals change (e.g., central bank policy shift)

### 7.6.3 Rebalancing Frequency

When using annual data, **annual rebalancing** is standard.

- **Timing**: After new year data publication (usually February–March)
- **When using high-frequency data** (future extension): Consider quarterly or monthly rebalancing

---

## 7.7 Combination with External Indicators

### 7.7.1 Importance of External Indicators

Since $m_i(t)$ shows "relative valuation within the three-currency basket," it cannot directly observe factors outside the basket. Therefore, combination with external indicators is important.

**External Indicators to Use Complementarily**:

| Indicator | Usage | Specific Example |
|-----------|-------|------------------|
| **DXY** (Dollar Index) | Global dollar strength/weakness | Correlation analysis with m[USD] |
| **VIX** (Fear Index) | Risk-on/off environment | Safe currency (JPY) tends to be overvalued when VIX is high |
| **Interest rate differentials** | Consistency with interest rate parity | Relationship between US-Japan rate differential and m[USD] - m[JPY] |
| **REER** (Real Effective Exchange Rate) | Comparison with other valuation criteria | Difference analysis between PPP-based and REER-based |

### 7.7.2 Example of Integrated Judgment

**2022 Dollar Strength Episode**:

1. **Mikan Index**: m[USD] = +0.518 (extremely overvalued) → Dollar sell signal
2. **DXY**: High level above 110 (global dollar strength)
3. **US-Japan interest rate differential**: +4% or more (supporting dollar strength)
4. **VIX**: Around 25 (risk-off environment)

**Integrated Judgment**:
- Mikan Index shows dollar overvaluation, but DXY and interest rate differentials support dollar strength
- Conflicting signals → **Reduce position size** or **continue observation**
- Actually, the dollar declined after late 2022 but maintained high levels through 2023–2024

**Lesson**: Even when $m_i(t)$ is extreme, if supported by external factors (interest rate differentials, etc.), mean reversion may be delayed.

---

## 7.8 Operational Considerations

### 7.8.1 Recognition of Method Limitations

Always keep the limitations of this method in mind:

1. **Annual data constraints**: Cannot capture short-term fluctuations
2. **Scope of this research**: This paper analyzes only 3 currencies (USD/JPY/TRY), excluding major currencies like EUR and CNY (theoretically extensible to N currencies where N≥3)
3. **PPP limitations**: Short-term exchange rate determinants (interest rate differentials, risk sentiment, etc.) are not directly reflected
4. **Uncertainty of mean reversion**: Mean reversion may not materialize when structural changes occur

### 7.8.2 Necessity of Backtesting

The strategies presented in this chapter are **theoretical proposals**, and actual performance has not been verified.

**Essential before live trading**:
- Backtesting with historical data
- Profitability verification including transaction costs (spreads, commissions)
- Evaluation of maximum drawdown and Sharpe ratio

### 7.8.3 Response to Structural Changes

When regime transitions occur (see Chapter 6), past means and standard deviations may become unreliable.

**Countermeasures**:
- **Moving average/standard deviation**: Update statistics using rolling windows such as the most recent 10 years
- **Regime detection**: When |Δm_i| > 0.10 occurs, pause strategy and review

### 7.8.4 Liquidity Considerations

This research assumes trading in USD/JPY, USD/TRY, and TRY/JPY, but liquidity varies.

**Liquidity Reality**:
- **USD/JPY**: World's second-highest liquidity, minimal spread
- **USD/TRY**: Limited liquidity as an emerging market currency pair, large spread
- **TRY/JPY**: Minor currency pair, low liquidity, very large spread

**Countermeasures**:
- Limit position size for low-liquidity pairs (TRY/JPY)
- Use limit orders to avoid unfavorable slippage

### 7.8.5 Geopolitical Risks

Emerging market currencies like TRY are strongly affected by geopolitical risks (political instability, deteriorating foreign relations, etc.).

**Lessons from the 2018 Lira Crisis**:
- Even when $m[\text{TRY}]$ was undervalued, further collapse occurred due to political risks
- Also confirm deterioration of fundamentals (high inflation, current account deficit, declining foreign reserves)

**Response**:
- Limit exposure to emerging market currencies to 10–20% of total assets
- Regularly reassess country risk

---

## 7.9 Practical Operation Flow

### 7.9.1 Monthly Monitoring (When Using Annual Data)

**Step 1: Data Update**
- Obtain latest PPP and exchange rate data from World Bank (published annually, usually February–March)
- Calculate $m_i(t)$ for the latest year

**Step 2: Statistics Update**
- Recalculate mean and standard deviation for the most recent 10 years or entire period
- Update ±1σ and ±2σ thresholds

**Step 3: Signal Determination**
- Check if each currency exceeds thresholds
- Calculate year-over-year change (Δm_i) to detect signs of regime transition

**Step 4: External Indicator Confirmation**
- Check external indicators such as DXY, VIX, interest rate differentials
- Verify consistency with Mikan Index signals

**Step 5: Position Adjustment**
- Adjust positions or portfolio weights based on signals
- Operate within risk limits (leverage, maximum drawdown)

**Step 6: Recording and Evaluation**
- Record adjustments
- Evaluate performance quarterly

### 7.9.2 Daily Monitoring (When Using High-Frequency Data)

Operation flow when extended to daily data in the future:

**Step 1: Daily Data Update**
- Obtain daily exchange rates, calculate $m_i(t)$ daily

**Step 2: Update Moving Statistics**
- Calculate 60-day moving average, 20-day volatility, etc.

**Step 3: Daily Signals**
- Alert when $m_i(t)$ exceeds moving average ± 2 standard deviations

**Step 4: Entry/Exit Decisions**
- After alert, confirm external and technical indicators before entering
- Exit upon reaching target or stop-loss

---

## 7.10 Case Study: 2022–2024 Trading Simulation

### 7.10.1 Initial Situation (Early 2022)

**End of 2021 State**:
- m[USD] = +0.429 (above +1σ, overvalued)
- m[JPY] = +0.323 (slightly overvalued)
- m[TRY] = -0.753 (-1.7σ, undervalued)

**Strategy**:
- USD: Overvalued → Reduce weight (20%)
- JPY: Slightly overvalued → Standard weight (40%)
- TRY: Undervalued → Increase weight (40%)

### 7.10.2 Changes in 2022

**End of 2022 State**:
- m[USD] = +0.518 (+1.7σ, extremely overvalued)
- m[JPY] = +0.167 (slightly overvalued but significant decline)
- m[TRY] = -0.685 (-1.1σ, undervaluation continues)

**Analysis of Changes**:
- USD became even more overvalued (Δm[USD] = +0.089) → Sign of regime transition
- JPY declined significantly (Δm[JPY] = -0.156) → Structural change

**Strategy Adjustment**:
- USD: Extremely overvalued → Consider short position or further reduce weight to 10%
- JPY: Sharp decline but still positive → Maintain weight
- TRY: Undervaluation continues but improving trend → Maintain weight

### 7.10.3 Results for 2023–2024

**End of 2024 State**:
- m[USD] = +0.483 (+1.4σ, overvaluation continues)
- m[JPY] = -0.003 (approximately zero, neutralized)
- m[TRY] = -0.480 (+0.6σ, undervaluation eased)

**Evaluation of Results**:
- USD: +0.518 → +0.483 (-0.035 decrease) → Signs of mean reversion
- JPY: +0.167 → -0.003 (-0.170 decrease) → Significant structural change
- TRY: -0.685 → -0.480 (+0.205 increase) → Undervaluation significantly improved

**Performance Estimate** (approximate):
- **TRY weight increase strategy**: Profit from TRY's relative appreciation
- **USD weight reduction strategy**: Loss avoidance from USD's relative decline
- **Overall**: Exposure to TRY drove performance

**Lessons**:
- Mean reversion from extreme levels was realized but took 2 years (patience required)
- JPY's sharp decline was an unexpected structural change; external factors (US-Japan interest rate differential) should not have been overlooked

---

## 7.11 Summary: Message to Practitioners

The Mikan 3-Currency clr Index is a new tool for currency valuation in a multi-currency environment. For practical use, keep the following points in mind:

### 7.11.1 Strengths

1. **Consistent multi-currency evaluation**: Expresses relative relationships among three currencies under the zero-sum constraint
2. **Intuitive visualization**: Trajectories in 2-dimensional space make structural changes easy to grasp
3. **Economic validity**: Consistent with major economic events (yen appreciation, lira crisis, dollar strength)

### 7.11.2 Weaknesses

1. **Time resolution constraints**: Annual data is unsuitable for short-term investment decisions
2. **Scope of this research**: This paper covers only 3 currencies (USD/JPY/TRY) and does not represent the global currency environment (theory is extensible to N currencies)
3. **Uncertainty of mean reversion**: When structural changes occur, reversion may be delayed or fail to materialize

### 7.11.3 Recommended Usage

- Use as a reference indicator for **long-term strategic asset allocation**
- **Combine with external indicators (DXY, interest rate differentials, VIX, etc.)** for comprehensive judgment
- **Conduct backtesting** before live trading
- Consider **extension to high-frequency data** (daily, monthly) to enhance practicality

### 7.11.4 Future Development Expectations

The operational guidelines presented in this chapter are preliminary proposals based on annual data. Future extensions to daily/monthly data, expansion to 4 or more currencies, and construction of predictive models using machine learning will dramatically improve practical usefulness.

Ultimately, we hope that the Mikan 3-Currency clr Index will be established as a **standard monitoring tool** for foreign exchange market practitioners.

---

# Chapter 8: Monthly Analysis and PPP Update Frequency

## 8.1 Significance of Monthly Observation

Chapter 4 analyzed long-term structural changes based on annual data. The 20-year graph (Figure 8.0) shown below captures major structural changes: the 2011 yen appreciation peak, the 2018 Turkish lira crisis, and the 2022 dollar strength period.

![Annual MCI Coordinate Progression (2005-2024)](annual_mci_plot.png)

*Figure 8.0: Annual MCI coordinate progression (reproduced from Chapter 4). Long-term trends over 20 years can be grasped, but detailed dynamics of recent years are difficult to read.*

However, for actual market participants, capturing movements on shorter time scales is important. The figure above compresses movements since 2022, making it insufficient for analyzing monthly dynamics. This chapter uses monthly data from 2022 to 2025 to analyze short-term dynamics of MCI coordinates.

Monthly observation reveals:
1. Short-term stress accumulation/release processes smoothed out in annual data
2. Structural response speed to market events
3. Leading movements signaling regime transitions

---

## 8.2 Monthly MCI Using Annual PPP

The figure below shows monthly MCI coordinates from January 2022 to November 2025, using each year's confirmed PPP values (IMF WEO).

![Monthly MCI (Annual PPP)](monthly_mci_annual_ppp.png)

*Figure 8.1: Monthly MCI coordinate progression using annual PPP. Orange dotted lines indicate year boundaries (PPP update timing).*

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

![Monthly MCI (Interpolated PPP)](monthly_mci_interpolated_ppp.png)

*Figure 8.2: MCI coordinate progression using monthly interpolated PPP. Year-boundary jumps are eliminated, showing smooth transitions.*

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

## 8.6 Estimating Future Price Ranges Using Monthly MCI

### Boundedness and Statistical Estimation Possibility

An important mathematical property of the Mikan 3-Currency clr Index is **boundedness**. While actual exchange rates can theoretically fluctuate in the range $0 \to \infty$, making direct estimation of future fluctuation ranges difficult, the $m[i]$ coordinates are mapped into a mathematically constrained space due to the zero-sum constraint (Equation 1).

The observed ranges of $m[i]$ in monthly interpolated data (January 2022 to November 2025, 47 months) are as follows:

| Currency | Observed Range | Range Width | Average |
|----------|---------------|-------------|---------|
| USD | [+0.392, +0.597] | 0.205 | +0.484 |
| JPY | [-0.100, +0.195] | 0.295 | +0.056 |
| TRY | [-0.596, -0.304] | 0.292 | -0.539 |

This observed range is more limited compared to the approximately $\pm 0.8$ range observed in annual data (20 years). Monthly-level fluctuations are moderate when excluding PPP jumps:

| Currency | Max Monthly Rise | Max Monthly Fall | Average Monthly Change |
|----------|-----------------|------------------|----------------------|
| USD | +0.059 | -0.028 | 0.010 |
| JPY | +0.051 | -0.054 | 0.017 |
| TRY | +0.046 | -0.079 | 0.016 |

This boundedness suggests the possibility of calculating the short-term theoretical range of motion for $m[i]$ using statistical methods.

### Reverse Calculation for Target Price Setting

By making assumptions about future values of $m[i]$, future exchange rates can be estimated using the following reverse calculation formula:

$$
S_{\text{A/B,future}} = \text{PPP}_{\text{A/B,future}} \times \exp(m[A]_{\text{target}} - m[B]_{\text{target}})
$$

Where:
- $\text{PPP}_{\text{future}}$ can be estimated from inflation rate forecasts for each country
- $m[i]_{\text{target}}$ is set from current trend extrapolation or statistical ranges

This method enables estimation of future price ranges based on statistical evidence, going beyond mere ex-post evaluation.

### Practical Example: USD/JPY Price Range Estimation for December 2025

**Current Status (as of November 2025)**:

The latest MCI coordinates (November 2025) using monthly interpolated PPP are as follows:

- $m[\text{USD}] = +0.404$ (maintaining overvaluation)
- $m[\text{JPY}] = -0.100$ (undervalued side)
- $m[\text{TRY}] = -0.304$ (undervalued but improving trend)

**Trend Analysis**:

The momentum observed from monthly data since 2023 is as follows:

- **USD**: Gradually declining from peak of +0.60 in 2022, hovering around +0.40 since latter half of 2024
- **JPY**: Continuously declining from +0.15 in 2023, reaching -0.10 in 2025 with slight continued decline
- **TRY**: Converging trend from -0.60 in 2022, improving to -0.30 as of November 2025

**Scenario Setting**:

Assuming current momentum is maintained until December 2025, the following scenarios are set:

| Scenario | m[USD] | m[JPY] | m[TRY] | Rationale |
|----------|--------|--------|--------|-----------|
| **A (Momentum Maintenance)** | +0.40 | -0.11 | -0.29 | Continuation of current trends (USD flat, JPY slight decline, TRY convergence) |
| **B (Accelerated Convergence)** | +0.38 | -0.13 | -0.25 | Overall accelerated convergence toward neutral |
| **C (Momentum Reversal)** | +0.42 | -0.08 | -0.34 | USD slight increase, JPY slight recovery, TRY rebound |

**PPP Estimation Setting**:

PPP estimates for December 2025 are set as follows (considering current values and remaining one month of inflation):

- $\text{PPP}_{\text{USDJPY, December 2025}} \approx 93.3$ (November 2025: 93.2, assuming near-flat)
- $\text{PPP}_{\text{USDTRY, December 2025}} \approx 21.2$ (November 2025: 20.8, Turkish inflation continuing)

**USD/JPY Price Range Estimation**:

The USD/JPY estimates for each scenario are as follows:

$$
\begin{align}
\text{Scenario A}: \quad S_{\text{USDJPY}} &= 93.3 \times \exp(0.40 - (-0.11)) = 93.3 \times \exp(0.51) \approx 156 \\
\text{Scenario B}: \quad S_{\text{USDJPY}} &= 93.3 \times \exp(0.38 - (-0.13)) = 93.3 \times \exp(0.51) \approx 156 \\
\text{Scenario C}: \quad S_{\text{USDJPY}} &= 93.3 \times \exp(0.42 - (-0.08)) = 93.3 \times \exp(0.50) \approx 154
\end{align}
$$

**Consideration of Statistical Fluctuation Range**:

Considering typical fluctuation ranges in monthly data (approximately $\pm 0.05$) and assuming $m[\text{USD}] - m[\text{JPY}] \in [0.46, 0.56]$, the theoretical fluctuation range for USD/JPY is:

$$
\begin{align}
\text{Lower bound}: \quad S_{\text{USDJPY}} &= 93.3 \times \exp(0.46) \approx 148 \\
\text{Upper bound}: \quad S_{\text{USDJPY}} &= 93.3 \times \exp(0.56) \approx 158
\end{align}
$$

Therefore, considering the statistical range of monthly fluctuations, USD/JPY for December 2025 is estimated to fluctuate **within the range of 148-158 yen**. The central scenario is approximately 155 yen.

### Limitations and Caveats

This method is based on the following assumptions, and loses validity if these are violated:

1. **Momentum Maintenance**: Assumes current trends continue. If regime shifts (see Chapter 6) occur, $m[i]$ momentum breaks down
2. **PPP Estimation Accuracy**: Future PPP depends on inflation rate forecasts, so estimation accuracy declines with sudden inflation rate changes
3. **Absence of Exogenous Shocks**: Exogenous shocks such as geopolitical crises or sudden monetary policy shifts are not captured by this model
4. **Basket-Internal Limitation**: This estimation only reflects relative relationships within the 3-currency basket and does not consider factors outside the basket (e.g., EUR, CNY movements)
5. **Short-term Forecast Limitations**: This method assumes short-term forecasts of 1-3 months, with uncertainty increasing for longer-term forecasts

Therefore, this method should be positioned as a **short-term structural analysis auxiliary tool**, and for actual trading decisions, combination with external indicators (DXY, interest rate differentials, VIX, etc.) mentioned in Chapter 7 is essential.

### Summary

Estimating future price ranges using monthly MCI yielded the following insights:

1. **Boundedness**: $m[i]$ fluctuates moderately at the monthly level (average 0.01-0.02/month), enabling calculation of short-term ranges using statistical methods
2. **Reverse Calculation for Target Price Setting**: Theoretical ranges of exchange rates can be derived from assumed values of $m[i]$ and future PPP
3. **Practical Application**: The estimated range for USD/JPY in December 2025 is 148-158 yen (center 155 yen)
4. **Positioning as Short-term Forecast Tool**: This method is applicable to short-term forecasts of 1-3 months but assumes combination with external indicators and loses validity during regime transitions

This analytical approach demonstrates that the Mikan 3-Currency clr Index is not merely a retrospective evaluation tool but has aspects as a framework for short-term future analysis based on statistical evidence.

---

## 8.7 Chapter Summary

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

4. **Sarno, L., & Taylor, M. P. (2002).** *The Economics of Exchange Rates*. Cambridge University Press.
   - Comprehensive textbook on exchange rate determination theory

## Compositional Data Analysis (CoDA)

5. **Aitchison, J. (1986).** *The Statistical Analysis of Compositional Data*. Chapman & Hall.
   - Classic monograph establishing the foundations of compositional data analysis

6. **Pawlowsky-Glahn, V., & Egozcue, J. J. (2006).** "Compositional Data and Their Analysis: An Introduction," *Geological Society, London, Special Publications*, 264(1), 1–10.
   - Modern introductory paper on compositional data analysis

7. **Filzmoser, P., Hron, K., & Templ, M. (2018).** *Applied Compositional Data Analysis: With Worked Examples in R*. Springer.
   - Practical textbook on compositional data analysis using R

8. **Egozcue, J. J., Pawlowsky-Glahn, V., Mateu-Figueras, G., & Barceló-Vidal, C. (2003).** "Isometric Logratio Transformations for Compositional Data Analysis," *Mathematical Geology*, 35(3), 279–300.
   - Mathematical foundations of log-ratio transformations including clr (centered log-ratio)

## Real Effective Exchange Rates (REER) and Currency Valuation

9. **Chinn, M. D. (2006).** "A Primer on Real Effective Exchange Rates: Determinants, Overvaluation, Trade Flows and Competitive Devaluation," *Open Economies Review*, 17(1), 115–143.
   - Survey of REER definition, determinants, and empirical analysis

10. **Comunale, M., & Hessel, J. (2014).** "Current Account Imbalances in the Euro Area: Competitiveness or Financial Center?" DNB Working Paper No. 443.
    - Research on competitiveness indicator construction in multi-currency environments

## Time Series Analysis and Regime Switching

11. **Hamilton, J. D. (1989).** "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle," *Econometrica*, 57(2), 357–384.
    - Proposal of Markov-switching models (foundation for regime transition analysis)

12. **Perron, P. (1989).** "The Great Crash, the Oil Price Shock, and the Unit Root Hypothesis," *Econometrica*, 57(6), 1361–1401.
    - Testing methods for time series data with structural breaks

13. **Stock, J. H., & Watson, M. W. (2001).** "Vector Autoregressions," *Journal of Economic Perspectives*, 15(4), 101–115.
    - Explanation of VAR models and their application to economic analysis

## Currency Crises and Emerging Markets

14. **Kaminsky, G. L., & Reinhart, C. M. (1999).** "The Twin Crises: The Causes of Banking and Balance-of-Payments Problems," *American Economic Review*, 89(3), 473–500.
    - Influential paper analyzing the relationship between currency crises and banking crises

15. **Eichengreen, B., Rose, A. K., & Wyplosz, C. (1996).** "Contagious Currency Crises," NBER Working Paper No. 5681.
    - Research on transmission mechanisms of currency crises

16. **Özatay, F., & Sak, G. (2003).** "The 2000–2001 Financial Crisis in Turkey," in *Managing Currency Crises in Emerging Markets*, University of Chicago Press, 157–184.
    - Detailed analysis of Turkey's currency crisis (period prior to this study)

## Japanese Economy and Yen Appreciation

17. **Shirakawa, M. (2012).** "Deleveraging and Growth: Is the Developed World Following Japan's Long and Winding Road?" Lecture at the London School of Economics.
    - Analysis of the Japanese economy including the 2011 extreme yen appreciation period by the then-BOJ Governor

18. **Ito, T., & Mishkin, F. S. (2006).** "Two Decades of Japanese Monetary Policy and the Deflation Problem," in *Monetary Policy with Very Low Inflation in the Pacific Rim*, University of Chicago Press, 131–202.
    - Long-term analysis of Japanese monetary policy and yen appreciation/deflation

## Data Sources

19. **World Bank (2024).** *World Development Indicators (WDI)*. https://databank.worldbank.org/source/world-development-indicators
    - Primary source for PPP and exchange rate data used in this study
    - Indicators: PA.NUS.PPP (PPP conversion factor, GDP), PA.NUS.FCRF (Official exchange rate)

20. **Bank for International Settlements (BIS) (2024).** *Effective Exchange Rate Indices*. https://www.bis.org/statistics/eer.htm
    - Standard source for Real Effective Exchange Rate (REER) data

21. **International Monetary Fund (IMF) (2024).** *International Financial Statistics (IFS)*. https://data.imf.org/
    - Comprehensive database for exchange rates and financial statistics

## Visualization and Statistical Methods

22. **Cleveland, W. S., & McGill, R. (1984).** "Graphical Perception: Theory, Experimentation, and Application to the Development of Graphical Methods," *Journal of the American Statistical Association*, 79(387), 531–554.
    - Theoretical foundations of data visualization

23. **Tukey, J. W. (1977).** *Exploratory Data Analysis*. Addison-Wesley.
    - Classic text on exploratory data analysis

## International Finance and Exchange Policy

24. **Obstfeld, M., & Rogoff, K. (1996).** *Foundations of International Macroeconomics*. MIT Press.
    - Standard textbook on international macroeconomics

25. **Frankel, J. A., & Rose, A. K. (1995).** "Empirical Research on Nominal Exchange Rates," in *Handbook of International Economics*, Vol. 3, Elsevier, 1689–1729.
    - Comprehensive survey of empirical research on exchange rates

## Monetary Policy and Central Banks

26. **Clarida, R., Galí, J., & Gertler, M. (1999).** "The Science of Monetary Policy: A New Keynesian Perspective," *Journal of Economic Literature*, 37(4), 1661–1707.
    - Theoretical framework of modern monetary policy

27. **Bernanke, B. S., & Mishkin, F. S. (1997).** "Inflation Targeting: A New Framework for Monetary Policy?" *Journal of Economic Perspectives*, 11(2), 97–116.
    - Theory and practice of inflation targeting

## Risk Management and Portfolio Theory

28. **Markowitz, H. (1952).** "Portfolio Selection," *Journal of Finance*, 7(1), 77–91.
    - Classic paper establishing the foundations of modern portfolio theory

29. **Jorion, P. (2006).** *Value at Risk: The New Benchmark for Managing Financial Risk* (3rd ed.). McGraw-Hill.
    - Practical textbook on risk management centered on VaR

## Machine Learning and Time Series Forecasting

30. **Hochreiter, S., & Schmidhuber, J. (1997).** "Long Short-Term Memory," *Neural Computation*, 9(8), 1735–1780.
    - Proposal of LSTM (Long Short-Term Memory) networks (mentioned as future extension in Chapter 8)

31. **Vaswani, A., et al. (2017).** "Attention Is All You Need," in *Advances in Neural Information Processing Systems*, 5998–6008.
    - Proposal of Transformer models (potential application to time series forecasting)

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
- **Future Extensions**: Including recent literature on machine learning (LSTM, Transformer)
