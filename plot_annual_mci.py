#!/usr/bin/env python3
"""年次MCI座標（m_USD, m_JPY, m_TRY）のグラフを作成"""

import csv
import matplotlib.pyplot as plt
import matplotlib

# 日本語フォント設定
matplotlib.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']

# データ読み込み
years = []
m_usd = []
m_jpy = []
m_try = []

with open('dataset/mikan_3currency_clr_index_ppp_data.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        years.append(int(row['year']))
        m_usd.append(float(row['m_USD']))
        m_jpy.append(float(row['m_JPY']))
        m_try.append(float(row['m_TRY']))

# グラフ作成
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(years, m_usd, 'b-o', label='m[USD]', linewidth=2, markersize=6)
ax.plot(years, m_jpy, 'r-s', label='m[JPY]', linewidth=2, markersize=6)
ax.plot(years, m_try, 'g-^', label='m[TRY]', linewidth=2, markersize=6)

# ゼロライン
ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.7)

# 軸設定
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('m[i] (MCI Coordinate)', fontsize=12)
ax.set_title('Mikan 3-Currency CLR Index: Annual MCI Coordinates (2005-2024)', fontsize=14)
ax.legend(loc='best', fontsize=11)
ax.grid(True, alpha=0.3)
ax.set_xlim(2004, 2025)

# 注釈
ax.annotate('Overvalued (+)', xy=(2024.5, 0.3), fontsize=9, color='gray')
ax.annotate('Undervalued (-)', xy=(2024.5, -0.3), fontsize=9, color='gray')

plt.tight_layout()
plt.savefig('annual_mci_plot.png', dpi=150, bbox_inches='tight')
print('Saved: annual_mci_plot.png')
plt.show()
