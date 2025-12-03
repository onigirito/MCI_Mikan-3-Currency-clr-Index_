#!/usr/bin/env python3
"""
誤差修正モジュール

レジュームチェンジ時の予想誤差を修正するための外圧調整機能を提供
"""

import csv
import math
from typing import Dict, List, Optional, Tuple


class ErrorCorrector:
    """誤差修正を行うクラス"""

    def __init__(self):
        """初期化"""
        self.external_adjustments = {}  # 外部から設定する調整値
        self.correction_history = []     # 修正履歴

    def add_external_adjustment(self, month: str,
                               delta_m_adjustments: Optional[Dict[str, float]] = None,
                               rate_adjustments: Optional[Dict[str, float]] = None,
                               description: str = ''):
        """
        外部調整値を追加（後付け設定可能）

        Args:
            month: 対象月 (YYYY-MM)
            delta_m_adjustments: Δm座標への調整値
                例: {'USD': 0.01, 'JPY': -0.005, 'TRY': -0.005}
            rate_adjustments: レート予想への調整値（%）
                例: {'USDJPY': -2.0, 'USDTRY': 1.5}
            description: 調整の説明
        """
        self.external_adjustments[month] = {
            'delta_m_adjustments': delta_m_adjustments or {},
            'rate_adjustments': rate_adjustments or {},
            'description': description
        }

    def apply_delta_m_correction(self, month: str,
                                 avg_delta_m_USD: float,
                                 avg_delta_m_JPY: float,
                                 avg_delta_m_TRY: float,
                                 regime_factor: float = 1.0) -> Tuple[float, float, float]:
        """
        Δm座標に誤差修正を適用

        Args:
            month: 対象月
            avg_delta_m_USD, JPY, TRY: 3カ月平均のΔm座標
            regime_factor: レジューム深刻度係数

        Returns:
            修正後のΔm座標 (USD, JPY, TRY)
        """
        corrected_usd = avg_delta_m_USD
        corrected_jpy = avg_delta_m_JPY
        corrected_try = avg_delta_m_TRY

        # 外部調整値がある場合は適用
        if month in self.external_adjustments:
            adjustments = self.external_adjustments[month]['delta_m_adjustments']

            if 'USD' in adjustments:
                corrected_usd += adjustments['USD']
            if 'JPY' in adjustments:
                corrected_jpy += adjustments['JPY']
            if 'TRY' in adjustments:
                corrected_try += adjustments['TRY']

        # レジューム期間は変動を減衰させる（保守的予測）
        if regime_factor > 1.0:
            # 高いregime_factorは不確実性を示すため、変動を抑制
            dampening = 1.0 / math.sqrt(regime_factor)
            corrected_usd *= dampening
            corrected_jpy *= dampening
            corrected_try *= dampening

        # ゼロサム制約を保持（修正後も m_USD + m_JPY + m_TRY = 0）
        total = corrected_usd + corrected_jpy + corrected_try
        if abs(total) > 1e-10:
            # 誤差を3通貨で均等に分散
            correction = total / 3.0
            corrected_usd -= correction
            corrected_jpy -= correction
            corrected_try -= correction

        return corrected_usd, corrected_jpy, corrected_try

    def apply_rate_correction(self, month: str,
                             pred_usdjpy: float,
                             pred_usdtry: float,
                             pred_tryjpy: float) -> Tuple[float, float, float]:
        """
        為替レート予想に直接的な修正を適用

        Args:
            month: 対象月
            pred_usdjpy, pred_usdtry, pred_tryjpy: 予想レート

        Returns:
            修正後のレート (USDJPY, USDTRY, TRYJPY)
        """
        corrected_usdjpy = pred_usdjpy
        corrected_usdtry = pred_usdtry
        corrected_tryjpy = pred_tryjpy

        # 外部調整値がある場合は適用（パーセンテージ調整）
        if month in self.external_adjustments:
            adjustments = self.external_adjustments[month]['rate_adjustments']

            if 'USDJPY' in adjustments:
                corrected_usdjpy *= (1.0 + adjustments['USDJPY'] / 100.0)

            if 'USDTRY' in adjustments:
                corrected_usdtry *= (1.0 + adjustments['USDTRY'] / 100.0)

            if 'TRYJPY' in adjustments:
                corrected_tryjpy *= (1.0 + adjustments['TRYJPY'] / 100.0)
            else:
                # TRYJPYに直接調整がない場合はクロスレートで再計算
                corrected_tryjpy = corrected_usdjpy / corrected_usdtry

        return corrected_usdjpy, corrected_usdtry, corrected_tryjpy

    def calculate_confidence_interval(self, base_error_pct: float,
                                      regime_factor: float) -> Tuple[float, float]:
        """
        信頼区間を計算

        Args:
            base_error_pct: ベースとなる誤差率（%）
            regime_factor: レジューム深刻度係数

        Returns:
            (下限誤差%, 上限誤差%)
        """
        # レジューム期間は信頼区間を拡大
        adjusted_error = base_error_pct * regime_factor

        return -adjusted_error, adjusted_error

    def get_recommendation(self, regime_factor: float,
                          regime_info: Optional[Dict] = None) -> str:
        """
        予想に対する推奨アクションを返す

        Args:
            regime_factor: レジューム深刻度係数
            regime_info: レジューム情報

        Returns:
            推奨アクション
        """
        if regime_factor <= 1.0:
            return "NORMAL: 通常の予測精度が期待できます"
        elif regime_factor <= 1.5:
            return "CAUTION: やや不確実性が高まっています"
        elif regime_factor <= 2.0:
            return "WARNING: 予測精度の低下が予想されます"
        else:
            if regime_info:
                return f"HIGH RISK: レジュームチェンジ期間 - {regime_info.get('description', '不明')}"
            return "HIGH RISK: 予測精度が大幅に低下する可能性があります"

    def save_adjustments(self, path: str):
        """外部調整値を保存"""
        with open(path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['month', 'adjustment_type', 'currency_pair',
                         'adjustment_value', 'description']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for month, adj_data in sorted(self.external_adjustments.items()):
                desc = adj_data['description']

                # Δm調整を保存
                for currency, value in adj_data['delta_m_adjustments'].items():
                    writer.writerow({
                        'month': month,
                        'adjustment_type': 'delta_m',
                        'currency_pair': currency,
                        'adjustment_value': value,
                        'description': desc
                    })

                # レート調整を保存
                for pair, value in adj_data['rate_adjustments'].items():
                    writer.writerow({
                        'month': month,
                        'adjustment_type': 'rate_pct',
                        'currency_pair': pair,
                        'adjustment_value': value,
                        'description': desc
                    })

    def load_adjustments(self, path: str):
        """外部調整値を読み込み"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    month = row['month']
                    if month not in self.external_adjustments:
                        self.external_adjustments[month] = {
                            'delta_m_adjustments': {},
                            'rate_adjustments': {},
                            'description': row['description']
                        }

                    adj_type = row['adjustment_type']
                    currency = row['currency_pair']
                    value = float(row['adjustment_value'])

                    if adj_type == 'delta_m':
                        self.external_adjustments[month]['delta_m_adjustments'][currency] = value
                    elif adj_type == 'rate_pct':
                        self.external_adjustments[month]['rate_adjustments'][currency] = value

        except FileNotFoundError:
            print(f"Warning: Adjustment file not found at {path}")


def main():
    """テスト用メイン関数"""
    corrector = ErrorCorrector()

    # テスト: 外部調整追加
    print("=== Adding External Adjustments ===")
    corrector.add_external_adjustment(
        month='2023-07',
        delta_m_adjustments={'USD': 0.01, 'JPY': -0.005, 'TRY': -0.005},
        description='Turkish crisis correction'
    )

    corrector.add_external_adjustment(
        month='2024-08',
        rate_adjustments={'USDJPY': -3.0},  # 3%下方修正
        description='JPY interest rate regime change'
    )

    # テスト: Δm修正
    print("\n=== Delta-m Correction Test ===")
    corrected = corrector.apply_delta_m_correction(
        month='2023-07',
        avg_delta_m_USD=0.025,
        avg_delta_m_JPY=0.027,
        avg_delta_m_TRY=-0.052,
        regime_factor=2.0
    )
    print(f"Original: USD=0.025, JPY=0.027, TRY=-0.052")
    print(f"Corrected: USD={corrected[0]:.6f}, JPY={corrected[1]:.6f}, TRY={corrected[2]:.6f}")
    print(f"Zero-sum check: {sum(corrected):.10f}")

    # テスト: レート修正
    print("\n=== Rate Correction Test ===")
    corrected_rates = corrector.apply_rate_correction(
        month='2024-08',
        pred_usdjpy=146.5,
        pred_usdtry=33.5,
        pred_tryjpy=4.37
    )
    print(f"Original: USDJPY=146.5, USDTRY=33.5, TRYJPY=4.37")
    print(f"Corrected: USDJPY={corrected_rates[0]:.2f}, "
          f"USDTRY={corrected_rates[1]:.2f}, TRYJPY={corrected_rates[2]:.3f}")

    # 推奨アクション
    print("\n=== Recommendation Test ===")
    for factor in [1.0, 1.3, 1.8, 2.5]:
        print(f"Factor {factor}: {corrector.get_recommendation(factor)}")


if __name__ == '__main__':
    main()
