#!/usr/bin/env python3
"""
2025年データを作成してデータセットに追加
"""

import csv
import math

# 2025年の実勢レート（現在値）
S_USDJPY_2025 = 157.0
S_USDTRY_2025 = 42.3

# 既存データ読み込み
data = []
with open('dataset/mikan_3currency_clr_index_ppp_data.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

# 2024年データ
data_2024 = data[-1]
ppp_jpy_2024 = float(data_2024['PPP_JPY'])
ppp_try_2024 = float(data_2024['PPP_TRY'])

# PPP推定（シナリオ3: 円は据え置き、リラは50%インフレ）
PPP_JPY_2025 = ppp_jpy_2024  # 93.20（据え置き）
PPP_TRY_2025 = ppp_try_2024 * 1.50  # 18.825

print("=" * 80)
print("2025年データ作成")
print("=" * 80)
print()
print("入力値:")
print(f"  USD/JPY = {S_USDJPY_2025}")
print(f"  USD/TRY = {S_USDTRY_2025}")
print()
print("PPP推定値:")
print(f"  PPP_JPY = {PPP_JPY_2025:.2f} (2024: {ppp_jpy_2024:.2f})")
print(f"  PPP_TRY = {PPP_TRY_2025:.2f} (2024: {ppp_try_2024:.2f})")
print()

# PPP乖離率計算
d_USDJPY = math.log(S_USDJPY_2025 / PPP_JPY_2025)
d_USDTRY = math.log(S_USDTRY_2025 / PPP_TRY_2025)

# MCI座標計算
m_USD = (d_USDJPY + d_USDTRY) / 3
m_JPY = (-2*d_USDJPY + d_USDTRY) / 3
m_TRY = (d_USDJPY - 2*d_USDTRY) / 3

# クロスレート
S_TRYJPY = S_USDJPY_2025 / S_USDTRY_2025
PPP_TRYJPY = PPP_JPY_2025 / PPP_TRY_2025
d_TRYJPY = math.log(S_TRYJPY / PPP_TRYJPY)

print("計算結果:")
print("-" * 80)
print(f"d_USDJPY = {d_USDJPY:.6f}")
print(f"d_USDTRY = {d_USDTRY:.6f}")
print()
print(f"m[USD] = {m_USD:+.6f}")
print(f"m[JPY] = {m_JPY:+.6f}")
print(f"m[TRY] = {m_TRY:+.6f}")
print(f"合計 = {m_USD + m_JPY + m_TRY:.10f} (ゼロサム確認)")
print()
print(f"TRY/JPY = {S_TRYJPY:.4f}")
print(f"PPP_TRYJPY = {PPP_TRYJPY:.4f}")
print(f"d_TRYJPY = {d_TRYJPY:.6f}")
print()

# 2024年からの変動
m_TRY_2024 = float(data_2024['m_TRY'])
m_USD_2024 = float(data_2024['m_USD'])
m_JPY_2024 = float(data_2024['m_JPY'])

D_m_USD = m_USD - m_USD_2024
D_m_JPY = m_JPY - m_JPY_2024
D_m_TRY = m_TRY - m_TRY_2024

print("2024年比変動:")
print("-" * 80)
print(f"Δm[USD] = {D_m_USD:+.6f}")
print(f"Δm[JPY] = {D_m_JPY:+.6f}")
print(f"Δm[TRY] = {D_m_TRY:+.6f}")
print()

# 深度判定
if D_m_TRY >= -0.05:
    depth = "正常域"
elif D_m_TRY >= -0.06:
    depth = "深度1（通常変動）"
elif D_m_TRY >= -0.08:
    depth = "深度2"
else:
    depth = "深度3（危機レベル）"

print(f"深度判定: {depth}")
print()

# 新しいデータ行を作成
new_row = {
    'year': '2025',
    'S_USDJPY': f'{S_USDJPY_2025:.2f}',
    'S_USDTRY': f'{S_USDTRY_2025:.2f}',
    'PPP_JPY': f'{PPP_JPY_2025:.2f}',
    'PPP_TRY': f'{PPP_TRY_2025:.2f}',
    'd_USDJPY': f'{d_USDJPY}',
    'd_USDTRY': f'{d_USDTRY}',
    'm_USD': f'{m_USD}',
    'm_JPY': f'{m_JPY}',
    'm_TRY': f'{m_TRY}',
    'S_TRYJPY': f'{S_TRYJPY}',
    'PPP_TRYJPY': f'{PPP_TRYJPY}',
    'd_TRYJPY': f'{d_TRYJPY}',
}

# データセットに追加
data.append(new_row)

# 保存
with open('dataset/mikan_3currency_clr_index_ppp_data.csv', 'w', newline='') as f:
    fieldnames = ['year', 'S_USDJPY', 'S_USDTRY', 'PPP_JPY', 'PPP_TRY',
                  'd_USDJPY', 'd_USDTRY', 'm_USD', 'm_JPY', 'm_TRY',
                  'S_TRYJPY', 'PPP_TRYJPY', 'd_TRYJPY']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print("=" * 80)
print("✓ 2025年データをデータセットに追加しました")
print("  dataset/mikan_3currency_clr_index_ppp_data.csv")
print("=" * 80)
