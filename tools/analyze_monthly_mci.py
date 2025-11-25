#!/usr/bin/env python3
"""
月次MCIデータの分析
"""

import csv
import math

# データ読み込み
data = []
with open('dataset/mci_monthly_recent.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append({
            'date': row['date'],
            'm_TRY': float(row['m_TRY']),
            'S_TRYJPY': float(row['S_TRYJPY']),
            'PPP_TRY': float(row['PPP_TRY']),
        })

# 月次変動を計算
for i in range(1, len(data)):
    data[i]['D_mTRY'] = data[i]['m_TRY'] - data[i-1]['m_TRY']
    data[i]['pct_TRYJPY'] = (data[i]['S_TRYJPY'] / data[i-1]['S_TRYJPY'] - 1) * 100
    data[i]['PPP_changed'] = data[i]['PPP_TRY'] != data[i-1]['PPP_TRY']

print("=" * 80)
print("月次MCI分析：構造的ジャンプの検出")
print("=" * 80)
print()

# PPP切り替え時のジャンプ
print("【重要】PPP基準切り替え時の構造的ジャンプ:")
print("-" * 80)
ppp_changes = [d for d in data[1:] if d.get('PPP_changed', False)]

for d in ppp_changes:
    idx = data.index(d)
    prev = data[idx-1]
    print(f"\n{d['date']}:")
    print(f"  PPP切り替え: {prev['PPP_TRY']:.2f} → {d['PPP_TRY']:.2f}")
    print(f"  m[TRY]変動: {d['D_mTRY']:+.6f}")
    print(f"  実際の価格変動: {d['pct_TRYJPY']:+.2f}%")
    print(f"  → これは実価格の変動ではなく、測定基準の変更による構造的ジャンプ")

print()
print()

# PPP切り替え以外の大きな変動
print("【実際の市場変動】PPP切り替え以外の大きな変動:")
print("-" * 80)

threshold = 0.05  # 月次で5%以上の変動
large_moves = [d for d in data[1:] if 'D_mTRY' in d and not d.get('PPP_changed', False) and abs(d['D_mTRY']) > threshold]

if large_moves:
    for d in large_moves:
        print(f"\n{d['date']}:")
        print(f"  m[TRY]変動: {d['D_mTRY']:+.6f}")
        print(f"  価格変動: {d['pct_TRYJPY']:+.2f}%")
        print(f"  TRY/JPY: {d['S_TRYJPY']:.4f}")
else:
    print("  月次5%超過の変動なし（正常域）")

print()
print()

# 2024年後半〜2025年の推移
print("【直近の動き】2024年後半〜2025年:")
print("-" * 80)

recent = [d for d in data if d['date'] >= '2024-06']
print(f"\n{'日付':<10} {'m[TRY]':<12} {'月次変動':<12} {'TRY/JPY':<10}")
print("-" * 50)

for d in recent:
    if 'D_mTRY' in d:
        print(f"{d['date']:<10} {d['m_TRY']:>10.6f} {d['D_mTRY']:>+10.6f} {d['S_TRYJPY']:>9.4f}")
    else:
        print(f"{d['date']:<10} {d['m_TRY']:>10.6f} {'---':>10} {d['S_TRYJPY']:>9.4f}")

print()
print()

# 現在位置の評価
current = data[-1]
print("【現在位置の評価】2025年1月:")
print("-" * 80)
print(f"  m[TRY] = {current['m_TRY']:.6f}")
print(f"  TRY/JPY = {current['S_TRYJPY']:.4f}")
print()

# 2024年末からの変動（PPP基準変更を考慮）
dec_2024 = [d for d in data if d['date'] == '2024-12'][0]
print(f"2024年12月比（同一PPP基準内）:")
print(f"  Δm[TRY] = {current['m_TRY'] - dec_2024['m_TRY']:+.6f}")
print(f"  価格変動: {(current['S_TRYJPY'] / dec_2024['S_TRYJPY'] - 1) * 100:+.2f}%")
print()

# ユーザーのストップライン
stopline = 3.35
distance = current['S_TRYJPY'] - stopline
pct_to_stop = (distance / current['S_TRYJPY']) * 100

print(f"ストップライン (3.35🌰) までの距離:")
print(f"  現在価格: {current['S_TRYJPY']:.4f}")
print(f"  ストップ: {stopline:.2f}")
print(f"  マージン: {distance:.4f} ({pct_to_stop:.2f}%)")

if distance > 0:
    print(f"  → まだ余裕あり")
else:
    print(f"  → ⚠️ ストップライン到達！")

print()
print("=" * 80)

# 統計サマリー
print("月次変動統計（PPP切り替え除外）:")
print("-" * 80)

regular_moves = [d['D_mTRY'] for d in data[1:] if 'D_mTRY' in d and not d.get('PPP_changed', False)]
if regular_moves:
    mean = sum(regular_moves) / len(regular_moves)
    variance = sum((x - mean)**2 for x in regular_moves) / len(regular_moves)
    std = math.sqrt(variance)

    print(f"  平均: {mean:.6f}")
    print(f"  標準偏差: {std:.6f}")
    print(f"  最小値: {min(regular_moves):.6f}")
    print(f"  最大値: {max(regular_moves):.6f}")
    print()
    print(f"  深度1相当（-0.06）: 月次では{-0.06 / std:.2f}σ")
    print(f"  深度3相当（-0.114）: 月次では{-0.114 / std:.2f}σ")

print()
print("=" * 80)
