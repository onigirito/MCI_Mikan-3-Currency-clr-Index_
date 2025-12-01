#!/usr/bin/env python3
"""
全期間バックテスト実行ツール

2022年1月から2025年10月まで、各月のデータから翌月を予想し、
結果をCSV形式で出力する。

使い方:
  python run_comprehensive_backtest.py
  python run_comprehensive_backtest.py --output results.csv
"""

import argparse
import csv
import math
from typing import Dict, List, Tuple
from datetime import datetime
from dateutil.relativedelta import relativedelta

def load_monthly_data(csv_path: str) -> List[Dict]:
    """月次MCIデータを読み込む"""
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def get_month_data(data: List[Dict], target_month: str) -> Dict:
    """指定月のデータを取得"""
    for row in data:
        if row['date'] == target_month:
            return {
                'date': row['date'],
                'm_USD': float(row['m_USD']),
                'm_JPY': float(row['m_JPY']),
                'm_TRY': float(row['m_TRY']),
                'S_USDJPY': float(row['S_USDJPY']),
                'S_USDTRY': float(row['S_USDTRY']),
                'S_TRYJPY': float(row['S_TRYJPY']),
                'PPP_JPY': float(row['PPP_JPY']),
                'PPP_TRY': float(row['PPP_TRY'])
            }
    return None

def get_next_month(date_str: str) -> str:
    """次月の文字列を取得"""
    dt = datetime.strptime(date_str, '%Y-%m')
    next_dt = dt + relativedelta(months=1)
    return next_dt.strftime('%Y-%m')

def get_prev_month(date_str: str) -> str:
    """前月の文字列を取得"""
    dt = datetime.strptime(date_str, '%Y-%m')
    prev_dt = dt - relativedelta(months=1)
    return prev_dt.strftime('%Y-%m')

def extract_scenario_deltas(data: List[Dict], ref_month: str, next_month: str) -> Dict:
    """
    参照期間（ref_month → next_month）からシナリオ変化量を抽出
    """
    ref_data = get_month_data(data, ref_month)
    next_data = get_month_data(data, next_month)

    if ref_data is None or next_data is None:
        return None

    # 実際の変化量を計算
    dm_usd = next_data['m_USD'] - ref_data['m_USD']
    dm_jpy = next_data['m_JPY'] - ref_data['m_JPY']
    dm_try = next_data['m_TRY'] - ref_data['m_TRY']

    # シナリオ設定（参照変化量を基に3パターン作成）
    scenarios = {
        'A（慣性維持）': {
            'dm_usd': dm_usd,
            'dm_jpy': dm_jpy,
            'dm_try': dm_try
        },
        'B（やや円高）': {
            'dm_usd': dm_usd * 1.5,
            'dm_jpy': -dm_jpy * 0.5,
            'dm_try': dm_try * 0.8
        },
        'C（やや円安）': {
            'dm_usd': dm_usd * 0.7,
            'dm_jpy': dm_jpy * 0.5,
            'dm_try': dm_try
        }
    }

    return scenarios

def apply_scenario_to_base(base_data: Dict, scenario_deltas: Dict) -> Dict:
    """基準月のデータにシナリオ変化量を適用"""
    scenarios = {}
    for name, deltas in scenario_deltas.items():
        m_usd = base_data['m_USD'] + deltas['dm_usd']
        m_jpy = base_data['m_JPY'] + deltas['dm_jpy']
        m_try = base_data['m_TRY'] + deltas['dm_try']

        # ゼロサム制約を強制
        sum_check = m_usd + m_jpy + m_try
        if abs(sum_check) > 1e-6:
            m_try = -(m_usd + m_jpy)

        scenarios[name] = {
            'm_usd': m_usd,
            'm_jpy': m_jpy,
            'm_try': m_try
        }

    return scenarios

def calculate_prices(scenarios: Dict, ppp_jpy: float, ppp_try: float) -> Dict:
    """各シナリオから3通貨ペアの価格を計算"""
    prices = {
        'USD/JPY': [],
        'USD/TRY': [],
        'TRY/JPY': []
    }

    for name, vals in scenarios.items():
        # USD/JPY
        s_usdjpy = ppp_jpy * math.exp(vals['m_usd'] - vals['m_jpy'])
        prices['USD/JPY'].append(s_usdjpy)

        # USD/TRY
        s_usdtry = ppp_try * math.exp(vals['m_usd'] - vals['m_try'])
        prices['USD/TRY'].append(s_usdtry)

        # TRY/JPY
        s_tryjpy = (ppp_jpy / ppp_try) * math.exp(vals['m_try'] - vals['m_jpy'])
        prices['TRY/JPY'].append(s_tryjpy)

    return prices

def calculate_ranges(prices: Dict) -> Dict:
    """中心シナリオとリスクレンジを計算"""
    ranges = {}

    for pair, price_list in prices.items():
        center_min = min(price_list)
        center_max = max(price_list)
        center_mid = (center_min + center_max) / 2

        # リスクレンジ（±0.05の統計的変動）
        risk_factor = math.exp(0.05) - 1
        risk_lower = center_mid * (1 - risk_factor)
        risk_upper = center_mid * (1 + risk_factor)

        ranges[pair] = {
            'center_min': center_min,
            'center_max': center_max,
            'center_mid': center_mid,
            'risk_lower': risk_lower,
            'risk_upper': risk_upper
        }

    return ranges

def run_backtest_for_month(data: List[Dict], base_month: str) -> Dict:
    """
    指定月のバックテストを実行

    Args:
        data: 月次データ
        base_month: 基準月

    Returns:
        バックテスト結果（None if failed）
    """
    # 前月を参照シナリオとして使用
    ref_month = get_prev_month(base_month)
    target_month = get_next_month(base_month)

    # データ取得
    ref_data = get_month_data(data, ref_month)
    base_data = get_month_data(data, base_month)
    target_data = get_month_data(data, target_month)

    # いずれかのデータが欠けていればスキップ
    if ref_data is None or base_data is None or target_data is None:
        return None

    # シナリオ変化量を抽出
    scenario_deltas = extract_scenario_deltas(data, ref_month, base_month)
    if scenario_deltas is None:
        return None

    # シナリオを適用
    scenarios = apply_scenario_to_base(base_data, scenario_deltas)

    # 価格計算
    prices = calculate_prices(scenarios, target_data['PPP_JPY'], target_data['PPP_TRY'])

    # レンジ計算
    ranges = calculate_ranges(prices)

    # 結果を構築
    result = {
        'base_month': base_month,
        'target_month': target_month,
        'ref_month': ref_month,
    }

    # 各通貨ペアの結果を追加
    pairs_config = {
        'USDJPY': {'key': 'USD/JPY', 'actual_key': 'S_USDJPY'},
        'USDTRY': {'key': 'USD/TRY', 'actual_key': 'S_USDTRY'},
        'TRYJPY': {'key': 'TRY/JPY', 'actual_key': 'S_TRYJPY'}
    }

    for pair_name, config in pairs_config.items():
        r = ranges[config['key']]
        actual_val = target_data[config['actual_key']]
        error_pct = ((r['center_mid'] - actual_val) / actual_val) * 100

        result[f'{pair_name}_pred_center_min'] = r['center_min']
        result[f'{pair_name}_pred_center_max'] = r['center_max']
        result[f'{pair_name}_pred_center_mid'] = r['center_mid']
        result[f'{pair_name}_pred_risk_lower'] = r['risk_lower']
        result[f'{pair_name}_pred_risk_upper'] = r['risk_upper']
        result[f'{pair_name}_actual'] = actual_val
        result[f'{pair_name}_error_pct'] = error_pct

    return result

def main():
    parser = argparse.ArgumentParser(
        description='全期間バックテスト実行',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--csv-path',
                        default='../dataset/monthly_mci_interpolated_ppp_2022_2025.csv',
                        help='月次MCIデータのCSVパス')
    parser.add_argument('--output',
                        default='backtest_results_2022_2025.csv',
                        help='出力CSVファイル名')

    args = parser.parse_args()

    # データ読み込み
    print(f"Loading data from {args.csv_path}...")
    data = load_monthly_data(args.csv_path)

    # 全月のリストを取得（dateカラムから）
    all_months = [row['date'] for row in data]

    # 2022-01から2025-10まで（2025-11を予想対象とする）
    # 最初の月（2022-01）は参照データがないのでスキップ
    base_months = all_months[1:-1]  # 2番目から最後の1つ前まで

    print(f"Running backtest for {len(base_months)} months...")
    print(f"Range: {base_months[0]} to {base_months[-1]}")
    print()

    results = []
    for base_month in base_months:
        result = run_backtest_for_month(data, base_month)
        if result is not None:
            results.append(result)
            print(f"OK {base_month} -> {result['target_month']}")
        else:
            print(f"SKIP {base_month} (data missing)")

    # CSV出力
    if results:
        fieldnames = [
            'base_month', 'target_month', 'ref_month',
            'USDJPY_pred_center_min', 'USDJPY_pred_center_max', 'USDJPY_pred_center_mid',
            'USDJPY_pred_risk_lower', 'USDJPY_pred_risk_upper',
            'USDJPY_actual', 'USDJPY_error_pct',
            'USDTRY_pred_center_min', 'USDTRY_pred_center_max', 'USDTRY_pred_center_mid',
            'USDTRY_pred_risk_lower', 'USDTRY_pred_risk_upper',
            'USDTRY_actual', 'USDTRY_error_pct',
            'TRYJPY_pred_center_min', 'TRYJPY_pred_center_max', 'TRYJPY_pred_center_mid',
            'TRYJPY_pred_risk_lower', 'TRYJPY_pred_risk_upper',
            'TRYJPY_actual', 'TRYJPY_error_pct'
        ]

        with open(args.output, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print()
        print(f"Results saved to {args.output}")
        print(f"Total: {len(results)} months")

        # 統計サマリーを表示
        print()
        print("=== Error Statistics ===")
        for pair in ['USDJPY', 'USDTRY', 'TRYJPY']:
            errors = [r[f'{pair}_error_pct'] for r in results]
            avg_error = sum(errors) / len(errors)
            abs_errors = [abs(e) for e in errors]
            avg_abs_error = sum(abs_errors) / len(abs_errors)
            max_error = max(abs_errors)

            print(f"{pair}: avg={avg_error:+.2f}%, abs_avg={avg_abs_error:.2f}%, max={max_error:.2f}%")
    else:
        print("No results generated.")

if __name__ == '__main__':
    main()
