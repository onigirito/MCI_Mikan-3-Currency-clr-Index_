#!/usr/bin/env python3
"""
直近3年の月次MCIデータ作成ツール

年次PPPを使って、月次の為替レートからMCI座標を計算する。
2022-2024は確定PPP、2025は推定PPPを使用。
"""

import csv
import math
from datetime import datetime

# 各年のPPP設定
PPP_CONFIG = {
    2022: {'PPP_JPY': 92.50, 'PPP_TRY': 4.975},    # 確定値（World Bank WDI）
    2023: {'PPP_JPY': 92.84, 'PPP_TRY': 8.074},    # 確定値（World Bank WDI）
    2024: {'PPP_JPY': 93.20, 'PPP_TRY': 12.55},    # 確定値（World Bank WDI）
    2025: {'PPP_JPY': 93.20, 'PPP_TRY': 16.63},    # 推定値（32.5%インフレ想定、OECD/IMF予測ベース）
}

def calculate_mci(s_usdjpy, s_usdtry, ppp_jpy, ppp_try):
    """為替レートとPPPからMCI座標を計算"""

    # PPP乖離率
    d_usdjpy = math.log(s_usdjpy / ppp_jpy)
    d_usdtry = math.log(s_usdtry / ppp_try)

    # MCI座標
    m_usd = (d_usdjpy + d_usdtry) / 3
    m_jpy = (-2 * d_usdjpy + d_usdtry) / 3
    m_try = (d_usdjpy - 2 * d_usdtry) / 3

    # クロスレート
    s_tryjpy = s_usdjpy / s_usdtry
    ppp_tryjpy = ppp_jpy / ppp_try
    d_tryjpy = math.log(s_tryjpy / ppp_tryjpy)

    return {
        'S_USDJPY': s_usdjpy,
        'S_USDTRY': s_usdtry,
        'PPP_JPY': ppp_jpy,
        'PPP_TRY': ppp_try,
        'd_USDJPY': d_usdjpy,
        'd_USDTRY': d_usdtry,
        'm_USD': m_usd,
        'm_JPY': m_jpy,
        'm_TRY': m_try,
        'S_TRYJPY': s_tryjpy,
        'PPP_TRYJPY': ppp_tryjpy,
        'd_TRYJPY': d_tryjpy,
    }

def read_monthly_rates(filename):
    """
    月次為替レートを読み込む

    CSVフォーマット:
    date,S_USDJPY,S_USDTRY
    2022-01,115.10,13.42
    2022-02,115.54,14.01
    ...
    """
    data = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'date': row['date'],
                'S_USDJPY': float(row['S_USDJPY']),
                'S_USDTRY': float(row['S_USDTRY']),
            })
    return data

def process_monthly_data(rate_data):
    """月次レートデータを処理してMCI座標を計算"""
    results = []

    for entry in rate_data:
        # 日付から年を抽出
        year = int(entry['date'].split('-')[0])

        if year not in PPP_CONFIG:
            print(f"Warning: No PPP config for year {year}, skipping")
            continue

        ppp = PPP_CONFIG[year]

        # MCI計算
        mci = calculate_mci(
            entry['S_USDJPY'],
            entry['S_USDTRY'],
            ppp['PPP_JPY'],
            ppp['PPP_TRY']
        )

        # 結果をマージ
        result = {'date': entry['date']}
        result.update(mci)
        results.append(result)

    return results

def create_sample_template(output_file='monthly_rates_template.csv'):
    """
    月次レート入力用のテンプレートCSVを作成
    """
    # 2022-01から2025-12までの月リストを生成
    months = []
    for year in range(2022, 2026):
        for month in range(1, 13):
            # 2025年は現在月まで
            if year == 2025 and month > datetime.now().month:
                break
            months.append(f"{year}-{month:02d}")

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'S_USDJPY', 'S_USDTRY'])
        for month in months:
            # サンプル値（要入力）
            writer.writerow([month, '', ''])

    print(f"✓ テンプレートを作成しました: {output_file}")
    print(f"  {len(months)}ヶ月分のデータ入力欄があります")
    print()
    print("次のステップ:")
    print("  1. このCSVファイルに実際の月次平均レートを入力")
    print("  2. python3 tools/create_monthly_mci.py monthly_rates_template.csv を実行")

def save_monthly_mci(data, output_file='dataset/mci_monthly_recent.csv'):
    """月次MCIデータを保存"""
    if not data:
        print("Error: No data to save")
        return

    fieldnames = ['date', 'S_USDJPY', 'S_USDTRY', 'PPP_JPY', 'PPP_TRY',
                  'd_USDJPY', 'd_USDTRY', 'm_USD', 'm_JPY', 'm_TRY',
                  'S_TRYJPY', 'PPP_TRYJPY', 'd_TRYJPY']

    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"✓ 月次MCIデータを保存しました: {output_file}")
    print(f"  {len(data)}ヶ月分のデータ")

def calculate_monthly_variations(data):
    """月次変動を計算して統計を表示"""
    print()
    print("=" * 80)
    print("月次変動統計")
    print("=" * 80)

    variations = []
    for i in range(1, len(data)):
        d_m_try = data[i]['m_TRY'] - data[i-1]['m_TRY']
        variations.append({
            'date': data[i]['date'],
            'D_mTRY': d_m_try,
            'm_TRY': data[i]['m_TRY'],
        })

    if variations:
        D_values = [v['D_mTRY'] for v in variations]
        mean = sum(D_values) / len(D_values)
        variance = sum((x - mean)**2 for x in D_values) / len(D_values)
        std = math.sqrt(variance)

        print(f"m[TRY]月次変動:")
        print(f"  平均: {mean:.6f}")
        print(f"  標準偏差: {std:.6f}")
        print(f"  最小値: {min(D_values):.6f}")
        print(f"  最大値: {max(D_values):.6f}")
        print()

        # 大きな変動を抽出
        threshold = std * 2
        large_moves = [v for v in variations if abs(v['D_mTRY']) > threshold]
        if large_moves:
            print(f"大きな変動（±2σ超過）:")
            for v in large_moves:
                print(f"  {v['date']}: {v['D_mTRY']:+.6f}")
        print()

def main():
    import sys

    if len(sys.argv) < 2:
        print("使い方:")
        print("  1. テンプレート作成: python3 tools/create_monthly_mci.py --template")
        print("  2. データ処理: python3 tools/create_monthly_mci.py <monthly_rates.csv>")
        print()
        print("テンプレートを作成しますか？ (y/n)")
        response = input().strip().lower()
        if response == 'y':
            create_sample_template()
        return

    if sys.argv[1] == '--template':
        create_sample_template()
        return

    # 月次レートデータを読み込んで処理
    input_file = sys.argv[1]

    print(f"月次レートデータを読み込んでいます: {input_file}")
    rate_data = read_monthly_rates(input_file)

    print(f"✓ {len(rate_data)}ヶ月分のデータを読み込みました")
    print()

    # MCI計算
    print("MCI座標を計算中...")
    mci_data = process_monthly_data(rate_data)

    # 保存
    save_monthly_mci(mci_data)

    # 統計表示
    calculate_monthly_variations(mci_data)

    print("=" * 80)
    print("完了")
    print("=" * 80)

if __name__ == '__main__':
    main()
