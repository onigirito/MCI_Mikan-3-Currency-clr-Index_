#!/usr/bin/env python3
"""
MCIを使った年間変動率推測の客観的評価

検証項目:
1. 予測力: 過去の変動統計は将来を予測できるか？
2. 代替手法との比較: 他の方法と比べてどうか？
3. 時間軸の問題: 年次データで短期トレードは可能か？
4. 誤差分析: 実際にどの程度のズレがあるか？
5. 適用条件: どういう状況で有効/無効か？
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
            'S_TRYJPY': float(row['S_TRYJPY']),
            'm_USD': float(row['m_USD']),
            'm_JPY': float(row['m_JPY']),
            'm_TRY': float(row['m_TRY']),
        })

# 年次変動を計算
for i in range(1, len(data)):
    data[i]['D_mTRY'] = data[i]['m_TRY'] - data[i-1]['m_TRY']
    data[i]['D_mUSD'] = data[i]['m_USD'] - data[i-1]['m_USD']
    data[i]['D_mJPY'] = data[i]['m_JPY'] - data[i-1]['m_JPY']
    data[i]['pct_TRYJPY'] = (data[i]['S_TRYJPY'] / data[i-1]['S_TRYJPY'] - 1) * 100

print("=" * 80)
print("MCIを使った年間変動率推測の客観的評価")
print("=" * 80)
print()

# ===== 1. 予測力の検証 =====
print("【検証1】予測力: 過去N年の統計で次の1年を予測できるか？")
print("-" * 80)

# ローリングウィンドウで予測精度を検証
window_sizes = [3, 5, 10]
predictions = {}

for window in window_sizes:
    predictions[window] = []
    for i in range(window + 1, len(data)):
        # 過去window年のm[TRY]変動から統計を取る
        recent_D = [data[j]['D_mTRY'] for j in range(i-window, i) if 'D_mTRY' in data[j]]

        if not recent_D:
            continue

        mean_D = sum(recent_D) / len(recent_D)
        # 標準偏差
        variance = sum((x - mean_D)**2 for x in recent_D) / len(recent_D)
        std_D = math.sqrt(variance)

        # 実際の値
        actual_D = data[i]['D_mTRY'] if 'D_mTRY' in data[i] else None

        if actual_D is not None:
            # 予測区間: mean ± 2*std
            lower_bound = mean_D - 2 * std_D
            upper_bound = mean_D + 2 * std_D

            # 的中判定
            hit = lower_bound <= actual_D <= upper_bound

            predictions[window].append({
                'year': data[i]['year'],
                'predicted_mean': mean_D,
                'predicted_std': std_D,
                'actual': actual_D,
                'hit': hit,
                'lower': lower_bound,
                'upper': upper_bound,
            })

for window in window_sizes:
    preds = predictions[window]
    if preds:
        hit_rate = sum(1 for p in preds if p['hit']) / len(preds) * 100
        print(f"\n過去{window}年平均で予測:")
        print(f"  的中率（±2σ区間）: {hit_rate:.1f}% ({sum(1 for p in preds if p['hit'])}/{len(preds)})")

        # 外れた年を表示
        misses = [p for p in preds if not p['hit']]
        if misses:
            print(f"  外れた年: {', '.join(str(m['year']) for m in misses)}")
            for m in misses:
                print(f"    {m['year']}: 予測[{m['lower']:.3f}, {m['upper']:.3f}], 実際={m['actual']:.3f}")

print()
print("→ 評価: 理論的には95%の的中率（2σ）だが、実際には" )
print("  サンプル数が少ない（20年）ため、統計的予測力は限定的")
print()

# ===== 2. 代替手法との比較 =====
print("【検証2】代替手法との比較")
print("-" * 80)

# 手法A: 単純な価格変動率の標準偏差
price_changes = [d['pct_TRYJPY'] for d in data[1:] if 'pct_TRYJPY' in d]
price_mean = sum(price_changes) / len(price_changes)
price_variance = sum((x - price_mean)**2 for x in price_changes) / len(price_changes)
price_std = math.sqrt(price_variance)

print("手法A: 単純な価格変動率の統計")
print(f"  TRY/JPY年間変動率: 平均={price_mean:.2f}%, 標準偏差={price_std:.2f}%")
print(f"  予測区間（±2σ）: {price_mean - 2*price_std:.2f}% ~ {price_mean + 2*price_std:.2f}%")
print()

# 手法B: MCIのm[TRY]変動統計
D_TRY_values = [d['D_mTRY'] for d in data[1:] if 'D_mTRY' in d]
D_TRY_mean = sum(D_TRY_values) / len(D_TRY_values)
D_TRY_variance = sum((x - D_TRY_mean)**2 for x in D_TRY_values) / len(D_TRY_values)
D_TRY_std = math.sqrt(D_TRY_variance)

print("手法B: MCI m[TRY]変動の統計")
print(f"  m[TRY]年間変動: 平均={D_TRY_mean:.6f}, 標準偏差={D_TRY_std:.6f}")
print(f"  予測区間（±2σ）: {D_TRY_mean - 2*D_TRY_std:.6f} ~ {D_TRY_mean + 2*D_TRY_std:.6f}")
print()

# 比較: どちらがバラツキが小さいか？
# 正規化して比較（変動係数 = std/mean）
cv_price = abs(price_std / price_mean) if price_mean != 0 else float('inf')
cv_mci = abs(D_TRY_std / D_TRY_mean) if D_TRY_mean != 0 else float('inf')

print("変動係数（CV = std/|mean|）で比較:")
print(f"  手法A（価格）: CV = {cv_price:.2f}")
print(f"  手法B（MCI）: CV = {cv_mci:.2f}")
print()

if cv_mci < cv_price:
    print("→ MCIの方が相対的にバラツキが小さい（安定的）")
else:
    print("→ 単純な価格統計の方が相対的にバラツキが小さい")
print()

# ===== 3. m[TRY]と価格の相関 =====
print("【検証3】m[TRY]変動と実際の価格変動の関係")
print("-" * 80)

# 相関係数を計算
paired_data = [(d['D_mTRY'], d['pct_TRYJPY']) for d in data[1:] if 'D_mTRY' in d and 'pct_TRYJPY' in d]

if len(paired_data) > 1:
    D_values = [p[0] for p in paired_data]
    pct_values = [p[1] for p in paired_data]

    mean_D = sum(D_values) / len(D_values)
    mean_pct = sum(pct_values) / len(pct_values)

    covariance = sum((D_values[i] - mean_D) * (pct_values[i] - mean_pct) for i in range(len(D_values))) / len(D_values)

    std_D = math.sqrt(sum((x - mean_D)**2 for x in D_values) / len(D_values))
    std_pct = math.sqrt(sum((x - mean_pct)**2 for x in pct_values) / len(pct_values))

    correlation = covariance / (std_D * std_pct) if (std_D * std_pct) != 0 else 0

    print(f"相関係数: r = {correlation:.3f}")
    print()

    if correlation > 0.7:
        print("→ 強い正の相関あり（MCIは価格変動をよく反映）")
    elif correlation > 0.4:
        print("→ 中程度の正の相関あり（ある程度反映）")
    else:
        print("→ 相関は弱い（MCIと価格は別の情報を持つ）")
    print()

# ===== 4. ユーザーの手法の検証 =====
print("【検証4】ユーザーの深度分類手法の妥当性")
print("-" * 80)

# 深度1ラインを超えた年はあるか？
depth1_violations = [(d['year'], d['D_mTRY']) for d in data[1:] if 'D_mTRY' in d and d['D_mTRY'] < -0.06]
depth3_violations = [(d['year'], d['D_mTRY']) for d in data[1:] if 'D_mTRY' in d and d['D_mTRY'] < -0.08]

print(f"深度1超過（-0.06以下）: {len(depth1_violations)}回")
for year, val in depth1_violations:
    print(f"  {year}: {val:.6f}")
print()

# 深度1を超えた時の実際の価格下落
if depth1_violations:
    print("深度1超過時の実際の価格変動:")
    for year, _ in depth1_violations:
        d = [x for x in data if x['year'] == year][0]
        if 'pct_TRYJPY' in d:
            print(f"  {year}: TRY/JPY {d['pct_TRYJPY']:+.2f}%")
print()

# ===== 5. 時間軸の問題 =====
print("【検証5】時間軸の問題: 年次データで日次トレードは可能か？")
print("-" * 80)
print("制約事項:")
print("  1. データは年次 → 年内の変動は捉えられない")
print("  2. PPPは構造的指標 → 短期の投機的変動とは別")
print("  3. 深度1 = 年間-0.06変動 → 日次では±数%の乱高下がありうる")
print()
print("例: 2018年トルコショック")
depth3_2018 = [d for d in data if d['year'] == 2018][0]
if 'pct_TRYJPY' in depth3_2018:
    print(f"  年間変動: m[TRY] = {depth3_2018['D_mTRY']:.3f}")
    print(f"  価格変動: TRY/JPY {depth3_2018['pct_TRYJPY']:+.2f}%")
    print("  → 実際には8月に一時的に-40%以上の暴落があった")
    print("  → 年次データではその瞬間的なリスクは捉えられない")
print()

# ===== 総合評価 =====
print("=" * 80)
print("【総合評価】MCIを使った年間変動率推測の有効性")
print("=" * 80)
print()

print("✅ 強み（有効な点）:")
print()
print("  1. 構造的な変動限界の推定")
print("     - 3通貨のゼロサム制約により、単独では見えない力学を可視化")
print("     - 過去の最悪ケース（リーマン: -0.114）から限界を推測可能")
print()
print("  2. 多通貨間の配分推測")
print("     - TRY下落時のUSD/JPY配分を逆算できる")
print("     - 単純な二国間分析では不可能")
print()
print("  3. バリュエーション指標としての有用性")
print("     - PPP乖離という「理論値からのズレ」を測定")
print("     - 価格モメンタムとは異なる情報を提供")
print()

print("⚠️ 弱み（限界）:")
print()
print("  1. サンプルサイズの制約")
print("     - 20年間のデータのみ → 統計的予測力は限定的")
print("     - 未経験の極端事象には対応不可")
print()
print("  2. 時間軸のミスマッチ")
print("     - 年次データ ↔ 日次トレードのギャップ")
print("     - 年内の短期的な暴落は捉えられない")
print()
print("  3. PPPの限界")
print("     - PPP自体が長期均衡概念（短期では大きく乖離しうる）")
print("     - 政治リスク、資本規制などは反映されない")
print()

print("📊 結論:")
print()
print("  MCIを使った年間変動率推測は:")
print()
print("  【中長期的な構造分析】として → 有効 ★★★★☆")
print("    - 「現在の通貨ポジションが構造的にどの位置か」の判断材料")
print("    - 「過去の危機レベルと比較してどの程度のリスクか」の把握")
print()
print("  【短期トレードのストップライン】として → 条件付きで有効 ★★☆☆☆")
print("    - 日次の価格ボラティリティとの関係を別途検証が必要")
print("    - 年次統計だけでは短期の暴落リスクを過小評価する可能性")
print("    - ボラティリティ分析、テクニカル分析との併用が推奨")
print()
print("  【最も有効な使い方】:")
print("    - 長期保有のポジションサイジング")
print("    - キャリートレードの構造的リスク評価")
print("    - 複数通貨ポートフォリオの配分最適化")
print()

print("=" * 80)
print("推奨: MCIを「唯一の」指標とせず、")
print("      価格ボラティリティ、テクニカル指標、ファンダメンタルズと")
print("      組み合わせた「多層的なリスク管理」を構築すべき")
print("=" * 80)
