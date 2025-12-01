#!/usr/bin/env python3
"""
バックテスト用データセット作成スクリプト

既存の monthly_mci_interpolated_ppp_2022_2025.csv に
前月とのm座標変動値（delta_m_USD, delta_m_JPY, delta_m_TRY）を追加
"""

import pandas as pd
import numpy as np

# 既存データを読み込み
input_file = 'monthly_mci_interpolated_ppp_2022_2025.csv'
output_file = 'monthly_mci_with_deltas_2022_2025.csv'

print(f"Reading {input_file}...")
df = pd.read_csv(input_file)

# 前月とのm座標変動を計算
df['delta_m_USD'] = df['m_USD'].diff()
df['delta_m_JPY'] = df['m_JPY'].diff()
df['delta_m_TRY'] = df['m_TRY'].diff()

# 最初の月はNaNになるので、そのまま残す（またはゼロにする場合は .fillna(0)）
# ここではNaNのままにして、バックテストで適切に処理する

# 結果を保存
print(f"Saving to {output_file}...")
df.to_csv(output_file, index=False, float_format='%.15g')

print("\n=== Summary ===")
print(f"Total rows: {len(df)}")
print(f"Date range: {df['date'].iloc[0]} to {df['date'].iloc[-1]}")
print("\nNew columns added:")
print("  - delta_m_USD: USD m-coordinate change from previous month")
print("  - delta_m_JPY: JPY m-coordinate change from previous month")
print("  - delta_m_TRY: TRY m-coordinate change from previous month")
print(f"\nOutput saved to: {output_file}")

# サンプルを表示
print("\nSample data (first 5 rows, selected columns):")
print(df[['date', 'm_USD', 'delta_m_USD', 'm_JPY', 'delta_m_JPY', 'm_TRY', 'delta_m_TRY']].head())

print("\nSample data (last 5 rows, selected columns):")
print(df[['date', 'm_USD', 'delta_m_USD', 'm_JPY', 'delta_m_JPY', 'm_TRY', 'delta_m_TRY']].tail())
