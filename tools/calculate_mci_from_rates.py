#!/usr/bin/env python3
"""
為替レートからMCI座標を計算するツール

使い方:
  python3 calculate_mci_from_rates.py --usdjpy 157 --usdtry 42.3 --ppp-year 2024

PPPは固定（直近の確定値）を使い、為替レートのみを更新することで
月次・週次・日次のMCI座標を算出できる。
"""

import argparse
import csv
import math

def load_ppp_data(year):
    """指定年のPPPデータを読み込む"""
    with open('dataset/mikan_3currency_clr_index_ppp_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row['year']) == year:
                return {
                    'PPP_JPY': float(row['PPP_JPY']),
                    'PPP_TRY': float(row['PPP_TRY']),
                }
    raise ValueError(f"Year {year} not found in dataset")

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
        'd_usdjpy': d_usdjpy,
        'd_usdtry': d_usdtry,
        'm_usd': m_usd,
        'm_jpy': m_jpy,
        'm_try': m_try,
        's_tryjpy': s_tryjpy,
        'ppp_tryjpy': ppp_tryjpy,
        'd_tryjpy': d_tryjpy,
    }

def main():
    parser = argparse.ArgumentParser(description='Calculate MCI coordinates from exchange rates')
    parser.add_argument('--usdjpy', type=float, required=True, help='USD/JPY exchange rate')
    parser.add_argument('--usdtry', type=float, required=True, help='USD/TRY exchange rate')
    parser.add_argument('--ppp-year', type=int, default=2024, help='PPP reference year (default: 2024)')
    parser.add_argument('--compare', type=int, help='Compare with this year from dataset')

    args = parser.parse_args()

    # PPPデータ読み込み
    ppp_data = load_ppp_data(args.ppp_year)

    # MCI計算
    result = calculate_mci(args.usdjpy, args.usdtry, ppp_data['PPP_JPY'], ppp_data['PPP_TRY'])

    print("=" * 80)
    print(f"MCI座標計算（PPP基準年: {args.ppp_year}）")
    print("=" * 80)
    print()
    print("入力:")
    print(f"  USD/JPY = {args.usdjpy:.2f}")
    print(f"  USD/TRY = {args.usdtry:.2f}")
    print(f"  TRY/JPY = {result['s_tryjpy']:.4f}")
    print()
    print("PPP基準値:")
    print(f"  PPP_JPY = {ppp_data['PPP_JPY']:.2f}")
    print(f"  PPP_TRY = {ppp_data['PPP_TRY']:.2f}")
    print()
    print("PPP乖離率:")
    print(f"  d_USDJPY = {result['d_usdjpy']:+.6f}")
    print(f"  d_USDTRY = {result['d_usdtry']:+.6f}")
    print(f"  d_TRYJPY = {result['d_tryjpy']:+.6f}")
    print()
    print("MCI座標:")
    print(f"  m[USD] = {result['m_usd']:+.6f}")
    print(f"  m[JPY] = {result['m_jpy']:+.6f}")
    print(f"  m[TRY] = {result['m_try']:+.6f}")
    print(f"  合計   = {result['m_usd'] + result['m_jpy'] + result['m_try']:+.10f} (ゼロサム確認)")
    print()

    # 比較年が指定されている場合
    if args.compare:
        with open('dataset/mikan_3currency_clr_index_ppp_data.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row['year']) == args.compare:
                    m_try_ref = float(row['m_TRY'])
                    m_usd_ref = float(row['m_USD'])
                    m_jpy_ref = float(row['m_JPY'])

                    print(f"{args.compare}年との比較:")
                    print(f"  Δm[USD] = {result['m_usd'] - m_usd_ref:+.6f}")
                    print(f"  Δm[JPY] = {result['m_jpy'] - m_jpy_ref:+.6f}")
                    print(f"  Δm[TRY] = {result['m_try'] - m_try_ref:+.6f}")

                    # 深度判定
                    D_m_try = result['m_try'] - m_try_ref
                    if D_m_try >= -0.05:
                        depth = "正常域"
                    elif D_m_try >= -0.06:
                        depth = "深度1（通常変動）"
                    elif D_m_try >= -0.08:
                        depth = "深度2"
                    else:
                        depth = "深度3（危機レベル）"

                    print(f"  深度判定: {depth}")
                    print()

    print("=" * 80)

if __name__ == '__main__':
    main()
