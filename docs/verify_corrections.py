#!/usr/bin/env python3
"""
論文修正版の検証スクリプト

修正後の式(1)が実データと一致することを確認します。
"""

import csv
import math

def verify_formula(year, d_uj, d_ut, m_usd_actual, m_jpy_actual, m_try_actual):
    """修正後の式(1)で計算した値が実データと一致するか検証"""

    # 修正後の式(1)で計算
    m_usd_calc = (d_uj + d_ut) / 3
    m_jpy_calc = (-2 * d_uj + d_ut) / 3
    m_try_calc = (d_uj - 2 * d_ut) / 3

    # 誤差判定
    epsilon = 1e-6
    usd_match = abs(m_usd_calc - m_usd_actual) < epsilon
    jpy_match = abs(m_jpy_calc - m_jpy_actual) < epsilon
    try_match = abs(m_try_calc - m_try_actual) < epsilon

    # ゼロサム確認
    sum_check = abs(m_usd_calc + m_jpy_calc + m_try_calc) < epsilon

    print(f"\n【{year}年の検証】")
    print(f"d_USDJPY = {d_uj:.6f}")
    print(f"d_USDTRY = {d_ut:.6f}")
    print()
    print("修正後の式(1)で計算:")
    print(f"  m[USD] = {m_usd_calc:.6f}  (実データ: {m_usd_actual:.6f}) {'✓' if usd_match else '✗'}")
    print(f"  m[JPY] = {m_jpy_calc:.6f}  (実データ: {m_jpy_actual:.6f}) {'✓' if jpy_match else '✗'}")
    print(f"  m[TRY] = {m_try_calc:.6f}  (実データ: {m_try_actual:.6f}) {'✓' if try_match else '✗'}")
    print(f"  合計   = {m_usd_calc + m_jpy_calc + m_try_calc:.10f} {'✓' if sum_check else '✗'}")

    # 差分関係の確認
    print()
    print("差分関係の確認:")
    diff_usd_jpy = m_usd_calc - m_jpy_calc
    diff_usd_try = m_usd_calc - m_try_calc
    print(f"  m[USD] - m[JPY] = {diff_usd_jpy:.6f}  (d_USDJPY: {d_uj:.6f}) {'✓' if abs(diff_usd_jpy - d_uj) < epsilon else '✗'}")
    print(f"  m[USD] - m[TRY] = {diff_usd_try:.6f}  (d_USDTRY: {d_ut:.6f}) {'✓' if abs(diff_usd_try - d_ut) < epsilon else '✗'}")

    return all([usd_match, jpy_match, try_match, sum_check])

def interpret_signs(year, m_usd, m_jpy, m_try, d_uj, d_ut):
    """符号の経済的解釈を表示"""
    print(f"\n【{year}年の経済的解釈】")

    # d_USDJPYの解釈
    if d_uj > 0:
        print(f"d_USDJPY = {d_uj:.3f} > 0 → 円安/ドル高")
    elif d_uj < 0:
        print(f"d_USDJPY = {d_uj:.3f} < 0 → 円高/ドル安")
    else:
        print(f"d_USDJPY = {d_uj:.3f} ≈ 0 → 円は適正水準")

    # d_USDTRYの解釈
    if d_ut > 0.5:
        print(f"d_USDTRY = {d_ut:.3f} >> 0 → リラ大幅安/ドル高")
    elif d_ut > 0:
        print(f"d_USDTRY = {d_ut:.3f} > 0 → リラ安/ドル高")
    elif d_ut < 0:
        print(f"d_USDTRY = {d_ut:.3f} < 0 → リラ高/ドル安")

    print()
    print("修正後の解釈（負=割安、正=割高）:")

    # USDの解釈
    if m_usd > 0.3:
        print(f"  m[USD] = {m_usd:.3f} > 0 → ドルは大幅に割高")
    elif m_usd > 0:
        print(f"  m[USD] = {m_usd:.3f} > 0 → ドルは割高")
    elif m_usd < 0:
        print(f"  m[USD] = {m_usd:.3f} < 0 → ドルは割安")

    # JPYの解釈
    if m_jpy > 0.3:
        print(f"  m[JPY] = {m_jpy:.3f} > 0 → 円は大幅に割高（円高）")
    elif m_jpy > 0:
        print(f"  m[JPY] = {m_jpy:.3f} > 0 → 円は割高（円高傾向）")
    elif m_jpy < 0:
        print(f"  m[JPY] = {m_jpy:.3f} < 0 → 円は割安（円安傾向）")

    # TRYの解釈
    if m_try < -0.5:
        print(f"  m[TRY] = {m_try:.3f} << 0 → リラは極端に割安（暴落）")
    elif m_try < -0.3:
        print(f"  m[TRY] = {m_try:.3f} < 0 → リラは大幅に割安")
    elif m_try < 0:
        print(f"  m[TRY] = {m_try:.3f} < 0 → リラは割安")
    elif m_try > 0:
        print(f"  m[TRY] = {m_try:.3f} > 0 → リラは割高")

def main():
    print("=" * 80)
    print("論文修正版の検証")
    print("=" * 80)

    # CSVデータを読み込み
    with open('../dataset/mikan_3currency_clr_index_ppp_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # 重要な年度を検証
    test_years = [2005, 2011, 2018, 2022, 2024]

    all_pass = True
    for year in test_years:
        row = [r for r in data if r['year'] == str(year)][0]

        d_uj = float(row['d_USDJPY'])
        d_ut = float(row['d_USDTRY'])
        m_usd = float(row['m_USD'])
        m_jpy = float(row['m_JPY'])
        m_try = float(row['m_TRY'])

        passed = verify_formula(year, d_uj, d_ut, m_usd, m_jpy, m_try)
        interpret_signs(year, m_usd, m_jpy, m_try, d_uj, d_ut)

        all_pass = all_pass and passed

    print("\n" + "=" * 80)
    if all_pass:
        print("✓ 全ての年度で修正後の式(1)が実データと一致しました！")
    else:
        print("✗ 一部の年度で不一致がありました")
    print("=" * 80)

    # 統計量の計算
    print("\n【全期間（2005-2024）の統計量】")
    m_usd_values = [float(r['m_USD']) for r in data]
    m_jpy_values = [float(r['m_JPY']) for r in data]
    m_try_values = [float(r['m_TRY']) for r in data]

    m_usd_mean = sum(m_usd_values) / len(m_usd_values)
    m_jpy_mean = sum(m_jpy_values) / len(m_jpy_values)
    m_try_mean = sum(m_try_values) / len(m_try_values)

    m_usd_std = (sum((x - m_usd_mean)**2 for x in m_usd_values) / len(m_usd_values)) ** 0.5
    m_jpy_std = (sum((x - m_jpy_mean)**2 for x in m_jpy_values) / len(m_jpy_values)) ** 0.5
    m_try_std = (sum((x - m_try_mean)**2 for x in m_try_values) / len(m_try_values)) ** 0.5

    print(f"m[USD]: 平均 = {m_usd_mean:+.3f}, 標準偏差 = {m_usd_std:.3f}")
    print(f"m[JPY]: 平均 = {m_jpy_mean:+.3f}, 標準偏差 = {m_jpy_std:.3f}")
    print(f"m[TRY]: 平均 = {m_try_mean:+.3f}, 標準偏差 = {m_try_std:.3f}")
    print()
    print("解釈:")
    print(f"  - USDは平均的に{'+割高' if m_usd_mean > 0 else '割安'}傾向（平均 {m_usd_mean:+.3f}）")
    print(f"  - JPYは平均的に{'+割高' if m_jpy_mean > 0 else '割安'}傾向（平均 {m_jpy_mean:+.3f}）")
    print(f"  - TRYは平均的に{'+割高' if m_try_mean > 0 else '割安'}傾向（平均 {m_try_mean:+.3f}）")
    print(f"  - TRYの変動が最大（標準偏差 {m_try_std:.3f}）、JPYが最小（標準偏差 {m_jpy_std:.3f}）")

if __name__ == '__main__':
    main()
