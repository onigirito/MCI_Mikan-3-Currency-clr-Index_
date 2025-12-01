#!/usr/bin/env python3
"""
3カ月平均ベースの月次MCI価格予想バックテストツール

過去3カ月のm座標変動平均を使った単一シナリオで予想を行う。

使い方:
  python backtest_with_rolling_avg.py --base-month 2022-03
  python backtest_with_rolling_avg.py --output my_results.csv
"""

import argparse
import csv
import math
from typing import Dict, List, Tuple

def load_monthly_data(csv_path: str) -> List[Dict]:
    """月次MCIデータ（3カ月平均含む）を読み込む"""
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
                'avg_delta_m_USD_3m': float(row['avg_delta_m_USD_3m']) if row['avg_delta_m_USD_3m'] else None,
                'avg_delta_m_JPY_3m': float(row['avg_delta_m_JPY_3m']) if row['avg_delta_m_JPY_3m'] else None,
                'avg_delta_m_TRY_3m': float(row['avg_delta_m_TRY_3m']) if row['avg_delta_m_TRY_3m'] else None,
                'S_USDJPY': float(row['S_USDJPY']),
                'S_USDTRY': float(row['S_USDTRY']),
                'S_TRYJPY': float(row['S_TRYJPY']),
                'PPP_JPY': float(row['PPP_JPY']),
                'PPP_TRY': float(row['PPP_TRY'])
            }
    raise ValueError(f"Month {target_month} not found in data")

def get_next_month(year_month: str) -> str:
    """次月の年月を返す (YYYY-MM形式)"""
    year, month = map(int, year_month.split('-'))
    if month == 12:
        return f"{year+1}-01"
    else:
        return f"{year}-{month+1:02d}"

def predict_next_month_rates(base_data: Dict, target_ppp: Dict) -> Dict:
    """
    3カ月平均変動を使って翌月の為替レートを予想

    Args:
        base_data: 基準月のデータ（3カ月平均含む）
        target_ppp: 予想対象月のPPP値

    Returns:
        予想レート
    """
    # 3カ月平均がない場合はスキップ
    if base_data['avg_delta_m_USD_3m'] is None:
        return None

    # 予想月のm座標を計算（基準月 + 3カ月平均変動）
    pred_m_usd = base_data['m_USD'] + base_data['avg_delta_m_USD_3m']
    pred_m_jpy = base_data['m_JPY'] + base_data['avg_delta_m_JPY_3m']
    pred_m_try = base_data['m_TRY'] + base_data['avg_delta_m_TRY_3m']

    # 予想レートを計算: S = PPP * exp(m_A - m_B)
    pred_usdjpy = target_ppp['PPP_JPY'] * math.exp(pred_m_usd - pred_m_jpy)
    pred_usdtry = target_ppp['PPP_TRY'] * math.exp(pred_m_usd - pred_m_try)
    pred_tryjpy = pred_usdjpy / pred_usdtry  # クロスレート: (USD/JPY) / (USD/TRY) = TRY/JPY

    return {
        'pred_USDJPY': pred_usdjpy,
        'pred_USDTRY': pred_usdtry,
        'pred_TRYJPY': pred_tryjpy,
        'pred_m_USD': pred_m_usd,
        'pred_m_JPY': pred_m_jpy,
        'pred_m_TRY': pred_m_try
    }

def run_single_backtest(data: List[Dict], base_month: str) -> Dict:
    """
    単一月のバックテストを実行

    Args:
        data: 全月次データ
        base_month: 基準月 (YYYY-MM)

    Returns:
        バックテスト結果
    """
    target_month = get_next_month(base_month)

    try:
        base_data = get_month_data(data, base_month)
        target_data = get_month_data(data, target_month)
    except ValueError as e:
        return {'error': str(e)}

    # 予想を実行
    prediction = predict_next_month_rates(base_data, target_data)

    if prediction is None:
        return {'error': f'No 3-month average data available for {base_month}'}

    # 誤差を計算
    error_usdjpy = ((prediction['pred_USDJPY'] - target_data['S_USDJPY']) / target_data['S_USDJPY']) * 100
    error_usdtry = ((prediction['pred_USDTRY'] - target_data['S_USDTRY']) / target_data['S_USDTRY']) * 100
    error_tryjpy = ((prediction['pred_TRYJPY'] - target_data['S_TRYJPY']) / target_data['S_TRYJPY']) * 100

    return {
        'base_month': base_month,
        'target_month': target_month,
        'pred_USDJPY': prediction['pred_USDJPY'],
        'actual_USDJPY': target_data['S_USDJPY'],
        'error_pct_USDJPY': error_usdjpy,
        'pred_USDTRY': prediction['pred_USDTRY'],
        'actual_USDTRY': target_data['S_USDTRY'],
        'error_pct_USDTRY': error_usdtry,
        'pred_TRYJPY': prediction['pred_TRYJPY'],
        'actual_TRYJPY': target_data['S_TRYJPY'],
        'error_pct_TRYJPY': error_tryjpy,
        'avg_delta_m_USD': base_data['avg_delta_m_USD_3m'],
        'avg_delta_m_JPY': base_data['avg_delta_m_JPY_3m'],
        'avg_delta_m_TRY': base_data['avg_delta_m_TRY_3m']
    }

def run_comprehensive_backtest(data: List[Dict], output_file: str):
    """
    全期間のバックテストを実行

    Args:
        data: 全月次データ
        output_file: 出力CSVファイル名
    """
    results = []

    # 2022-02から2025-10まで（2025-11を予想対象とするため）
    for row in data:
        base_month = row['date']

        # 最終月はスキップ（予想対象がない）
        if base_month == data[-1]['date']:
            continue

        print(f"Running backtest: {base_month} -> {get_next_month(base_month)}")
        result = run_single_backtest(data, base_month)

        if 'error' in result:
            print(f"  Skipped: {result['error']}")
            continue

        results.append(result)

        # 結果を表示
        print(f"  USDJPY: {result['pred_USDJPY']:.2f} (actual: {result['actual_USDJPY']:.2f}, error: {result['error_pct_USDJPY']:+.2f}%)")
        print(f"  USDTRY: {result['pred_USDTRY']:.2f} (actual: {result['actual_USDTRY']:.2f}, error: {result['error_pct_USDTRY']:+.2f}%)")
        print(f"  TRYJPY: {result['pred_TRYJPY']:.2f} (actual: {result['actual_TRYJPY']:.2f}, error: {result['error_pct_TRYJPY']:+.2f}%)")

    # CSVに保存
    if results:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = results[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print(f"\n[OK] Results saved to {output_file}")
        print(f"  Total predictions: {len(results)}")
    else:
        print("\n[ERROR] No valid results to save")

def main():
    parser = argparse.ArgumentParser(description='月次MCI価格予想バックテスト（3カ月平均ベース）')
    parser.add_argument('--base-month', type=str, help='基準月 (YYYY-MM形式、例: 2022-03)')
    parser.add_argument('--output', type=str, default='backtest_rolling_avg_results.csv',
                       help='出力CSVファイル名（包括的バックテスト用）')
    parser.add_argument('--comprehensive', action='store_true',
                       help='全期間の包括的バックテストを実行')

    args = parser.parse_args()

    # データ読み込み
    csv_path = '../dataset/monthly_mci_backtest_ready_2022_2025.csv'
    print(f"Loading data from {csv_path}...")
    data = load_monthly_data(csv_path)
    print(f"Loaded {len(data)} months of data\n")

    if args.comprehensive:
        # 包括的バックテスト
        run_comprehensive_backtest(data, args.output)
    elif args.base_month:
        # 単一月のバックテスト
        result = run_single_backtest(data, args.base_month)

        if 'error' in result:
            print(f"Error: {result['error']}")
            return

        print(f"=== Backtest: {result['base_month']} → {result['target_month']} ===\n")
        print(f"3-month average deltas used:")
        print(f"  USD: {result['avg_delta_m_USD']:+.6f}")
        print(f"  JPY: {result['avg_delta_m_JPY']:+.6f}")
        print(f"  TRY: {result['avg_delta_m_TRY']:+.6f}\n")
        print(f"Predictions vs Actual:")
        print(f"  USDJPY: {result['pred_USDJPY']:.2f} vs {result['actual_USDJPY']:.2f} (error: {result['error_pct_USDJPY']:+.2f}%)")
        print(f"  USDTRY: {result['pred_USDTRY']:.2f} vs {result['actual_USDTRY']:.2f} (error: {result['error_pct_USDTRY']:+.2f}%)")
        print(f"  TRYJPY: {result['pred_TRYJPY']:.3f} vs {result['actual_TRYJPY']:.3f} (error: {result['error_pct_TRYJPY']:+.2f}%)")
    else:
        print("Error: Please specify --base-month or --comprehensive")
        parser.print_help()

if __name__ == '__main__':
    main()
