#!/usr/bin/env python3
"""
月次PPPを線形補間で算出し、階段状の変化をなだらかにする

従来: 1月にPPPがガツンと変化 → m[TRY]に構造的ジャンプ
改善: 年次PPPの変化を12ヶ月で線形補間 → なだらかな変化
"""

import csv
import math

# 年次PPP確定値・推定値
ANNUAL_PPP = {
    2022: {'PPP_JPY': 92.50, 'PPP_TRY': 4.975},
    2023: {'PPP_JPY': 92.84, 'PPP_TRY': 8.074},
    2024: {'PPP_JPY': 93.20, 'PPP_TRY': 12.55},
    2025: {'PPP_JPY': 93.20, 'PPP_TRY': 16.63},
    2026: {'PPP_JPY': 93.20, 'PPP_TRY': 21.62},  # 推定（30%インフレ想定）
}

def interpolate_ppp(year, month):
    """
    月次PPPを線形補間で算出

    考え方：
    - 1月は当年のPPP
    - 12月は次年のPPPに向けて補間
    - 月ごとに (次年PPP - 当年PPP) / 12 ずつ増加
    """
    if year not in ANNUAL_PPP:
        raise ValueError(f"Year {year} not in ANNUAL_PPP")

    current_ppp = ANNUAL_PPP[year]

    # 次年のPPPがあれば補間、なければ当年の値をそのまま使う
    if year + 1 in ANNUAL_PPP:
        next_ppp = ANNUAL_PPP[year + 1]
    else:
        next_ppp = current_ppp

    # 補間係数（0〜11月 → 0/12〜11/12）
    # 1月(month=1) → factor=0/12, 12月(month=12) → factor=11/12
    factor = (month - 1) / 12

    ppp_jpy = current_ppp['PPP_JPY'] + (next_ppp['PPP_JPY'] - current_ppp['PPP_JPY']) * factor
    ppp_try = current_ppp['PPP_TRY'] + (next_ppp['PPP_TRY'] - current_ppp['PPP_TRY']) * factor

    return ppp_jpy, ppp_try

def calculate_mci(s_usdjpy, s_usdtry, ppp_jpy, ppp_try):
    """為替レートとPPPからMCI座標を計算"""
    d_usdjpy = math.log(s_usdjpy / ppp_jpy)
    d_usdtry = math.log(s_usdtry / ppp_try)

    m_usd = (d_usdjpy + d_usdtry) / 3
    m_jpy = (-2 * d_usdjpy + d_usdtry) / 3
    m_try = (d_usdjpy - 2 * d_usdtry) / 3

    s_tryjpy = s_usdjpy / s_usdtry
    ppp_tryjpy = ppp_jpy / ppp_try
    d_tryjpy = math.log(s_tryjpy / ppp_tryjpy)

    return {
        'd_USDJPY': d_usdjpy,
        'd_USDTRY': d_usdtry,
        'm_USD': m_usd,
        'm_JPY': m_jpy,
        'm_TRY': m_try,
        'S_TRYJPY': s_tryjpy,
        'PPP_TRYJPY': ppp_tryjpy,
        'd_TRYJPY': d_tryjpy,
    }

def main():
    # 月次レートデータ読み込み
    rate_data = []
    with open('monthly_rates_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rate_data.append({
                'date': row['date'],
                'S_USDJPY': float(row['S_USDJPY']),
                'S_USDTRY': float(row['S_USDTRY']),
            })

    print("=" * 80)
    print("月次PPP補間によるMCI再計算")
    print("=" * 80)
    print()

    # 補間PPPで再計算
    results = []

    for entry in rate_data:
        year = int(entry['date'].split('-')[0])
        month = int(entry['date'].split('-')[1])

        # 補間PPPを取得
        ppp_jpy, ppp_try = interpolate_ppp(year, month)

        # MCI計算
        mci = calculate_mci(entry['S_USDJPY'], entry['S_USDTRY'], ppp_jpy, ppp_try)

        result = {
            'date': entry['date'],
            'S_USDJPY': entry['S_USDJPY'],
            'S_USDTRY': entry['S_USDTRY'],
            'PPP_JPY': ppp_jpy,
            'PPP_TRY': ppp_try,
        }
        result.update(mci)
        results.append(result)

    # 月次変動を計算
    for i in range(1, len(results)):
        results[i]['D_mTRY'] = results[i]['m_TRY'] - results[i-1]['m_TRY']
        results[i]['pct_TRYJPY'] = (results[i]['S_TRYJPY'] / results[i-1]['S_TRYJPY'] - 1) * 100

    results[0]['D_mTRY'] = None
    results[0]['pct_TRYJPY'] = None

    # 保存（補間版）
    output_file = 'monthly_mci_interpolated.csv'
    fieldnames = ['date', 'S_USDJPY', 'S_USDTRY', 'S_TRYJPY', 'PPP_JPY', 'PPP_TRY',
                  'd_USDJPY', 'd_USDTRY', 'm_USD', 'm_JPY', 'm_TRY', 'D_mTRY', 'pct_TRYJPY']

    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for r in results:
            # Noneを空文字に変換
            row = {k: ('' if v is None else v) for k, v in r.items()}
            writer.writerow(row)

    print(f"✓ 補間版月次MCIデータを保存: {output_file}")
    print(f"  {len(results)}ヶ月分のデータ")
    print()

    # 比較：従来版 vs 補間版
    print("【比較】PPP切り替え時の変動（従来 vs 補間）")
    print("-" * 80)

    # 従来版の読み込み
    old_data = {}
    with open('monthly_mci_analysis.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            old_data[row['date']] = float(row['m_TRY'])

    # 1月の比較（PPP切り替え月）
    jan_months = [r for r in results if r['date'].endswith('-01')]

    print(f"\n{'月':^10} {'従来m[TRY]':^12} {'補間m[TRY]':^12} {'従来D':^10} {'補間D':^10}")
    print("-" * 60)

    for r in jan_months:
        date = r['date']
        new_m_try = r['m_TRY']
        old_m_try = old_data.get(date, 0)

        # 前月（12月）のデータを取得
        prev_date = f"{int(date.split('-')[0]) - 1}-12"

        # 補間版の前月
        prev_new = [x for x in results if x['date'] == prev_date]
        new_d = r['D_mTRY'] if r['D_mTRY'] else 0

        # 従来版の前月
        prev_old = old_data.get(prev_date, 0)
        old_d = old_m_try - prev_old if prev_date in old_data else 0

        print(f"{date:^10} {old_m_try:>12.6f} {new_m_try:>12.6f} {old_d:>+10.4f} {new_d:>+10.4f}")

    print()
    print("=" * 80)

    # 統計比較
    print("【統計比較】月次変動（PPP切り替え除外）")
    print("-" * 80)

    # 補間版の統計
    new_D = [r['D_mTRY'] for r in results[1:] if r['D_mTRY'] is not None]
    new_mean = sum(new_D) / len(new_D)
    new_variance = sum((x - new_mean)**2 for x in new_D) / len(new_D)
    new_std = math.sqrt(new_variance)

    print(f"\n補間版:")
    print(f"  平均: {new_mean:.6f}")
    print(f"  標準偏差: {new_std:.6f}")
    print(f"  最小値: {min(new_D):.6f}")
    print(f"  最大値: {max(new_D):.6f}")

    print()
    print("=" * 80)

if __name__ == '__main__':
    main()
