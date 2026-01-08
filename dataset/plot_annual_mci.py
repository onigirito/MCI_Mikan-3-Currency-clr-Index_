#!/usr/bin/env python3
"""
年次MCIグラフ生成（モノクロ版）

annual_mci_2005_2024.csvから年次MCI座標のグラフを生成
論文の図4.1および図8.0で使用
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# フォント設定
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# データ読み込み
df = pd.read_csv('annual_mci_2005_2024.csv')
df['year'] = pd.to_datetime(df['year'].astype(str) + '-01-01')

# プロット
fig, ax = plt.subplots(figsize=(12, 6))

# モノクロで判読可能なスタイル
ax.plot(df['year'], df['m_USD'], 'o', label='m[USD]', linewidth=2, markersize=6,
        color='black', linestyle='-', markerfacecolor='white', markeredgewidth=1.5, markeredgecolor='black')
ax.plot(df['year'], df['m_JPY'], 's', label='m[JPY]', linewidth=2, markersize=6,
        color='black', linestyle='--', markerfacecolor='black', markeredgewidth=1.5)
ax.plot(df['year'], df['m_TRY'], '^', label='m[TRY]', linewidth=2, markersize=6,
        color='black', linestyle=':', markerfacecolor='gray', markeredgewidth=1.5, markeredgecolor='black')

# ゼロライン
ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)

# 軸設定
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('m-coordinate', fontsize=12)
ax.set_title('Annual MCI Coordinates (2005-2024)', fontsize=14, fontweight='bold')
ax.legend(fontsize=11, loc='best')
ax.grid(True, alpha=0.3)

# 日付フォーマット
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.xaxis.set_major_locator(mdates.YearLocator(2))
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.savefig('../docs/annual_mci_plot.png', dpi=150, bbox_inches='tight')
plt.close()

print("Generated: docs/annual_mci_plot.png")
print(f"Data points: {len(df)}")
print(f"Year range: {df['year'].dt.year.min()} to {df['year'].dt.year.max()}")
print(f"m[USD] range: {df['m_USD'].min():.3f} to {df['m_USD'].max():.3f}")
print(f"m[JPY] range: {df['m_JPY'].min():.3f} to {df['m_JPY'].max():.3f}")
print(f"m[TRY] range: {df['m_TRY'].min():.3f} to {df['m_TRY'].max():.3f}")
