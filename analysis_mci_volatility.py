#!/usr/bin/env python3
"""
MCIを使った変動限界分析
ユーザーの提案した「深度」分類の妥当性を検証
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# データ読み込み
df = pd.read_csv('dataset/mikan_3currency_clr_index_ppp_data.csv')

# 年次変動を計算
df['D_mUSD'] = df['m_USD'].diff()
df['D_mJPY'] = df['m_JPY'].diff()
df['D_mTRY'] = df['m_TRY'].diff()

print("=" * 80)
print("MCI変動限界分析レポート")
print("=" * 80)
print()

# ===== m[TRY]の年次変動統計 =====
print("1. m[TRY]の年次変動 (D) の統計")
print("-" * 80)
D_TRY = df['D_mTRY'].dropna()
print(f"平均: {D_TRY.mean():.6f}")
print(f"標準偏差: {D_TRY.std():.6f}")
print(f"最小値: {D_TRY.min():.6f} ({df.loc[D_TRY.idxmin(), 'year']:.0f}年)")
print(f"最大値: {D_TRY.max():.6f} ({df.loc[D_TRY.idxmax(), 'year']:.0f}年)")
print(f"中央値: {D_TRY.median():.6f}")
print()

# ===== 深度分類の検証 =====
print("2. 深度分類の検証（下落方向のみ）")
print("-" * 80)

# 下落のみを抽出
D_TRY_decline = D_TRY[D_TRY < 0]

depth1 = D_TRY_decline[(D_TRY_decline >= -0.06) & (D_TRY_decline < -0.05)]
depth2 = D_TRY_decline[(D_TRY_decline >= -0.08) & (D_TRY_decline < -0.06)]
depth3 = D_TRY_decline[D_TRY_decline < -0.08]

print(f"深度1 (-0.05 ~ -0.06): {len(depth1)}回")
for idx in depth1.index:
    print(f"  {df.loc[idx, 'year']:.0f}年: {df.loc[idx, 'D_mTRY']:.6f}")

print(f"\n深度2 (-0.06 ~ -0.08): {len(depth2)}回")
for idx in depth2.index:
    print(f"  {df.loc[idx, 'year']:.0f}年: {df.loc[idx, 'D_mTRY']:.6f}")

print(f"\n深度3 (-0.08以下): {len(depth3)}回")
for idx in depth3.index:
    print(f"  {df.loc[idx, 'year']:.0f}年: {df.loc[idx, 'D_mTRY']:.6f} ← リーマンショック")

print()

# ===== パーセンタイル分析 =====
print("3. m[TRY]年次変動のパーセンタイル（下落方向）")
print("-" * 80)
percentiles = [10, 25, 50, 75, 90, 95, 99]
for p in percentiles:
    val = np.percentile(D_TRY_decline, 100-p)  # 下落なので逆向き
    print(f"{p}パーセンタイル: {val:.6f}")
print()

# ===== ゼロサム性の検証 =====
print("4. ゼロサム性の検証 (m[USD] + m[JPY] + m[TRY] = 0)")
print("-" * 80)
df['sum_m'] = df['m_USD'] + df['m_JPY'] + df['m_TRY']
print(f"最大誤差: {df['sum_m'].abs().max():.2e}")
print(f"平均誤差: {df['sum_m'].abs().mean():.2e}")
print("→ ゼロサム制約は厳密に満たされている")
print()

# ===== 逆算：特定のm[TRY]変動に必要なレート変動 =====
print("5. 逆算分析：m[TRY] = -0.06 の変動に必要なレート変動")
print("-" * 80)
print("公式: m[TRY] = (d_USDJPY - 2*d_USDTRY) / 3")
print("ゼロサム: m[USD] + m[JPY] + m[TRY] = 0")
print()

# 現在値（2024年）
current = df[df['year'] == 2024].iloc[0]
m_TRY_current = current['m_TRY']
m_USD_current = current['m_USD']
m_JPY_current = current['m_JPY']
d_UJ_current = current['d_USDJPY']
d_UT_current = current['d_USDTRY']

print(f"2024年現在値:")
print(f"  m[TRY] = {m_TRY_current:.6f}")
print(f"  m[USD] = {m_USD_current:.6f}")
print(f"  m[JPY] = {m_JPY_current:.6f}")
print(f"  d_USDJPY = {d_UJ_current:.6f}")
print(f"  d_USDTRY = {d_UT_current:.6f}")
print()

# 構造破綻ライン：m[TRY]が-0.06下落
target_D_mTRY = -0.06
target_m_TRY = m_TRY_current + target_D_mTRY

print(f"構造破綻ライン到達時:")
print(f"  m[TRY] = {target_m_TRY:.6f} (変動: {target_D_mTRY:.3f})")
print()

# ユーザーの配分仮説：円65%、ドル35%
# m[TRY]の変動 = -0.06なので、m[USD] + m[JPY]の変動 = +0.06 (ゼロサム)
# 配分: Δm[JPY] = +0.06 * 0.65, Δm[USD] = +0.06 * 0.35

D_m_JPY = 0.06 * 0.65
D_m_USD = 0.06 * 0.35

new_m_JPY = m_JPY_current + D_m_JPY
new_m_USD = m_USD_current + D_m_USD
new_m_TRY = target_m_TRY

print(f"シナリオA：ユーザー提案配分 (円65%、ドル35%)")
print(f"  Δm[JPY] = +{D_m_JPY:.6f}")
print(f"  Δm[USD] = +{D_m_USD:.6f}")
print(f"  Δm[TRY] = {target_D_mTRY:.6f}")
print()
print(f"  新しい座標:")
print(f"    m[USD] = {new_m_USD:.6f}")
print(f"    m[JPY] = {new_m_JPY:.6f}")
print(f"    m[TRY] = {new_m_TRY:.6f}")
print(f"    合計 = {new_m_USD + new_m_JPY + new_m_TRY:.6f}")
print()

# 逆算：d_USDJPY, d_USDTRYを求める
# m[USD] = (d_UJ + d_UT) / 3
# m[JPY] = (-2*d_UJ + d_UT) / 3
# m[TRY] = (d_UJ - 2*d_UT) / 3

# 逆変換行列を使う
# d_UJ = m[USD] - m[JPY]
# d_UT = m[USD] - m[TRY]

new_d_UJ = new_m_USD - new_m_JPY
new_d_UT = new_m_USD - new_m_TRY

print(f"  必要なPPP乖離:")
print(f"    d_USDJPY = {new_d_UJ:.6f} (現在: {d_UJ_current:.6f}, 変化: {new_d_UJ - d_UJ_current:.6f})")
print(f"    d_USDTRY = {new_d_UT:.6f} (現在: {d_UT_current:.6f}, 変化: {new_d_UT - d_UT_current:.6f})")
print()

# レート換算（概算）
# d = ln(S / PPP) なので S = PPP * exp(d)
S_USDJPY_current = current['S_USDJPY']
S_USDTRY_current = current['S_USDTRY']
PPP_JPY_current = current['PPP_JPY']
PPP_TRY_current = current['PPP_TRY']

new_S_USDJPY = PPP_JPY_current * np.exp(new_d_UJ)
new_S_USDTRY = PPP_TRY_current * np.exp(new_d_UT)

print(f"  必要な為替レート（概算）:")
print(f"    USD/JPY = {new_S_USDJPY:.2f} (現在: {S_USDJPY_current:.2f}, 変化: {((new_S_USDJPY/S_USDJPY_current - 1) * 100):.2f}%)")
print(f"    USD/TRY = {new_S_USDTRY:.2f} (現在: {S_USDTRY_current:.2f}, 変化: {((new_S_USDTRY/S_USDTRY_current - 1) * 100):.2f}%)")
print()

# TRY/JPY（クロスレート）
new_S_TRYJPY = new_S_USDJPY / new_S_USDTRY
S_TRYJPY_current = current['S_TRYJPY']

print(f"    TRY/JPY = {new_S_TRYJPY:.4f} (現在: {S_TRYJPY_current:.4f}, 変化: {((new_S_TRYJPY/S_TRYJPY_current - 1) * 100):.2f}%)")
print()

# ===== 極限ケース：m[TRY] = -1 =====
print("6. 理論的極限ケース：m[TRY] = -1 に到達するには？")
print("-" * 80)

extreme_m_TRY = -1.0
# m[USD] + m[JPY] = 1.0 (ゼロサム)
# いくつかのシナリオ

scenarios = [
    ("ドル単独上昇", 1.0, 0.0),
    ("円単独上昇", 0.0, 1.0),
    ("ユーザー配分 (35%/65%)", 0.35, 0.65),
]

for name, ratio_USD, ratio_JPY in scenarios:
    extreme_m_USD = m_USD_current + 1.0 * ratio_USD
    extreme_m_JPY = m_JPY_current + 1.0 * ratio_JPY

    extreme_d_UJ = extreme_m_USD - extreme_m_JPY
    extreme_d_UT = extreme_m_USD - extreme_m_TRY

    extreme_S_USDJPY = PPP_JPY_current * np.exp(extreme_d_UJ)
    extreme_S_USDTRY = PPP_TRY_current * np.exp(extreme_d_UT)
    extreme_S_TRYJPY = extreme_S_USDJPY / extreme_S_USDTRY

    print(f"\n{name}:")
    print(f"  m座標: USD={extreme_m_USD:.3f}, JPY={extreme_m_JPY:.3f}, TRY={extreme_m_TRY:.3f}")
    print(f"  USD/JPY = {extreme_S_USDJPY:.2f}, USD/TRY = {extreme_S_USDTRY:.2f}, TRY/JPY = {extreme_S_TRYJPY:.4f}")

print()
print("=" * 80)

# ===== 可視化 =====
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. m[TRY]の時系列
ax1 = axes[0, 0]
ax1.plot(df['year'], df['m_TRY'], marker='o', linewidth=2)
ax1.axhline(y=-0.5, color='orange', linestyle='--', alpha=0.5, label='通常域')
ax1.axhline(y=-0.7, color='red', linestyle='--', alpha=0.5, label='危機域')
ax1.axhline(y=-1.0, color='darkred', linestyle='--', alpha=0.5, label='理論的限界')
ax1.set_xlabel('Year')
ax1.set_ylabel('m[TRY]')
ax1.set_title('m[TRY] 時系列（PPP座標）')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2. 年次変動Dの分布
ax2 = axes[0, 1]
ax2.hist(D_TRY, bins=15, edgecolor='black', alpha=0.7)
ax2.axvline(x=-0.06, color='orange', linestyle='--', linewidth=2, label='深度1下限 (-0.06)')
ax2.axvline(x=-0.08, color='red', linestyle='--', linewidth=2, label='深度2 (-0.08)')
ax2.axvline(x=-0.114, color='darkred', linestyle='--', linewidth=2, label='深度3 (-0.114)')
ax2.set_xlabel('年次変動 D (m[TRY])')
ax2.set_ylabel('頻度')
ax2.set_title('m[TRY] 年次変動の分布')
ax2.legend()
ax2.grid(True, alpha=0.3)

# 3. 三通貨座標の時系列
ax3 = axes[1, 0]
ax3.plot(df['year'], df['m_USD'], marker='o', label='USD', linewidth=2)
ax3.plot(df['year'], df['m_JPY'], marker='s', label='JPY', linewidth=2)
ax3.plot(df['year'], df['m_TRY'], marker='^', label='TRY', linewidth=2)
ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)
ax3.set_xlabel('Year')
ax3.set_ylabel('m[i]')
ax3.set_title('三通貨座標の時系列（ゼロサム）')
ax3.legend()
ax3.grid(True, alpha=0.3)

# 4. 年次変動の時系列
ax4 = axes[1, 1]
ax4.plot(df['year'][1:], df['D_mTRY'][1:], marker='o', linewidth=2, color='purple')
ax4.axhline(y=0, color='black', linestyle='-', alpha=0.3)
ax4.axhline(y=-0.06, color='orange', linestyle='--', alpha=0.5, label='深度1')
ax4.axhline(y=-0.08, color='red', linestyle='--', alpha=0.5, label='深度2')
# 特定年をハイライト
highlight_years = {2009: 'リーマン', 2018: 'トルコ'}
for year, label in highlight_years.items():
    idx = df[df['year'] == year].index[0]
    if idx > 0:
        ax4.plot(year, df.loc[idx, 'D_mTRY'], 'ro', markersize=10)
        ax4.annotate(label, (year, df.loc[idx, 'D_mTRY']),
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7))
ax4.set_xlabel('Year')
ax4.set_ylabel('D (年次変動)')
ax4.set_title('m[TRY] 年次変動の推移')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('mci_volatility_analysis.png', dpi=300, bbox_inches='tight')
print(f"グラフを保存しました: mci_volatility_analysis.png")
