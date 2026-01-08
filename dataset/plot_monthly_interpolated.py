#!/usr/bin/env python3
"""
月次MCI グラフ生成（PPP線形補間版）

monthly_mci_complete_2022_2025.csv（2022年m座標修正済み）を使用
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# フォント設定
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# データ読み込み
df = pd.read_csv('monthly_mci_complete_2022_2025.csv')
df['date'] = pd.to_datetime(df['date'])

# プロット
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(df['date'], df['m_USD'], 'o-', label='m[USD]', linewidth=2, markersize=4, color='#1f77b4')
ax.plot(df['date'], df['m_JPY'], 's-', label='m[JPY]', linewidth=2, markersize=4, color='#ff7f0e')
ax.plot(df['date'], df['m_TRY'], '^-', label='m[TRY]', linewidth=2, markersize=4, color='#2ca02c')

# ゼロライン
ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)

# 軸設定
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('m-coordinate', fontsize=12)
ax.set_title('Monthly MCI Coordinates (PPP Interpolated)', fontsize=14, fontweight='bold')
ax.legend(fontsize=11, loc='best')
ax.grid(True, alpha=0.3)

# 日付フォーマット
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.xticks(rotation=45, ha='right')

# Y軸範囲調整
ax.set_ylim(-1.1, 0.7)

plt.tight_layout()
plt.savefig('../docs/monthly_mci_interpolated_ppp.png', dpi=150, bbox_inches='tight')
plt.close()

print("Generated: docs/monthly_mci_interpolated_ppp.png")
print(f"Data points: {len(df)}")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"m[USD] range: {df['m_USD'].min():.3f} to {df['m_USD'].max():.3f}")
print(f"m[JPY] range: {df['m_JPY'].min():.3f} to {df['m_JPY'].max():.3f}")
print(f"m[TRY] range: {df['m_TRY'].min():.3f} to {df['m_TRY'].max():.3f}")
