#!/usr/bin/env python3
"""
3カ月平均ベースのバックテスト結果を分析

使い方:
  python analyze_rolling_avg_results.py
  python analyze_rolling_avg_results.py 2023-08  # 指定月以降のみ分析
"""

import sys
import csv
import math
from typing import List, Dict
from datetime import datetime

def load_results(csv_path: str) -> List[Dict]:
    """バックテスト結果を読み込む"""
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def filter_by_start_month(results: List[Dict], start_month: str) -> List[Dict]:
    """指定月以降の結果のみを抽出"""
    return [r for r in results if r['target_month'] >= start_month]

def calculate_metrics(errors: List[float]) -> Dict:
    """誤差指標を計算"""
    n = len(errors)
    if n == 0:
        return {'mean': 0, 'mae': 0, 'rmse': 0}

    mean_error = sum(errors) / n
    mae = sum(abs(e) for e in errors) / n
    rmse = math.sqrt(sum(e**2 for e in errors) / n)

    return {
        'mean': mean_error,
        'mae': mae,
        'rmse': rmse
    }

def analyze_distribution(errors: List[float]) -> Dict[str, int]:
    """誤差分布を計算"""
    bins = {
        '0-1%': 0,
        '1-2%': 0,
        '2-3%': 0,
        '3-5%': 0,
        '5-10%': 0,
        '10%+': 0
    }

    for e in errors:
        abs_e = abs(e)
        if abs_e < 1:
            bins['0-1%'] += 1
        elif abs_e < 2:
            bins['1-2%'] += 1
        elif abs_e < 3:
            bins['2-3%'] += 1
        elif abs_e < 5:
            bins['3-5%'] += 1
        elif abs_e < 10:
            bins['5-10%'] += 1
        else:
            bins['10%+'] += 1

    return bins

def get_worst_predictions(results: List[Dict], pair: str, n: int = 5) -> List[Dict]:
    """最も外れた予想を取得"""
    pair_results = []
    for r in results:
        error = abs(float(r[f'error_pct_{pair}']))
        pair_results.append({
            'month': r['target_month'],
            'error': error,
            'pred': float(r[f'pred_{pair}']),
            'actual': float(r[f'actual_{pair}'])
        })

    pair_results.sort(key=lambda x: x['error'], reverse=True)
    return pair_results[:n]

def main():
    csv_path = 'backtest_rolling_avg_results.csv'

    # 開始月の指定
    start_month = sys.argv[1] if len(sys.argv) > 1 else None

    print("=" * 70)
    print("3カ月平均ベース バックテスト結果分析")
    print("=" * 70)

    # データ読み込み
    results = load_results(csv_path)
    total_count = len(results)

    if start_month:
        results = filter_by_start_month(results, start_month)
        print(f"\n分析期間: {start_month} 以降")
    else:
        print(f"\n分析期間: 全期間")

    print(f"対象月数: {len(results)}ヶ月 (全体: {total_count}ヶ月)")
    if results:
        print(f"期間: {results[0]['target_month']} 〜 {results[-1]['target_month']}")

    # 各通貨ペアの分析
    pairs = ['USDJPY', 'USDTRY', 'TRYJPY']

    print("\n" + "=" * 70)
    print("1. 精度指標サマリー")
    print("=" * 70)
    print(f"\n{'通貨ペア':<10} {'件数':<6} {'平均誤差':<10} {'平均絶対誤差':<12} {'RMSE':<10}")
    print("-" * 70)

    all_metrics = {}
    for pair in pairs:
        errors = [float(r[f'error_pct_{pair}']) for r in results]
        metrics = calculate_metrics(errors)
        all_metrics[pair] = metrics

        print(f"{pair:<10} {len(errors):<6} {metrics['mean']:>+8.2f}%  {metrics['mae']:>10.2f}%  {metrics['rmse']:>8.2f}%")

    # 誤差分布
    print("\n" + "=" * 70)
    print("2. 誤差分布")
    print("=" * 70)

    for pair in pairs:
        errors = [float(r[f'error_pct_{pair}']) for r in results]
        distribution = analyze_distribution(errors)

        print(f"\n{pair}:")
        for bin_name, count in distribution.items():
            pct = (count / len(errors)) * 100 if errors else 0
            bar = "■" * int(pct / 2)
            print(f"  {bin_name:<8}: {count:>3}件 ({pct:>5.1f}%) {bar}")

    # 最も外れた予想
    print("\n" + "=" * 70)
    print("3. 最も外れた予想 Top 5")
    print("=" * 70)

    for pair in pairs:
        worst = get_worst_predictions(results, pair, 5)
        print(f"\n{pair}:")
        for i, w in enumerate(worst, 1):
            print(f"  {i}. {w['month']}: 誤差 {w['error']:.2f}% (予想 {w['pred']:.2f} vs 実績 {w['actual']:.2f})")

    # 総合評価
    print("\n" + "=" * 70)
    print("4. 総合評価")
    print("=" * 70)

    avg_mae = sum(m['mae'] for m in all_metrics.values()) / len(all_metrics)
    avg_rmse = sum(m['rmse'] for m in all_metrics.values()) / len(all_metrics)

    print(f"\n平均絶対誤差（3通貨ペア平均）: {avg_mae:.2f}%")
    print(f"RMSE（3通貨ペア平均）: {avg_rmse:.2f}%")

    print("\n評価:")
    if avg_mae < 2.0:
        print("  [EXCELLENT] 非常に高精度（MAE < 2%）")
    elif avg_mae < 3.0:
        print("  [GOOD] 良好な精度（MAE < 3%）")
    elif avg_mae < 4.0:
        print("  [OK] 実用可能な精度（MAE < 4%）")
    else:
        print("  [POOR] 精度改善が必要（MAE >= 4%）")

    # バイアス評価
    print("\nバイアス評価:")
    for pair in pairs:
        mean_error = all_metrics[pair]['mean']
        if abs(mean_error) < 0.5:
            bias_str = "ほぼニュートラル"
        elif mean_error > 0:
            bias_str = "やや高めに予測"
        else:
            bias_str = "やや低めに予測"
        print(f"  {pair}: {mean_error:+.2f}% ({bias_str})")

    # 期間別比較の提案
    if not start_month and len(results) >= 28:
        print("\n" + "=" * 70)
        print("安定期のみの分析を見るには:")
        print(f"  python {sys.argv[0]} 2023-08")
        print("=" * 70)

if __name__ == '__main__':
    main()
