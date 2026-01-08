#!/usr/bin/env python3
"""
月次MCIグラフ生成スクリプト（CHAPTER8用）

月次データ（2022年m座標修正後）から2つのグラフを生成：
1. monthly_mci_interpolated_ppp.png - PPP線形補間版
2. monthly_mci_annual_ppp.png - 年次PPP固定版（比較用）
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# 日本語フォント設定（必要に応じて変更）
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def plot_monthly_mci_interpolated():
    """PPP線形補間版の月次MCIグラフ（モノクロ版）"""

    # データ読み込み
    df = pd.read_csv('monthly_mci_complete_2022_2025.csv')
    df['date'] = pd.to_datetime(df['date'])

    # プロット
    fig, ax = plt.subplots(figsize=(12, 6))

    # モノクロで判読可能なスタイル
    ax.plot(df['date'], df['m_USD'], 'o', label='m[USD]', linewidth=2, markersize=5,
            color='black', linestyle='-', markerfacecolor='white', markeredgewidth=1.5, markeredgecolor='black')
    ax.plot(df['date'], df['m_JPY'], 's', label='m[JPY]', linewidth=2, markersize=5,
            color='black', linestyle='--', markerfacecolor='black', markeredgewidth=1.5)
    ax.plot(df['date'], df['m_TRY'], '^', label='m[TRY]', linewidth=2, markersize=5,
            color='black', linestyle=':', markerfacecolor='gray', markeredgewidth=1.5, markeredgecolor='black')

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

    plt.tight_layout()
    plt.savefig('../docs/monthly_mci_interpolated_ppp.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("Generated: docs/monthly_mci_interpolated_ppp.png")

def plot_monthly_mci_annual_ppp():
    """年次PPP固定版の月次MCIグラフ（比較用・モノクロ版）"""

    # データ読み込み
    df = pd.read_csv('monthly_mci_fixed_ppp_2022_2025.csv')
    df['date'] = pd.to_datetime(df['date'])

    # プロット
    fig, ax = plt.subplots(figsize=(12, 6))

    # モノクロで判読可能なスタイル
    ax.plot(df['date'], df['m_USD'], 'o', label='m[USD]', linewidth=2, markersize=5,
            color='black', linestyle='-', markerfacecolor='white', markeredgewidth=1.5, markeredgecolor='black')
    ax.plot(df['date'], df['m_JPY'], 's', label='m[JPY]', linewidth=2, markersize=5,
            color='black', linestyle='--', markerfacecolor='black', markeredgewidth=1.5)
    ax.plot(df['date'], df['m_TRY'], '^', label='m[TRY]', linewidth=2, markersize=5,
            color='black', linestyle=':', markerfacecolor='gray', markeredgewidth=1.5, markeredgecolor='black')

    # ゼロライン
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)

    # 年境界（PPP更新タイミング）を示す縦線（モノクロ版）
    year_boundaries = ['2023-01-01', '2024-01-01', '2025-01-01']
    for boundary in year_boundaries:
        ax.axvline(x=pd.to_datetime(boundary), color='gray', linestyle='-.',
                   linewidth=1.5, alpha=0.6, label='Year boundary' if boundary == year_boundaries[0] else '')

    # 軸設定
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('m-coordinate', fontsize=12)
    ax.set_title('Monthly MCI Coordinates (Annual PPP Fixed)', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11, loc='best')
    ax.grid(True, alpha=0.3)

    # 日付フォーマット
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig('../docs/monthly_mci_annual_ppp.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("Generated: docs/monthly_mci_annual_ppp.png")

if __name__ == '__main__':
    print("="*60)
    print("月次MCIグラフ生成（CHAPTER8用）")
    print("="*60)

    print("\n[1] PPP線形補間版を生成中...")
    plot_monthly_mci_interpolated()

    print("\n[2] 年次PPP固定版を生成中...")
    plot_monthly_mci_annual_ppp()

    print("\n" + "="*60)
    print("All graphs generated successfully")
    print("  - docs/monthly_mci_interpolated_ppp.png")
    print("  - docs/monthly_mci_annual_ppp.png")
    print("="*60)
