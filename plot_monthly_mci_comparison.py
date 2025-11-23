#!/usr/bin/env python3
"""月次MCI座標のグラフ比較: 年単位PPP vs 補間PPP"""

import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# データ読み込み関数
def load_monthly_data(filename):
    dates = []
    m_usd = []
    m_jpy = []
    m_try = []

    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dates.append(datetime.strptime(row['date'], '%Y-%m'))
            m_usd.append(float(row['m_USD']))
            m_jpy.append(float(row['m_JPY']))
            m_try.append(float(row['m_TRY']))

    return dates, m_usd, m_jpy, m_try

# グラフ1: 年単位PPPでの月次MCI
def plot_annual_ppp():
    dates, m_usd, m_jpy, m_try = load_monthly_data('dataset/mci_monthly_recent.csv')

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(dates, m_usd, 'b-', label='m[USD]', linewidth=1.5)
    ax.plot(dates, m_jpy, 'r-', label='m[JPY]', linewidth=1.5)
    ax.plot(dates, m_try, 'g-', label='m[TRY]', linewidth=1.5)

    ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.7)

    # 年境界に縦線を追加
    for year in [2023, 2024, 2025]:
        ax.axvline(x=datetime(year, 1, 1), color='orange', linestyle=':', alpha=0.7, linewidth=1.5)

    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('m[i] (MCI Coordinate)', fontsize=12)
    ax.set_title('Monthly MCI with Annual PPP (2022-2025)\nPPP updates cause discontinuities at year boundaries', fontsize=13)
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)

    ax.annotate('PPP update', xy=(datetime(2023, 1, 1), 0.1), fontsize=9, color='orange')
    ax.annotate('PPP update', xy=(datetime(2024, 1, 1), 0.1), fontsize=9, color='orange')

    plt.tight_layout()
    plt.savefig('monthly_mci_annual_ppp.png', dpi=150, bbox_inches='tight')
    print('Saved: monthly_mci_annual_ppp.png')

# グラフ2: 補間PPPでの月次MCI
def plot_interpolated_ppp():
    dates, m_usd, m_jpy, m_try = load_monthly_data('monthly_mci_interpolated.csv')

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(dates, m_usd, 'b-', label='m[USD]', linewidth=1.5)
    ax.plot(dates, m_jpy, 'r-', label='m[JPY]', linewidth=1.5)
    ax.plot(dates, m_try, 'g-', label='m[TRY]', linewidth=1.5)

    ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.7)

    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('m[i] (MCI Coordinate)', fontsize=12)
    ax.set_title('Monthly MCI with Interpolated PPP (2022-2025)\nSmooth transition using monthly PPP estimates', fontsize=13)
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig('monthly_mci_interpolated_ppp.png', dpi=150, bbox_inches='tight')
    print('Saved: monthly_mci_interpolated_ppp.png')

if __name__ == '__main__':
    plot_annual_ppp()
    plot_interpolated_ppp()
    print('Done!')
