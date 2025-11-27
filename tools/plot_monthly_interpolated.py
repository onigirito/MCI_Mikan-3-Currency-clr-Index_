#!/usr/bin/env python3
"""
Generate monthly MCI plot with interpolated PPP
"""
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Read data
dates = []
m_USD = []
m_JPY = []
m_TRY = []

with open('dataset/monthly_mci_interpolated_ppp_2022_2025.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        dates.append(datetime.strptime(row['date'], '%Y-%m'))
        m_USD.append(float(row['m_USD']))
        m_JPY.append(float(row['m_JPY']))
        m_TRY.append(float(row['m_TRY']))

# Create figure
fig, ax = plt.subplots(figsize=(12, 6))

# Plot lines
ax.plot(dates, m_USD, 'o-', color='#1f77b4', linewidth=2, markersize=3, label='m[USD]')
ax.plot(dates, m_JPY, 's-', color='#d62728', linewidth=2, markersize=3, label='m[JPY]')
ax.plot(dates, m_TRY, '^-', color='#2ca02c', linewidth=2, markersize=3, label='m[TRY]')

# Zero line
ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)

# Formatting
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('m[i] (MCI Coordinate)', fontsize=12)
ax.set_title('Monthly MCI with Interpolated PPP (2022-2025)\nSmooth transition using monthly PPP estimates',
             fontsize=14, pad=20)

# Grid
ax.grid(True, alpha=0.3)

# Legend
ax.legend(fontsize=11, loc='right')

# X-axis formatting
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.xticks(rotation=45, ha='right')

# Tight layout
plt.tight_layout()

# Save
output_file = 'docs/monthly_mci_interpolated_ppp.png'
plt.savefig(output_file, dpi=150, bbox_inches='tight')
print(f"✓ Graph saved: {output_file}")
print(f"  Data points: {len(dates)}")
print(f"  Date range: {dates[0].strftime('%Y-%m')} to {dates[-1].strftime('%Y-%m')}")
print(f"\nLatest values ({dates[-1].strftime('%Y-%m')}):")
print(f"  m[USD] = {m_USD[-1]:+.3f}")
print(f"  m[JPY] = {m_JPY[-1]:+.3f}")
print(f"  m[TRY] = {m_TRY[-1]:+.3f}")
