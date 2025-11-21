#!/usr/bin/env python3
"""
2025年PPP推定ツール

トルコのインフレ予測に基づいて2025年のPPP_TRYを推定する。
"""

import math

# 2024年確定値
PPP_JPY_2024 = 93.20
PPP_TRY_2024 = 12.55

print("=" * 80)
print("2025年PPP推定")
print("=" * 80)
print()

print("2024年確定値:")
print(f"  PPP_JPY = {PPP_JPY_2024:.2f}")
print(f"  PPP_TRY = {PPP_TRY_2024:.2f}")
print()

# 円のPPP推定
print("【JPY】2025年推定:")
print("  過去3年の推移: 92.50 → 92.84 → 93.20")
print("  年次変化率: 約0.4%増")
print()

# シナリオ
jpy_scenarios = [
    ("据え置き", 93.20),
    ("微増（+0.4%）", 93.20 * 1.004),
]

for name, value in jpy_scenarios:
    print(f"  {name}: {value:.2f}")
print()
print("  → 推奨: 93.20（据え置き、保守的）")
print()

PPP_JPY_2025 = 93.20

# リラのPPP推定
print("【TRY】2025年推定:")
print("  インフレ予測:")
print("    - BBVAリサーチ: 30%")
print("    - IMF: 34.9%")
print("    - 中央値: 32.45%")
print()

# インフレシナリオ
try_scenarios = [
    ("保守的（30%）", 12.55 * 1.30),
    ("中間（32.5%）", 12.55 * 1.325),
    ("楽観的（35%）", 12.55 * 1.35),
    ("IMF予測（34.9%）", 12.55 * 1.349),
]

for name, value in try_scenarios:
    print(f"  {name}: {value:.2f}")
print()
print("  → 推奨: 16.63（中間32.5%、バランス型）")
print()

PPP_TRY_2025_conservative = 12.55 * 1.30
PPP_TRY_2025_balanced = 12.55 * 1.325
PPP_TRY_2025_optimistic = 12.55 * 1.35

print("=" * 80)
print("3シナリオでのMCI計算")
print("=" * 80)
print()

# 現在のレートと予測レート
current_rates = {
    'USD/JPY': 157.0,
    'USD/TRY': 42.3,
}

forecast_rates = {
    'USD/JPY': 157.0,  # 円は横ばい想定
    'USD/TRY': 45.0,   # BBVAリサーチ予測
}

def calculate_mci(s_usdjpy, s_usdtry, ppp_jpy, ppp_try, label):
    d_usdjpy = math.log(s_usdjpy / ppp_jpy)
    d_usdtry = math.log(s_usdtry / ppp_try)

    m_usd = (d_usdjpy + d_usdtry) / 3
    m_jpy = (-2 * d_usdjpy + d_usdtry) / 3
    m_try = (d_usdjpy - 2 * d_usdtry) / 3

    s_tryjpy = s_usdjpy / s_usdtry

    print(f"{label}:")
    print(f"  PPP: JPY={ppp_jpy:.2f}, TRY={ppp_try:.2f}")
    print(f"  レート: USD/JPY={s_usdjpy:.2f}, USD/TRY={s_usdtry:.2f}, TRY/JPY={s_tryjpy:.4f}")
    print(f"  m[USD] = {m_usd:+.6f}")
    print(f"  m[JPY] = {m_jpy:+.6f}")
    print(f"  m[TRY] = {m_try:+.6f}")
    print()

    return m_try

print("【現在値】（2025年1月時点）")
print("-" * 80)
m_try_current_conservative = calculate_mci(
    current_rates['USD/JPY'], current_rates['USD/TRY'],
    PPP_JPY_2025, PPP_TRY_2025_conservative,
    "保守的PPP（30%インフレ）"
)

m_try_current_balanced = calculate_mci(
    current_rates['USD/JPY'], current_rates['USD/TRY'],
    PPP_JPY_2025, PPP_TRY_2025_balanced,
    "中間PPP（32.5%インフレ）"
)

m_try_current_optimistic = calculate_mci(
    current_rates['USD/JPY'], current_rates['USD/TRY'],
    PPP_JPY_2025, PPP_TRY_2025_optimistic,
    "楽観的PPP（35%インフレ）"
)

print()
print("【年末予測】（USD/TRY = 45想定）")
print("-" * 80)
m_try_forecast_balanced = calculate_mci(
    forecast_rates['USD/JPY'], forecast_rates['USD/TRY'],
    PPP_JPY_2025, PPP_TRY_2025_balanced,
    "中間PPP（32.5%インフレ）+ 年末レート予測"
)

print("=" * 80)
print("2024年確定値との比較")
print("=" * 80)
print()

m_try_2024 = -0.4802599978128906

print(f"2024年末: m[TRY] = {m_try_2024:.6f}")
print()
print("2025年現在値（シナリオ別）:")
print(f"  保守的（30%）: m[TRY] = {m_try_current_conservative:.6f}, 変動 = {m_try_current_conservative - m_try_2024:+.6f}")
print(f"  中間（32.5%）: m[TRY] = {m_try_current_balanced:.6f}, 変動 = {m_try_current_balanced - m_try_2024:+.6f}")
print(f"  楽観的（35%）: m[TRY] = {m_try_current_optimistic:.6f}, 変動 = {m_try_current_optimistic - m_try_2024:+.6f}")
print()
print("2025年末予測（中間シナリオ）:")
print(f"  m[TRY] = {m_try_forecast_balanced:.6f}, 変動 = {m_try_forecast_balanced - m_try_2024:+.6f}")
print()

# 深度判定
def depth_classification(delta):
    if delta >= -0.05:
        return "正常域"
    elif delta >= -0.06:
        return "深度1"
    elif delta >= -0.08:
        return "深度2"
    else:
        return "深度3（危機）"

print("深度判定:")
print(f"  保守的: {depth_classification(m_try_current_conservative - m_try_2024)}")
print(f"  中間: {depth_classification(m_try_current_balanced - m_try_2024)}")
print(f"  楽観的: {depth_classification(m_try_current_optimistic - m_try_2024)}")
print(f"  年末予測: {depth_classification(m_try_forecast_balanced - m_try_2024)}")
print()

print("=" * 80)
print("推奨設定")
print("=" * 80)
print()
print("tools/create_monthly_mci.py のPPP_CONFIG更新:")
print()
print("2025: {")
print(f"    'PPP_JPY': {PPP_JPY_2025:.2f},")
print(f"    'PPP_TRY': {PPP_TRY_2025_balanced:.2f},  # 32.5%インフレ想定（バランス型）")
print("}")
print()
print("代替案（保守的）:")
print(f"    'PPP_TRY': {PPP_TRY_2025_conservative:.2f},  # 30%インフレ想定（保守的）")
print()
