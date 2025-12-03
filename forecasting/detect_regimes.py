#!/usr/bin/env python3
"""
レジュームチェンジ検出モジュール

統計的手法と外部カタログを使ってレジュームチェンジを検出する
"""

import csv
from typing import Dict, List, Optional
import math


class RegimeDetector:
    """レジュームチェンジを検出するクラス"""

    def __init__(self, catalog_path: str = 'regime_catalog.csv'):
        """
        Args:
            catalog_path: レジュームカタログCSVのパス
        """
        self.regime_catalog = self._load_regime_catalog(catalog_path)

    def _load_regime_catalog(self, path: str) -> Dict[str, Dict]:
        """レジュームカタログを読み込む"""
        catalog = {}
        try:
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    catalog[row['date']] = {
                        'regime_type': row['regime_type'],
                        'description': row['description'],
                        'severity': row['severity'],
                        'notes': row['notes']
                    }
        except FileNotFoundError:
            print(f"Warning: Regime catalog not found at {path}")

        return catalog

    def get_regime_state(self, month: str) -> Optional[Dict]:
        """
        指定月のレジューム状態を取得

        Args:
            month: 対象月 (YYYY-MM形式)

        Returns:
            レジューム情報、または None（通常時）
        """
        return self.regime_catalog.get(month)

    def is_regime_period(self, month: str) -> bool:
        """指定月がレジュームチェンジ期間かどうか"""
        return month in self.regime_catalog

    def detect_volatility_spike(self, data: List[Dict], current_idx: int,
                               threshold_sigma: float = 2.0) -> bool:
        """
        ボラティリティスパイクを検出

        Args:
            data: 月次データリスト
            current_idx: 現在のインデックス
            threshold_sigma: 閾値（標準偏差の倍数）

        Returns:
            ボラティリティスパイクが検出されたかどうか
        """
        # 最低6カ月のデータが必要（3カ月平均 + 標準偏差計算用）
        if current_idx < 6:
            return False

        # 過去6カ月のデルタm変動を取得
        lookback = 6
        deltas_usd = []
        deltas_jpy = []
        deltas_try = []

        for i in range(current_idx - lookback, current_idx):
            if 'delta_m_USD' in data[i] and data[i]['delta_m_USD']:
                try:
                    deltas_usd.append(float(data[i]['delta_m_USD']))
                    deltas_jpy.append(float(data[i]['delta_m_JPY']))
                    deltas_try.append(float(data[i]['delta_m_TRY']))
                except (ValueError, TypeError):
                    continue

        if len(deltas_usd) < 3:
            return False

        # 標準偏差を計算
        std_usd = self._calculate_std(deltas_usd)
        std_jpy = self._calculate_std(deltas_jpy)
        std_try = self._calculate_std(deltas_try)

        # 平均を計算
        mean_usd = sum(deltas_usd) / len(deltas_usd)
        mean_jpy = sum(deltas_jpy) / len(deltas_jpy)
        mean_try = sum(deltas_try) / len(deltas_try)

        # 現在月の変動を取得
        try:
            current_delta_usd = float(data[current_idx]['delta_m_USD'])
            current_delta_jpy = float(data[current_idx]['delta_m_JPY'])
            current_delta_try = float(data[current_idx]['delta_m_TRY'])
        except (ValueError, TypeError, KeyError):
            return False

        # 閾値を超えているか確認（いずれかの通貨で）
        spike_usd = abs(current_delta_usd - mean_usd) > threshold_sigma * std_usd
        spike_jpy = abs(current_delta_jpy - mean_jpy) > threshold_sigma * std_jpy
        spike_try = abs(current_delta_try - mean_try) > threshold_sigma * std_try

        return spike_usd or spike_jpy or spike_try

    def _calculate_std(self, values: List[float]) -> float:
        """標準偏差を計算"""
        if len(values) < 2:
            return 0.0

        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return math.sqrt(variance)

    def get_regime_severity_factor(self, month: str) -> float:
        """
        レジュームの深刻度に応じた補正係数を返す

        Args:
            month: 対象月

        Returns:
            補正係数（1.0 = 通常、> 1.0 = 不確実性増加）
        """
        regime = self.get_regime_state(month)

        if regime is None:
            return 1.0

        severity_factors = {
            'low': 1.2,
            'medium': 1.5,
            'high': 2.0
        }

        return severity_factors.get(regime['severity'], 1.5)

    def add_external_regime(self, month: str, regime_type: str,
                           description: str, severity: str = 'medium',
                           notes: str = ''):
        """
        外部からレジューム情報を追加

        Args:
            month: 対象月 (YYYY-MM)
            regime_type: レジュームタイプ ('normal', 'transition', 'crisis')
            description: 説明
            severity: 深刻度 ('low', 'medium', 'high')
            notes: 備考
        """
        self.regime_catalog[month] = {
            'regime_type': regime_type,
            'description': description,
            'severity': severity,
            'notes': notes
        }

    def save_regime_catalog(self, path: str):
        """レジュームカタログを保存"""
        with open(path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['date', 'regime_type', 'description', 'severity', 'notes']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for month, info in sorted(self.regime_catalog.items()):
                row = {'date': month}
                row.update(info)
                writer.writerow(row)


def main():
    """テスト用メイン関数"""
    detector = RegimeDetector()

    # カタログ内容を表示
    print("=== Regime Catalog ===")
    for month, info in sorted(detector.regime_catalog.items()):
        print(f"{month}: {info['regime_type']} ({info['severity']}) - {info['description']}")

    # テスト: 外部レジューム追加
    print("\n=== Adding External Regime ===")
    detector.add_external_regime(
        month='2025-12',
        regime_type='transition',
        description='Test external regime addition',
        severity='low',
        notes='Manual test'
    )

    # 確認
    print(f"2025-12 regime: {detector.get_regime_state('2025-12')}")
    print(f"Severity factor: {detector.get_regime_severity_factor('2025-12')}")


if __name__ == '__main__':
    main()
