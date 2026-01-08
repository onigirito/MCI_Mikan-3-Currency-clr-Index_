#!/usr/bin/env python3
"""
2022年のm座標を論文の式(1)で再計算するスクリプト

問題：2022年のm座標が旧式（符号反転前）で計算されていた
修正：論文の式(1)で正しく再計算
  m[USD] = (d_USDJPY + d_USDTRY) / 3
  m[JPY] = (-2·d_USDJPY + d_USDTRY) / 3
  m[TRY] = (d_USDJPY - 2·d_USDTRY) / 3
"""

import csv
import math
from typing import List, Dict

def calculate_m_coordinates(d_usdjpy: float, d_usdtry: float) -> tuple:
    """論文の式(1)でm座標を計算"""
    m_USD = (d_usdjpy + d_usdtry) / 3
    m_JPY = (-2 * d_usdjpy + d_usdtry) / 3
    m_TRY = (d_usdjpy - 2 * d_usdtry) / 3

    # ゼロサム検証
    zero_sum = m_USD + m_JPY + m_TRY
    assert abs(zero_sum) < 1e-10, f"Zero-sum constraint violated: {zero_sum}"

    return m_USD, m_JPY, m_TRY

def fix_monthly_mci_csv(csv_path: str):
    """月次MCIデータの2022年m座標を修正"""

    # CSVを読み込み
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print("=" * 80)
    print("2022年m座標修正スクリプト")
    print("=" * 80)

    # 2022年のm座標を再計算（行0-11）
    print("\n[1] 2022年m座標を再計算中...")
    for i, row in enumerate(rows):
        if row['date'].startswith('2022'):
            d_usdjpy = float(row['d_USDJPY'])
            d_usdtry = float(row['d_USDTRY'])

            # 旧値を保存
            old_m_USD = float(row['m_USD'])
            old_m_JPY = float(row['m_JPY'])
            old_m_TRY = float(row['m_TRY'])

            # 論文の式(1)で再計算
            m_USD, m_JPY, m_TRY = calculate_m_coordinates(d_usdjpy, d_usdtry)

            # 更新
            row['m_USD'] = str(m_USD)
            row['m_JPY'] = str(m_JPY)
            row['m_TRY'] = str(m_TRY)

            # D_mTRYも更新
            row['D_mTRY'] = str(m_TRY - m_JPY)

            print(f"{row['date']}: m_USD {old_m_USD:+.3f} → {m_USD:+.3f} (符号反転)")

    # 全期間のdelta_m_*を再計算
    print("\n[2] 全期間のdelta_m_*を再計算中...")
    for i in range(1, len(rows)):
        prev_row = rows[i-1]
        curr_row = rows[i]

        delta_m_USD = float(curr_row['m_USD']) - float(prev_row['m_USD'])
        delta_m_JPY = float(curr_row['m_JPY']) - float(prev_row['m_JPY'])
        delta_m_TRY = float(curr_row['m_TRY']) - float(prev_row['m_TRY'])

        curr_row['delta_m_USD'] = str(delta_m_USD)
        curr_row['delta_m_JPY'] = str(delta_m_JPY)
        curr_row['delta_m_TRY'] = str(delta_m_TRY)

    # 最初の行はdelta_m_*を空にする
    rows[0]['delta_m_USD'] = ''
    rows[0]['delta_m_JPY'] = ''
    rows[0]['delta_m_TRY'] = ''

    # 全期間のavg_delta_m_*_3mを再計算
    print("\n[3] 全期間のavg_delta_m_*_3mを再計算中...")
    for i in range(len(rows)):
        if i < 3:
            # 最初の3行は3カ月移動平均を計算できない
            rows[i]['avg_delta_m_USD_3m'] = ''
            rows[i]['avg_delta_m_JPY_3m'] = ''
            rows[i]['avg_delta_m_TRY_3m'] = ''
        else:
            # 過去3カ月の平均
            deltas_USD = [float(rows[j]['delta_m_USD']) for j in range(i-2, i+1)]
            deltas_JPY = [float(rows[j]['delta_m_JPY']) for j in range(i-2, i+1)]
            deltas_TRY = [float(rows[j]['delta_m_TRY']) for j in range(i-2, i+1)]

            rows[i]['avg_delta_m_USD_3m'] = str(sum(deltas_USD) / 3)
            rows[i]['avg_delta_m_JPY_3m'] = str(sum(deltas_JPY) / 3)
            rows[i]['avg_delta_m_TRY_3m'] = str(sum(deltas_TRY) / 3)

    # 予測値と誤差列をクリア（バックテスト再実行が必要）
    print("\n[4] バックテスト結果をクリア中（再実行が必要）...")
    prediction_cols = ['pred_USDJPY', 'pred_USDTRY', 'pred_TRYJPY',
                      'error_pct_USDJPY', 'error_pct_USDTRY', 'error_pct_TRYJPY']
    for row in rows:
        for col in prediction_cols:
            row[col] = ''

    # CSVを保存
    print("\n[5] CSVを保存中...")
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = list(rows[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅ 修正完了: {csv_path}")

    # 検証: 2022-12と2023-01の連続性
    print("\n[6] 連続性検証（2022-12 → 2023-01）:")
    row_2022_12 = [r for r in rows if r['date'] == '2022-12'][0]
    row_2023_01 = [r for r in rows if r['date'] == '2023-01'][0]

    print(f"  2022-12: m_USD={float(row_2022_12['m_USD']):+.3f}, "
          f"m_JPY={float(row_2022_12['m_JPY']):+.3f}, "
          f"m_TRY={float(row_2022_12['m_TRY']):+.3f}")
    print(f"  2023-01: m_USD={float(row_2023_01['m_USD']):+.3f}, "
          f"m_JPY={float(row_2023_01['m_JPY']):+.3f}, "
          f"m_TRY={float(row_2023_01['m_TRY']):+.3f}")

    # 年次データと比較
    print("\n[7] 年次データとの比較:")
    print("  annual_mci_2005_2024.csvの2022年: m_USD=+0.518, m_JPY=+0.167, m_TRY=-0.685")

    # 2022年の平均を計算
    rows_2022 = [r for r in rows if r['date'].startswith('2022')]
    avg_m_USD = sum(float(r['m_USD']) for r in rows_2022) / len(rows_2022)
    avg_m_JPY = sum(float(r['m_JPY']) for r in rows_2022) / len(rows_2022)
    avg_m_TRY = sum(float(r['m_TRY']) for r in rows_2022) / len(rows_2022)

    print(f"  monthly平均（修正後）: m_USD={avg_m_USD:+.3f}, "
          f"m_JPY={avg_m_JPY:+.3f}, m_TRY={avg_m_TRY:+.3f}")

    print("\n" + "=" * 80)
    print("次のステップ: バックテストを再実行してください")
    print("  python backtest_with_rolling_avg.py --comprehensive")
    print("=" * 80)

if __name__ == '__main__':
    csv_path = 'monthly_mci_complete_2022_2025.csv'
    fix_monthly_mci_csv(csv_path)
