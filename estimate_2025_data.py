#!/usr/bin/env python3
"""
2025年データの推測
実際のレートと推定PPPからMCI座標を計算
"""

import csv
import math

# データ読み込み
data = []
with open('dataset/mikan_3currency_clr_index_ppp_data.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append({
            'year': int(row['year']),
            'S_USDJPY': float(row['S_USDJPY']),
            'S_USDTRY': float(row['S_USDTRY']),
            'PPP_JPY': float(row['PPP_JPY']),
            'PPP_TRY': float(row['PPP_TRY']),
        })

print("=" * 80)
print("2025年データ推定")
print("=" * 80)
print()

# 直近3年のPPP変化率を分析
recent_years = data[-3:]
print("直近3年のPPP推移:")
print("-" * 80)
for d in recent_years:
    print(f"{d['year']}: PPP_JPY={d['PPP_JPY']:.2f}, PPP_TRY={d['PPP_TRY']:.2f}")
print()

# PPPの年次成長率を計算
ppp_jpy_growth_rates = []
ppp_try_growth_rates = []

for i in range(1, len(data)):
    jpy_rate = (data[i]['PPP_JPY'] / data[i-1]['PPP_JPY']) - 1
    try_rate = (data[i]['PPP_TRY'] / data[i-1]['PPP_TRY']) - 1
    ppp_jpy_growth_rates.append(jpy_rate)
    ppp_try_growth_rates.append(try_rate)

# 直近5年平均
recent_jpy_growth = sum(ppp_jpy_growth_rates[-5:]) / 5
recent_try_growth = sum(ppp_try_growth_rates[-5:]) / 5

print("PPP年次成長率（直近5年平均）:")
print(f"  JPY: {recent_jpy_growth*100:.2f}%")
print(f"  TRY: {recent_try_growth*100:.2f}%")
print()

# 2025年PPPの推定
ppp_jpy_2024 = data[-1]['PPP_JPY']
ppp_try_2024 = data[-1]['PPP_TRY']

# シナリオ1: 直近5年平均で外挿
ppp_jpy_2025_s1 = ppp_jpy_2024 * (1 + recent_jpy_growth)
ppp_try_2025_s1 = ppp_try_2024 * (1 + recent_try_growth)

# シナリオ2: 直近1年の変化をそのまま適用
jpy_2024_growth = (data[-1]['PPP_JPY'] / data[-2]['PPP_JPY']) - 1
try_2024_growth = (data[-1]['PPP_TRY'] / data[-2]['PPP_TRY']) - 1

ppp_jpy_2025_s2 = ppp_jpy_2024 * (1 + jpy_2024_growth)
ppp_try_2025_s2 = ppp_try_2024 * (1 + try_2024_growth)

# シナリオ3: ほぼ据え置き（直近の傾向では円のPPPは横ばい）
ppp_jpy_2025_s3 = ppp_jpy_2024
ppp_try_2025_s3 = ppp_try_2024 * 1.50  # トルコは高インフレ継続

print("2025年PPP推定（3シナリオ）:")
print("-" * 80)
print(f"シナリオ1（5年平均）: PPP_JPY={ppp_jpy_2025_s1:.2f}, PPP_TRY={ppp_try_2025_s1:.2f}")
print(f"シナリオ2（直近1年）: PPP_JPY={ppp_jpy_2025_s2:.2f}, PPP_TRY={ppp_try_2025_s2:.2f}")
print(f"シナリオ3（据置+高インフレ）: PPP_JPY={ppp_jpy_2025_s3:.2f}, PPP_TRY={ppp_try_2025_s3:.2f}")
print()

# 実際のレート（ユーザー提供情報）
print("2025年実勢レート（現在値）:")
print("-" * 80)
s_usdjpy_2025 = 157.0  # ユーザー提供
print(f"USD/JPY = {s_usdjpy_2025}")
print()
print("USD/TRYは？（現在のドルリラレートを入力してください）")
print("参考: 2024年は32.88でした")
print()

# いくつかのUSD/TRYシナリオで計算
usdtry_scenarios = [35.0, 38.0, 40.0, 42.0, 45.0, 50.0]

print("=" * 80)
print("USD/TRYシナリオ別のMCI座標計算")
print("=" * 80)
print()

# 使用するPPP: シナリオ3（据置+高インフレ）を採用
ppp_jpy_2025 = ppp_jpy_2025_s3
ppp_try_2025 = ppp_try_2025_s3

print(f"使用PPP: JPY={ppp_jpy_2025:.2f}, TRY={ppp_try_2025:.2f}")
print()

for s_usdtry in usdtry_scenarios:
    # PPP乖離率計算
    d_usdjpy = math.log(s_usdjpy_2025 / ppp_jpy_2025)
    d_usdtry = math.log(s_usdtry / ppp_try_2025)

    # MCI座標計算
    m_usd = (d_usdjpy + d_usdtry) / 3
    m_jpy = (-2*d_usdjpy + d_usdtry) / 3
    m_try = (d_usdjpy - 2*d_usdtry) / 3

    # TRY/JPY
    s_tryjpy = s_usdjpy_2025 / s_usdtry

    # 2024年からの変動
    m_try_2024 = data[-1]['PPP_JPY'] * math.exp((math.log(data[-1]['S_USDJPY']/data[-1]['PPP_JPY']) - 2*math.log(data[-1]['S_USDTRY']/data[-1]['PPP_TRY']))/3)
    # 正しい計算
    d_uj_2024 = math.log(data[-1]['S_USDJPY'] / data[-1]['PPP_JPY'])
    d_ut_2024 = math.log(data[-1]['S_USDTRY'] / data[-1]['PPP_TRY'])
    m_try_2024_correct = (d_uj_2024 - 2*d_ut_2024) / 3

    D_m_try = m_try - m_try_2024_correct

    print(f"USD/TRY = {s_usdtry:.2f}:")
    print(f"  TRY/JPY = {s_tryjpy:.4f}")
    print(f"  d_USDJPY = {d_usdjpy:.6f}, d_USDTRY = {d_usdtry:.6f}")
    print(f"  m[USD] = {m_usd:+.6f}")
    print(f"  m[JPY] = {m_jpy:+.6f}")
    print(f"  m[TRY] = {m_try:+.6f} (変動: {D_m_try:+.6f})")

    # 深度判定
    if D_m_try >= -0.05:
        depth = "正常"
    elif D_m_try >= -0.06:
        depth = "深度1"
    elif D_m_try >= -0.08:
        depth = "深度2"
    else:
        depth = "深度3"

    print(f"  → 年次変動: {depth}")
    print()

print("=" * 80)
print("推奨:")
print("  現在のドルリラレートを確認して、適切なシナリオを選択してください")
print("=" * 80)
