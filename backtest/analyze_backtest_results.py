#!/usr/bin/env python3
"""
バックテスト結果の詳細分析

的中率、誤差分布、外れた月の特徴などを分析する
"""

import csv
import math
from typing import List, Dict

def load_results(csv_path: str) -> List[Dict]:
    """結果CSVを読み込む"""
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def analyze_hit_rates(results: List[Dict]) -> Dict:
    """レンジ的中率を分析"""
    pairs = ['USDJPY', 'USDTRY', 'TRYJPY']
    analysis = {}

    for pair in pairs:
        center_hits = 0
        risk_hits = 0
        total = len(results)

        misses = []

        for row in results:
            actual = float(row[f'{pair}_actual'])
            center_min = float(row[f'{pair}_pred_center_min'])
            center_max = float(row[f'{pair}_pred_center_max'])
            risk_lower = float(row[f'{pair}_pred_risk_lower'])
            risk_upper = float(row[f'{pair}_pred_risk_upper'])
            error_pct = float(row[f'{pair}_error_pct'])

            # 中心シナリオレンジ内か
            if center_min <= actual <= center_max:
                center_hits += 1

            # リスクレンジ内か
            if risk_lower <= actual <= risk_upper:
                risk_hits += 1
            else:
                # 外れた月を記録
                misses.append({
                    'month': row['target_month'],
                    'base_month': row['base_month'],
                    'actual': actual,
                    'risk_lower': risk_lower,
                    'risk_upper': risk_upper,
                    'error_pct': error_pct
                })

        analysis[pair] = {
            'center_hit_rate': center_hits / total * 100,
            'risk_hit_rate': risk_hits / total * 100,
            'center_hits': center_hits,
            'risk_hits': risk_hits,
            'total': total,
            'misses': misses
        }

    return analysis

def analyze_error_distribution(results: List[Dict]) -> Dict:
    """誤差分布を分析"""
    pairs = ['USDJPY', 'USDTRY', 'TRYJPY']
    distribution = {}

    for pair in pairs:
        errors = [float(row[f'{pair}_error_pct']) for row in results]
        abs_errors = [abs(e) for e in errors]

        # 誤差範囲ごとの件数
        ranges = {
            '0-1%': sum(1 for e in abs_errors if e <= 1),
            '1-2%': sum(1 for e in abs_errors if 1 < e <= 2),
            '2-3%': sum(1 for e in abs_errors if 2 < e <= 3),
            '3-5%': sum(1 for e in abs_errors if 3 < e <= 5),
            '5-10%': sum(1 for e in abs_errors if 5 < e <= 10),
            '>10%': sum(1 for e in abs_errors if e > 10)
        }

        distribution[pair] = {
            'ranges': ranges,
            'avg_error': sum(errors) / len(errors),
            'avg_abs_error': sum(abs_errors) / len(abs_errors),
            'max_error': max(abs_errors),
            'min_error': min(abs_errors),
            'std_dev': math.sqrt(sum((e - sum(errors)/len(errors))**2 for e in errors) / len(errors))
        }

    return distribution

def find_worst_predictions(results: List[Dict], top_n: int = 5) -> Dict:
    """最も外れた予想を特定"""
    pairs = ['USDJPY', 'USDTRY', 'TRYJPY']
    worst = {}

    for pair in pairs:
        errors = []
        for row in results:
            errors.append({
                'month': row['target_month'],
                'base_month': row['base_month'],
                'error_pct': abs(float(row[f'{pair}_error_pct'])),
                'actual': float(row[f'{pair}_actual']),
                'pred_mid': float(row[f'{pair}_pred_center_mid'])
            })

        errors.sort(key=lambda x: x['error_pct'], reverse=True)
        worst[pair] = errors[:top_n]

    return worst

def main():
    import sys

    print("Loading backtest results...")
    all_results = load_results('backtest_results_2022_2025.csv')

    # コマンドライン引数でフィルタ期間を指定可能
    start_date = sys.argv[1] if len(sys.argv) > 1 else None

    if start_date:
        results = [r for r in all_results if r['target_month'] >= start_date]
        print(f"Filtered to {start_date} onwards: {len(results)} months")
        print(f"(Excluded: {len(all_results) - len(results)} months)\n")
    else:
        results = all_results
        print(f"Total predictions: {len(results)} months\n")
    print("="*80)
    print("1. RANGE HIT RATE ANALYSIS")
    print("="*80)

    hit_analysis = analyze_hit_rates(results)

    for pair, data in hit_analysis.items():
        print(f"\n{pair}:")
        print(f"  Center Scenario Hit Rate: {data['center_hit_rate']:.1f}% ({data['center_hits']}/{data['total']})")
        print(f"  Risk Range Hit Rate:      {data['risk_hit_rate']:.1f}% ({data['risk_hits']}/{data['total']})")

        if data['misses']:
            print(f"  Risk Range Misses: {len(data['misses'])} months")
            print(f"    Worst miss: {data['misses'][0]['month']} (error: {data['misses'][0]['error_pct']:+.2f}%)")

    print("\n" + "="*80)
    print("2. ERROR DISTRIBUTION")
    print("="*80)

    error_dist = analyze_error_distribution(results)

    for pair, data in error_dist.items():
        print(f"\n{pair}:")
        print(f"  Average Error:     {data['avg_error']:+.2f}%")
        print(f"  Avg Absolute Err:  {data['avg_abs_error']:.2f}%")
        print(f"  Std Deviation:     {data['std_dev']:.2f}%")
        print(f"  Min Error:         {data['min_error']:.2f}%")
        print(f"  Max Error:         {data['max_error']:.2f}%")
        print(f"\n  Error Distribution:")
        for range_name, count in data['ranges'].items():
            pct = count / len(results) * 100
            bar = '#' * int(pct / 2)
            print(f"    {range_name:>6}: {count:2} ({pct:4.1f}%) {bar}")

    print("\n" + "="*80)
    print("3. WORST PREDICTIONS (Top 5)")
    print("="*80)

    worst = find_worst_predictions(results, top_n=5)

    for pair, predictions in worst.items():
        print(f"\n{pair}:")
        for i, pred in enumerate(predictions, 1):
            print(f"  {i}. {pred['base_month']} -> {pred['month']}: "
                  f"predicted {pred['pred_mid']:.2f}, actual {pred['actual']:.2f} "
                  f"(error: {pred['error_pct']:.2f}%)")

    print("\n" + "="*80)
    print("4. OVERALL ASSESSMENT")
    print("="*80)

    # 全体的な評価
    avg_center_hit = sum(d['center_hit_rate'] for d in hit_analysis.values()) / 3
    avg_risk_hit = sum(d['risk_hit_rate'] for d in hit_analysis.values()) / 3
    avg_abs_error = sum(d['avg_abs_error'] for d in error_dist.values()) / 3

    print(f"\nAverage Center Scenario Hit Rate: {avg_center_hit:.1f}%")
    print(f"Average Risk Range Hit Rate:      {avg_risk_hit:.1f}%")
    print(f"Average Absolute Error:           {avg_abs_error:.2f}%")

    print("\nInterpretation:")
    if avg_risk_hit >= 90:
        print("  Risk ranges are RELIABLE - cover most actual outcomes")
    elif avg_risk_hit >= 80:
        print("  Risk ranges are MODERATELY RELIABLE - cover most cases")
    elif avg_risk_hit >= 70:
        print("  Risk ranges are SOMEWHAT RELIABLE - miss ~30% of cases")
    else:
        print("  Risk ranges are UNRELIABLE - miss too many cases")

    if avg_abs_error <= 2:
        print("  Prediction accuracy is GOOD for monthly forecasts")
    elif avg_abs_error <= 3:
        print("  Prediction accuracy is MODERATE for monthly forecasts")
    else:
        print("  Prediction accuracy is LIMITED for practical use")

    # リスクレンジを外れた月の共通点を探す
    print("\n" + "="*80)
    print("5. ANALYSIS OF RISK RANGE MISSES")
    print("="*80)

    all_misses = set()
    for pair, data in hit_analysis.items():
        for miss in data['misses']:
            all_misses.add(miss['month'])

    if all_misses:
        print(f"\nMonths where at least one pair missed risk range: {len(all_misses)}")
        print("Months:", ', '.join(sorted(all_misses)))

        # 年ごとの分布
        year_dist = {}
        for month in all_misses:
            year = month.split('-')[0]
            year_dist[year] = year_dist.get(year, 0) + 1

        print("\nDistribution by year:")
        for year, count in sorted(year_dist.items()):
            print(f"  {year}: {count} months")
    else:
        print("\nNo months missed the risk range for any pair!")

if __name__ == '__main__':
    main()
