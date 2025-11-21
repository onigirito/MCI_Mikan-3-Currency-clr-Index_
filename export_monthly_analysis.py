#!/usr/bin/env python3
"""
月次MCIデータを分析付きCSVとして出力
"""

import csv

# データ読み込み
data = []
with open('dataset/mci_monthly_recent.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

# 月次変動を追加
for i in range(1, len(data)):
    prev = data[i-1]
    curr = data[i]

    # m[TRY]の月次変動
    curr['D_mTRY'] = str(float(curr['m_TRY']) - float(prev['m_TRY']))

    # 価格変動率
    curr['pct_TRYJPY'] = str((float(curr['S_TRYJPY']) / float(prev['S_TRYJPY']) - 1) * 100)

    # PPP基準が変わったか
    curr['PPP_changed'] = 'YES' if curr['PPP_TRY'] != prev['PPP_TRY'] else 'NO'

# 最初の行は変動なし
data[0]['D_mTRY'] = ''
data[0]['pct_TRYJPY'] = ''
data[0]['PPP_changed'] = ''

# 出力
output_file = 'monthly_mci_analysis.csv'
fieldnames = [
    'date',
    'S_USDJPY',
    'S_USDTRY',
    'S_TRYJPY',
    'PPP_JPY',
    'PPP_TRY',
    'PPP_changed',
    'd_USDJPY',
    'd_USDTRY',
    'm_USD',
    'm_JPY',
    'm_TRY',
    'D_mTRY',
    'pct_TRYJPY',
]

with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(data)

print(f"✓ 月次MCI分析CSVを出力しました: {output_file}")
print(f"  {len(data)}行のデータ")
print()
print("列の説明:")
print("  date: 年月")
print("  S_USDJPY, S_USDTRY, S_TRYJPY: 為替レート")
print("  PPP_JPY, PPP_TRY: PPP基準値")
print("  PPP_changed: PPP基準が前月から変更されたか")
print("  d_USDJPY, d_USDTRY: PPP乖離率")
print("  m_USD, m_JPY, m_TRY: MCI座標")
print("  D_mTRY: m[TRY]の月次変動")
print("  pct_TRYJPY: TRY/JPY価格の月次変動率（%）")
