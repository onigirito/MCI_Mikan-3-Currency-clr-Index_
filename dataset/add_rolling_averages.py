#!/usr/bin/env python3
"""
バックテスト用データセット：3カ月移動平均を追加

過去3カ月のm座標変動の平均を計算し、シナリオの中心軸として使用
"""

import pandas as pd
import numpy as np

# データを読み込み
input_file = 'monthly_mci_with_deltas_2022_2025.csv'
output_file = 'monthly_mci_backtest_ready_2022_2025.csv'

print(f"Reading {input_file}...")
df = pd.read_csv(input_file)

# 過去3カ月の差分の移動平均を計算
# rolling(3, min_periods=1) を使うと、データが3ヶ月未満でも計算可能
df['avg_delta_m_USD_3m'] = df['delta_m_USD'].rolling(window=3, min_periods=1).mean()
df['avg_delta_m_JPY_3m'] = df['delta_m_JPY'].rolling(window=3, min_periods=1).mean()
df['avg_delta_m_TRY_3m'] = df['delta_m_TRY'].rolling(window=3, min_periods=1).mean()

# 結果を保存
print(f"Saving to {output_file}...")
df.to_csv(output_file, index=False, float_format='%.15g')

print("\n=== Summary ===")
print(f"Total rows: {len(df)}")
print(f"Date range: {df['date'].iloc[0]} to {df['date'].iloc[-1]}")
print("\nNew columns added:")
print("  - avg_delta_m_USD_3m: 3-month rolling average of USD m-coordinate change")
print("  - avg_delta_m_JPY_3m: 3-month rolling average of JPY m-coordinate change")
print("  - avg_delta_m_TRY_3m: 3-month rolling average of TRY m-coordinate change")
print(f"\nOutput saved to: {output_file}")

# サンプルを表示
print("\nSample data (rows 3-8, showing trend calculation):")
sample_cols = ['date', 'delta_m_USD', 'avg_delta_m_USD_3m',
               'delta_m_JPY', 'avg_delta_m_JPY_3m',
               'delta_m_TRY', 'avg_delta_m_TRY_3m']
print(df[sample_cols].iloc[2:8].to_string(index=False))

print("\nLatest data (last 3 rows):")
print(df[sample_cols].tail(3).to_string(index=False))

print("\n=== Usage Note ===")
print("For predicting month N+1:")
print("  - Use row N's avg_delta_m_*_3m as the central scenario")
print("  - This represents the average trend from months N-2, N-1, N")
print("  - Apply this delta to month N's m-coordinates to predict month N+1")
