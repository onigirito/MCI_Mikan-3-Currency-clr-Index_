#!/usr/bin/env python3
"""
MCI適応的先行予想エンジン

バックテストの3カ月平均理論をベースに、レジュームチェンジでの誤差を修正する
外圧調整を後付けで設定可能な予想システム
"""

import argparse
import csv
import math
import sys
from typing import Dict, List, Optional, Tuple

# 同一ディレクトリのモジュールをインポート
from detect_regimes import RegimeDetector
from error_correction import ErrorCorrector


class AdaptiveForecastEngine:
    """適応的予想エンジン"""

    def __init__(self, data_path: str = '../dataset/monthly_mci_backtest_ready_2022_2025.csv',
                 regime_catalog_path: str = 'regime_catalog.csv'):
        """
        Args:
            data_path: 月次MCIデータのパス
            regime_catalog_path: レジュームカタログのパス
        """
        self.data = self._load_data(data_path)
        self.regime_detector = RegimeDetector(regime_catalog_path)
        self.error_corrector = ErrorCorrector()

        # バックテスト統計（通常期間のベースライン誤差）
        self.baseline_errors = {
            'USDJPY': 1.51,  # 通常期間のMAE%
            'USDTRY': 2.22,
            'TRYJPY': 2.95
        }

    def _load_data(self, path: str) -> List[Dict]:
        """月次データを読み込む"""
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def get_month_data(self, month: str) -> Optional[Dict]:
        """指定月のデータを取得"""
        for row in self.data:
            if row['date'] == month:
                return {
                    'date': row['date'],
                    'm_USD': float(row['m_USD']),
                    'm_JPY': float(row['m_JPY']),
                    'm_TRY': float(row['m_TRY']),
                    'avg_delta_m_USD_3m': float(row['avg_delta_m_USD_3m']) if row['avg_delta_m_USD_3m'] else None,
                    'avg_delta_m_JPY_3m': float(row['avg_delta_m_JPY_3m']) if row['avg_delta_m_JPY_3m'] else None,
                    'avg_delta_m_TRY_3m': float(row['avg_delta_m_TRY_3m']) if row['avg_delta_m_TRY_3m'] else None,
                    'S_USDJPY': float(row['S_USDJPY']),
                    'S_USDTRY': float(row['S_USDTRY']),
                    'S_TRYJPY': float(row['S_TRYJPY']),
                    'PPP_JPY': float(row['PPP_JPY']),
                    'PPP_TRY': float(row['PPP_TRY'])
                }
        return None

    def forecast_next_month(self, base_month: str, target_ppp: Optional[Dict] = None,
                           use_regime_detection: bool = True,
                           use_error_correction: bool = True) -> Dict:
        """
        翌月の為替レートを予想

        Args:
            base_month: 基準月 (YYYY-MM)
            target_ppp: 予想対象月のPPP値（Noneの場合は基準月のPPPを使用）
            use_regime_detection: レジューム検出を使用するか
            use_error_correction: 誤差修正を使用するか

        Returns:
            予想結果の辞書
        """
        # 基準月のデータを取得
        base_data = self.get_month_data(base_month)
        if base_data is None:
            return {'error': f'Base month {base_month} not found'}

        # 3カ月平均がない場合はエラー
        if base_data['avg_delta_m_USD_3m'] is None:
            return {'error': f'No 3-month average data for {base_month}'}

        # 予想対象月を計算
        target_month = self._get_next_month(base_month)

        # ターゲットPPPが指定されていない場合は基準月のPPPを使用
        if target_ppp is None:
            target_ppp = {
                'PPP_JPY': base_data['PPP_JPY'],
                'PPP_TRY': base_data['PPP_TRY']
            }

        # レジューム状態を検出
        regime_info = None
        regime_factor = 1.0

        if use_regime_detection:
            regime_info = self.regime_detector.get_regime_state(target_month)
            regime_factor = self.regime_detector.get_regime_severity_factor(target_month)

        # 3カ月平均のΔm座標を取得
        avg_delta_usd = base_data['avg_delta_m_USD_3m']
        avg_delta_jpy = base_data['avg_delta_m_JPY_3m']
        avg_delta_try = base_data['avg_delta_m_TRY_3m']

        # 誤差修正を適用
        if use_error_correction:
            avg_delta_usd, avg_delta_jpy, avg_delta_try = \
                self.error_corrector.apply_delta_m_correction(
                    target_month, avg_delta_usd, avg_delta_jpy, avg_delta_try,
                    regime_factor
                )

        # 予想月のm座標を計算
        pred_m_usd = base_data['m_USD'] + avg_delta_usd
        pred_m_jpy = base_data['m_JPY'] + avg_delta_jpy
        pred_m_try = base_data['m_TRY'] + avg_delta_try

        # 予想レートを計算
        pred_usdjpy = target_ppp['PPP_JPY'] * math.exp(pred_m_usd - pred_m_jpy)
        pred_usdtry = target_ppp['PPP_TRY'] * math.exp(pred_m_usd - pred_m_try)
        pred_tryjpy = pred_usdjpy / pred_usdtry

        # レート修正を適用
        if use_error_correction:
            pred_usdjpy, pred_usdtry, pred_tryjpy = \
                self.error_corrector.apply_rate_correction(
                    target_month, pred_usdjpy, pred_usdtry, pred_tryjpy
                )

        # 信頼区間を計算
        ci_usdjpy = self.error_corrector.calculate_confidence_interval(
            self.baseline_errors['USDJPY'], regime_factor
        )
        ci_usdtry = self.error_corrector.calculate_confidence_interval(
            self.baseline_errors['USDTRY'], regime_factor
        )
        ci_tryjpy = self.error_corrector.calculate_confidence_interval(
            self.baseline_errors['TRYJPY'], regime_factor
        )

        # 推奨アクションを取得
        recommendation = self.error_corrector.get_recommendation(
            regime_factor, regime_info
        )

        return {
            'base_month': base_month,
            'target_month': target_month,
            'pred_USDJPY': pred_usdjpy,
            'pred_USDTRY': pred_usdtry,
            'pred_TRYJPY': pred_tryjpy,
            'pred_m_USD': pred_m_usd,
            'pred_m_JPY': pred_m_jpy,
            'pred_m_TRY': pred_m_try,
            'regime_info': regime_info,
            'regime_factor': regime_factor,
            'confidence_interval': {
                'USDJPY': ci_usdjpy,
                'USDTRY': ci_usdtry,
                'TRYJPY': ci_tryjpy
            },
            'recommendation': recommendation,
            'corrected_delta_m': {
                'USD': avg_delta_usd,
                'JPY': avg_delta_jpy,
                'TRY': avg_delta_try
            }
        }

    def _get_next_month(self, year_month: str) -> str:
        """次月を計算"""
        year, month = map(int, year_month.split('-'))
        if month == 12:
            return f"{year+1}-01"
        else:
            return f"{year}-{month+1:02d}"

    def run_adaptive_backtest(self, output_file: str = 'adaptive_backtest_results.csv',
                             use_regime_detection: bool = True,
                             use_error_correction: bool = True):
        """
        適応的バックテストを実行

        Args:
            output_file: 出力ファイル名
            use_regime_detection: レジューム検出を使用
            use_error_correction: 誤差修正を使用
        """
        results = []

        for i, row in enumerate(self.data):
            base_month = row['date']

            # 最終月はスキップ
            if i == len(self.data) - 1:
                continue

            target_month = self._get_next_month(base_month)

            # 予想を実行
            forecast = self.forecast_next_month(
                base_month,
                use_regime_detection=use_regime_detection,
                use_error_correction=use_error_correction
            )

            if 'error' in forecast:
                print(f"Skipped {base_month}: {forecast['error']}")
                continue

            # 実績データを取得
            actual_data = self.get_month_data(target_month)
            if actual_data is None:
                continue

            # 誤差を計算
            error_usdjpy = ((forecast['pred_USDJPY'] - actual_data['S_USDJPY']) /
                           actual_data['S_USDJPY']) * 100
            error_usdtry = ((forecast['pred_USDTRY'] - actual_data['S_USDTRY']) /
                           actual_data['S_USDTRY']) * 100
            error_tryjpy = ((forecast['pred_TRYJPY'] - actual_data['S_TRYJPY']) /
                           actual_data['S_TRYJPY']) * 100

            result = {
                'base_month': base_month,
                'target_month': target_month,
                'pred_USDJPY': forecast['pred_USDJPY'],
                'actual_USDJPY': actual_data['S_USDJPY'],
                'error_pct_USDJPY': error_usdjpy,
                'pred_USDTRY': forecast['pred_USDTRY'],
                'actual_USDTRY': actual_data['S_USDTRY'],
                'error_pct_USDTRY': error_usdtry,
                'pred_TRYJPY': forecast['pred_TRYJPY'],
                'actual_TRYJPY': actual_data['S_TRYJPY'],
                'error_pct_TRYJPY': error_tryjpy,
                'regime_factor': forecast['regime_factor'],
                'is_regime_period': 'Yes' if forecast['regime_info'] else 'No',
                'regime_description': forecast['regime_info']['description'] if forecast['regime_info'] else '',
                'recommendation': forecast['recommendation']
            }

            results.append(result)

            # 結果を表示
            regime_mark = " [REGIME]" if forecast['regime_info'] else ""
            print(f"{base_month} → {target_month}{regime_mark}")
            print(f"  USDJPY: {result['pred_USDJPY']:.2f} vs {result['actual_USDJPY']:.2f} "
                  f"(error: {error_usdjpy:+.2f}%)")
            print(f"  Factor: {forecast['regime_factor']:.1f} | {forecast['recommendation']}")

        # 結果をCSVに保存
        if results:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)

            print(f"\n[OK] Results saved to {output_file}")

            # 統計サマリーを計算
            self._print_summary(results)

    def _print_summary(self, results: List[Dict]):
        """バックテスト結果のサマリーを表示"""
        print("\n=== BACKTEST SUMMARY ===")

        # 全期間
        all_errors_usdjpy = [abs(r['error_pct_USDJPY']) for r in results]
        all_errors_usdtry = [abs(r['error_pct_USDTRY']) for r in results]
        all_errors_tryjpy = [abs(r['error_pct_TRYJPY']) for r in results]

        print(f"\nFull Period ({len(results)} predictions):")
        print(f"  USDJPY MAE: {sum(all_errors_usdjpy)/len(all_errors_usdjpy):.2f}%")
        print(f"  USDTRY MAE: {sum(all_errors_usdtry)/len(all_errors_usdtry):.2f}%")
        print(f"  TRYJPY MAE: {sum(all_errors_tryjpy)/len(all_errors_tryjpy):.2f}%")

        # レジューム期間のみ
        regime_results = [r for r in results if r['is_regime_period'] == 'Yes']
        if regime_results:
            regime_errors_usdjpy = [abs(r['error_pct_USDJPY']) for r in regime_results]
            regime_errors_usdtry = [abs(r['error_pct_USDTRY']) for r in regime_results]
            regime_errors_tryjpy = [abs(r['error_pct_TRYJPY']) for r in regime_results]

            print(f"\nRegime Periods Only ({len(regime_results)} predictions):")
            print(f"  USDJPY MAE: {sum(regime_errors_usdjpy)/len(regime_errors_usdjpy):.2f}%")
            print(f"  USDTRY MAE: {sum(regime_errors_usdtry)/len(regime_errors_usdtry):.2f}%")
            print(f"  TRYJPY MAE: {sum(regime_errors_tryjpy)/len(regime_errors_tryjpy):.2f}%")

        # 通常期間のみ
        normal_results = [r for r in results if r['is_regime_period'] == 'No']
        if normal_results:
            normal_errors_usdjpy = [abs(r['error_pct_USDJPY']) for r in normal_results]
            normal_errors_usdtry = [abs(r['error_pct_USDTRY']) for r in normal_results]
            normal_errors_tryjpy = [abs(r['error_pct_TRYJPY']) for r in normal_results]

            print(f"\nNormal Periods Only ({len(normal_results)} predictions):")
            print(f"  USDJPY MAE: {sum(normal_errors_usdjpy)/len(normal_errors_usdjpy):.2f}%")
            print(f"  USDTRY MAE: {sum(normal_errors_usdtry)/len(normal_errors_usdtry):.2f}%")
            print(f"  TRYJPY MAE: {sum(normal_errors_tryjpy)/len(normal_errors_tryjpy):.2f}%")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description='MCI適応的先行予想エンジン'
    )
    parser.add_argument('--base-month', type=str,
                       help='基準月 (YYYY-MM) - 単一予想モード')
    parser.add_argument('--backtest', action='store_true',
                       help='適応的バックテストを実行')
    parser.add_argument('--output', type=str,
                       default='adaptive_backtest_results.csv',
                       help='出力ファイル名')
    parser.add_argument('--no-regime-detection', action='store_true',
                       help='レジューム検出を無効化')
    parser.add_argument('--no-error-correction', action='store_true',
                       help='誤差修正を無効化')

    args = parser.parse_args()

    # エンジンを初期化
    engine = AdaptiveForecastEngine()

    if args.backtest:
        # バックテストモード
        print("Running adaptive backtest...")
        engine.run_adaptive_backtest(
            output_file=args.output,
            use_regime_detection=not args.no_regime_detection,
            use_error_correction=not args.no_error_correction
        )

    elif args.base_month:
        # 単一予想モード
        forecast = engine.forecast_next_month(
            args.base_month,
            use_regime_detection=not args.no_regime_detection,
            use_error_correction=not args.no_error_correction
        )

        if 'error' in forecast:
            print(f"Error: {forecast['error']}")
            return

        print(f"\n=== FORECAST: {forecast['base_month']} → {forecast['target_month']} ===\n")

        # レジューム情報
        if forecast['regime_info']:
            print(f"[REGIME DETECTED]")
            print(f"  Type: {forecast['regime_info']['regime_type']}")
            print(f"  Severity: {forecast['regime_info']['severity']}")
            print(f"  Description: {forecast['regime_info']['description']}\n")

        # 予想値
        print(f"Predicted Exchange Rates:")
        print(f"  USD/JPY: {forecast['pred_USDJPY']:.2f}")
        print(f"  USD/TRY: {forecast['pred_USDTRY']:.2f}")
        print(f"  TRY/JPY: {forecast['pred_TRYJPY']:.3f}\n")

        # 信頼区間
        print(f"Confidence Intervals (±%):")
        ci = forecast['confidence_interval']
        print(f"  USD/JPY: {ci['USDJPY'][0]:.2f}% to {ci['USDJPY'][1]:.2f}%")
        print(f"  USD/TRY: {ci['USDTRY'][0]:.2f}% to {ci['USDTRY'][1]:.2f}%")
        print(f"  TRY/JPY: {ci['TRYJPY'][0]:.2f}% to {ci['TRYJPY'][1]:.2f}%\n")

        # 推奨
        print(f"Recommendation: {forecast['recommendation']}")

    else:
        print("Error: Specify --base-month or --backtest")
        parser.print_help()


if __name__ == '__main__':
    main()
