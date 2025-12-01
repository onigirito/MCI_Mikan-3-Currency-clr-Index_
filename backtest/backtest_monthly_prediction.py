#!/usr/bin/env python3
"""
月次MCI価格予想のバックテストツール

第8章の価格予想原理に基づき、任意の基準月から翌月の価格レンジを予想し、
実績と比較するバックテスト機能を提供する。

使い方:
  python backtest_monthly_prediction.py --base-month 2025-02
  python backtest_monthly_prediction.py --base-month 2024-08 --reference-month 2025-11
"""

import argparse
import csv
import math
from typing import Dict, List, Tuple

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
    raise ValueError(f"Month {target_month} not found in data")

def extract_scenario_deltas(data: List[Dict], ref_month: str, next_month: str) -> Dict:
    """
    参照期間（ref_month → next_month）からシナリオ変化量を抽出

    Args:
        data: 月次データ
        ref_month: 参照基準月（例: '2025-11'）
        next_month: 参照次月（例: '2025-12'）

    Returns:
        各シナリオの変化量
    """
    ref_data = get_month_data(data, ref_month)
    next_data = get_month_data(data, next_month)

    # 実際の変化量を計算
    dm_usd = next_data['m_USD'] - ref_data['m_USD']
    dm_jpy = next_data['m_JPY'] - ref_data['m_JPY']
    dm_try = next_data['m_TRY'] - ref_data['m_TRY']

    # シナリオ設定（参照変化量を基に3パターン作成）
    # A: 実際の変化量（慣性維持）
    # B: JPYが0方向に動くパターン（やや円高/円安）
    # C: 中間パターン

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
    """
    基準月のデータにシナリオ変化量を適用して予想月のシナリオを生成

    Args:
        base_data: 基準月のMCI座標
        scenario_deltas: シナリオ変化量

    Returns:
        各シナリオの予想MCI座標
    """
    scenarios = {}
    for name, deltas in scenario_deltas.items():
        m_usd = base_data['m_USD'] + deltas['dm_usd']
        m_jpy = base_data['m_JPY'] + deltas['dm_jpy']
        m_try = base_data['m_TRY'] + deltas['dm_try']

        # ゼロサム制約の確認
        sum_check = m_usd + m_jpy + m_try
        if abs(sum_check) > 1e-6:
            # ゼロサム制約を強制（TRYを調整）
            m_try = -(m_usd + m_jpy)

        scenarios[name] = {
            'm_usd': m_usd,
            'm_jpy': m_jpy,
            'm_try': m_try
        }

    return scenarios

def calculate_prices(scenarios: Dict, ppp_jpy: float, ppp_try: float) -> Dict:
    """
    各シナリオから3通貨ペアの価格を計算

    Args:
        scenarios: 各シナリオのMCI座標
        ppp_jpy: 予想月のPPP_JPY
        ppp_try: 予想月のPPP_TRY

    Returns:
        各通貨ペアの価格リスト
    """
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

def calculate_ranges(prices: Dict, center_m_diff: Dict) -> Dict:
    """
    中心シナリオとリスクレンジを計算

    Args:
        prices: 各通貨ペアの価格リスト
        center_m_diff: 中心シナリオのm差分（リスクレンジ計算用）

    Returns:
        各通貨ペアのレンジ
    """
    ranges = {}

    for pair, price_list in prices.items():
        center_min = min(price_list)
        center_max = max(price_list)
        center_mid = (center_min + center_max) / 2

        # リスクレンジ（±0.05の統計的変動）
        # 簡易的にcenter_midから±5%として計算
        risk_factor = math.exp(0.05) - 1  # 約5.13%
        risk_lower = center_mid * (1 - risk_factor)
        risk_upper = center_mid * (1 + risk_factor)

        ranges[pair] = {
            'center_min': center_min,
            'center_max': center_max,
            'risk_lower': risk_lower,
            'risk_upper': risk_upper
        }

    return ranges

def format_output(ranges: Dict, actual: Dict) -> str:
    """
    結果を8章形式の表で出力

    Args:
        ranges: 各通貨ペアのレンジ
        actual: 実績値

    Returns:
        フォーマットされた表
    """
    output = []
    output.append("| 通貨ペア | 中心シナリオ | リスクレンジ | 実績値 | 誤差率 |")
    output.append("|---------|-------------|-------------|--------|--------|")

    pairs_config = {
        'USD/JPY': {'unit': '円', 'decimals': 0, 'actual_key': 'S_USDJPY'},
        'USD/TRY': {'unit': 'リラ', 'decimals': 1, 'actual_key': 'S_USDTRY'},
        'TRY/JPY': {'unit': '円', 'decimals': 2, 'actual_key': 'S_TRYJPY'}
    }

    for pair, config in pairs_config.items():
        r = ranges[pair]
        actual_val = actual[config['actual_key']]
        center_mid = (r['center_min'] + r['center_max']) / 2
        error_pct = ((center_mid - actual_val) / actual_val) * 100

        if config['decimals'] == 0:
            center_str = f"{r['center_min']:.0f}〜{r['center_max']:.0f}{config['unit']}"
            risk_str = f"{r['risk_lower']:.0f}〜{r['risk_upper']:.0f}{config['unit']}"
            actual_str = f"{actual_val:.0f}{config['unit']}"
        elif config['decimals'] == 1:
            center_str = f"{r['center_min']:.1f}〜{r['center_max']:.1f}{config['unit']}"
            risk_str = f"{r['risk_lower']:.1f}〜{r['risk_upper']:.1f}{config['unit']}"
            actual_str = f"{actual_val:.2f}{config['unit']}"
        else:
            center_str = f"{r['center_min']:.2f}〜{r['center_max']:.2f}{config['unit']}"
            risk_str = f"{r['risk_lower']:.2f}〜{r['risk_upper']:.2f}{config['unit']}"
            actual_str = f"{actual_val:.2f}{config['unit']}"

        error_str = f"{error_pct:+.2f}%"

        output.append(f"| {pair} | {center_str} | {risk_str} | {actual_str} | {error_str} |")

    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(
        description='月次MCI価格予想のバックテスト',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  # 2025年2月→3月の予想をテスト（2025年11月→12月のシナリオを参照）
  python backtest_monthly_prediction.py --base-month 2025-02

  # 2024年8月→9月の予想をテスト（2025年11月→12月のシナリオを参照）
  python backtest_monthly_prediction.py --base-month 2024-08
        """
    )

    parser.add_argument('--base-month', required=True,
                        help='基準月（予想を行う月、YYYY-MM形式）例: 2025-02')
    parser.add_argument('--reference-month', default='2025-11',
                        help='シナリオ参照月（デフォルト: 2025-11）')
    parser.add_argument('--csv-path',
                        default='../dataset/monthly_mci_interpolated_ppp_2022_2025.csv',
                        help='月次MCIデータのCSVパス')

    args = parser.parse_args()

    # データ読み込み
    data = load_monthly_data(args.csv_path)

    # 基準月と予想月の計算
    base_year, base_month = map(int, args.base_month.split('-'))
    if base_month == 12:
        target_month = f"{base_year + 1}-01"
    else:
        target_month = f"{base_year}-{base_month + 1:02d}"

    # 参照月の次月を計算
    ref_year, ref_month = map(int, args.reference_month.split('-'))
    if ref_month == 12:
        ref_next_month = f"{ref_year + 1}-01"
    else:
        ref_next_month = f"{ref_year}-{ref_month + 1:02d}"

    print(f"基準月: {args.base_month} → 予想月: {target_month}")
    print(f"参照シナリオ: {args.reference_month} → {ref_next_month}")
    print()

    # シナリオ変化量を抽出
    scenario_deltas = extract_scenario_deltas(data, args.reference_month, ref_next_month)

    # 基準月データを取得
    base_data = get_month_data(data, args.base_month)

    # 予想月データを取得（実績比較用）
    target_data = get_month_data(data, target_month)

    # シナリオを適用
    scenarios = apply_scenario_to_base(base_data, scenario_deltas)

    # 価格計算
    prices = calculate_prices(scenarios, target_data['PPP_JPY'], target_data['PPP_TRY'])

    # レンジ計算
    center_m_diff = {
        'usdjpy': scenarios['A（慣性維持）']['m_usd'] - scenarios['A（慣性維持）']['m_jpy']
    }
    ranges = calculate_ranges(prices, center_m_diff)

    # 結果出力
    print(f"=== {target_month}の推定レンジと実績比較 ===")
    print()
    print(format_output(ranges, target_data))
    print()
    print("※中心シナリオ: 3つのシナリオから得られる範囲")
    print("※リスクレンジ: 過去の月次変動(±0.05)を考慮した統計的変動範囲")
    print("※誤差率: (中心シナリオの中央値 - 実績値) / 実績値")

if __name__ == '__main__':
    main()
