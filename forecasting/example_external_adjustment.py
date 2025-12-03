#!/usr/bin/env python3
"""
外部調整機能の使用例

このスクリプトは、外部調整値を後付けで設定して予想精度を改善する方法を示します。
"""

from adaptive_forecast import AdaptiveForecastEngine


def example_delta_m_adjustment():
    """
    例1: Δm座標への調整
    2023年7月のトルコショック期間の予想を手動で調整
    """
    print("=" * 60)
    print("例1: Δm座標への調整")
    print("=" * 60)

    engine = AdaptiveForecastEngine()

    # まず調整なしで予想
    print("\n--- 調整なしの予想 ---")
    forecast_no_adj = engine.forecast_next_month('2023-06')
    actual_data = engine.get_month_data('2023-07')

    print(f"予想: USD/JPY = {forecast_no_adj['pred_USDJPY']:.2f}")
    print(f"実績: USD/JPY = {actual_data['S_USDJPY']:.2f}")
    error_no_adj = ((forecast_no_adj['pred_USDJPY'] - actual_data['S_USDJPY']) /
                    actual_data['S_USDJPY']) * 100
    print(f"誤差: {error_no_adj:+.2f}%")

    # Δm調整を追加
    print("\n--- Δm調整を追加 ---")
    engine.error_corrector.add_external_adjustment(
        month='2023-07',
        delta_m_adjustments={
            'USD': -0.005,  # USDの上昇を抑制
            'JPY': 0.003,   # JPYをやや上昇
            'TRY': 0.002    # TRYをやや上昇（ゼロサム制約で自動調整）
        },
        description='Turkish crisis: manual dampening of volatility'
    )

    # 調整後の予想
    forecast_adj = engine.forecast_next_month('2023-06')
    print(f"予想: USD/JPY = {forecast_adj['pred_USDJPY']:.2f}")
    print(f"実績: USD/JPY = {actual_data['S_USDJPY']:.2f}")
    error_adj = ((forecast_adj['pred_USDJPY'] - actual_data['S_USDJPY']) /
                 actual_data['S_USDJPY']) * 100
    print(f"誤差: {error_adj:+.2f}%")

    improvement = abs(error_no_adj) - abs(error_adj)
    print(f"\n改善: {improvement:.2f}ポイント")


def example_rate_adjustment():
    """
    例2: 為替レートへの直接調整
    2024年8月のJPY金利政策転換を手動で反映
    """
    print("\n\n" + "=" * 60)
    print("例2: 為替レートへの直接調整")
    print("=" * 60)

    engine = AdaptiveForecastEngine()

    # 調整なしで予想
    print("\n--- 調整なしの予想 ---")
    forecast_no_adj = engine.forecast_next_month('2024-07')
    actual_data = engine.get_month_data('2024-08')

    print(f"予想: USD/JPY = {forecast_no_adj['pred_USDJPY']:.2f}")
    print(f"実績: USD/JPY = {actual_data['S_USDJPY']:.2f}")
    error_no_adj = ((forecast_no_adj['pred_USDJPY'] - actual_data['S_USDJPY']) /
                    actual_data['S_USDJPY']) * 100
    print(f"誤差: {error_no_adj:+.2f}%")

    # レート調整を追加（JPY強含みを反映）
    print("\n--- レート調整を追加（JPY強含み -5%） ---")
    engine.error_corrector.add_external_adjustment(
        month='2024-08',
        rate_adjustments={
            'USDJPY': -5.0,  # USD/JPYを5%下方修正（JPY高）
        },
        description='JPY interest rate hike: manual downward adjustment'
    )

    # 調整後の予想
    forecast_adj = engine.forecast_next_month('2024-07')
    print(f"予想: USD/JPY = {forecast_adj['pred_USDJPY']:.2f}")
    print(f"実績: USD/JPY = {actual_data['S_USDJPY']:.2f}")
    error_adj = ((forecast_adj['pred_USDJPY'] - actual_data['S_USDJPY']) /
                 actual_data['S_USDJPY']) * 100
    print(f"誤差: {error_adj:+.2f}%")

    improvement = abs(error_no_adj) - abs(error_adj)
    print(f"\n改善: {improvement:.2f}ポイント")


def example_regime_addition():
    """
    例3: 新しいレジューム期間の追加
    将来のイベントを手動で登録
    """
    print("\n\n" + "=" * 60)
    print("例3: 新しいレジューム期間の追加")
    print("=" * 60)

    engine = AdaptiveForecastEngine()

    # 2025年12月に予想されるイベントを登録
    print("\n--- レジューム期間を追加 ---")
    engine.regime_detector.add_external_regime(
        month='2025-12',
        regime_type='transition',
        description='Expected FED policy change in December 2025',
        severity='medium',
        notes='Based on forward guidance and economic indicators'
    )

    # この設定を保存
    engine.regime_detector.save_regime_catalog('regime_catalog_updated.csv')
    print("レジュームカタログを regime_catalog_updated.csv に保存しました")

    # 予想を実行（2025-11のデータを使って2025-12を予想）
    print("\n--- 2025-12の予想 ---")
    forecast = engine.forecast_next_month('2025-11')

    print(f"予想: USD/JPY = {forecast['pred_USDJPY']:.2f}")
    print(f"レジューム係数: {forecast['regime_factor']}")
    print(f"信頼区間: {forecast['confidence_interval']['USDJPY'][0]:.2f}% "
          f"to {forecast['confidence_interval']['USDJPY'][1]:.2f}%")
    print(f"推奨: {forecast['recommendation']}")


def example_combined_adjustment():
    """
    例4: 複数の調整を組み合わせる
    """
    print("\n\n" + "=" * 60)
    print("例4: 複数の調整を組み合わせる")
    print("=" * 60)

    engine = AdaptiveForecastEngine()

    # レジューム期間を追加
    engine.regime_detector.add_external_regime(
        month='2023-07',
        regime_type='crisis',
        description='Turkish crisis with manual adjustments',
        severity='high'
    )

    # Δm調整を追加
    engine.error_corrector.add_external_adjustment(
        month='2023-07',
        delta_m_adjustments={
            'USD': -0.003,
            'JPY': 0.002,
            'TRY': 0.001
        },
        description='Combined: regime detection + manual delta-m correction'
    )

    # 予想を実行
    forecast = engine.forecast_next_month('2023-06')
    actual_data = engine.get_month_data('2023-07')

    print(f"\n予想: USD/JPY = {forecast['pred_USDJPY']:.2f}")
    print(f"実績: USD/JPY = {actual_data['S_USDJPY']:.2f}")
    error = ((forecast['pred_USDJPY'] - actual_data['S_USDJPY']) /
             actual_data['S_USDJPY']) * 100
    print(f"誤差: {error:+.2f}%")

    print(f"\nレジューム情報: {forecast['regime_info']['description']}")
    print(f"レジューム係数: {forecast['regime_factor']}")
    print(f"推奨: {forecast['recommendation']}")


def example_save_and_load_adjustments():
    """
    例5: 調整値の保存と読み込み
    """
    print("\n\n" + "=" * 60)
    print("例5: 調整値の保存と読み込み")
    print("=" * 60)

    engine = AdaptiveForecastEngine()

    # 複数の調整を追加
    print("\n--- 調整値を追加 ---")
    engine.error_corrector.add_external_adjustment(
        month='2023-07',
        delta_m_adjustments={'USD': -0.005, 'JPY': 0.003, 'TRY': 0.002},
        description='Turkish crisis correction'
    )

    engine.error_corrector.add_external_adjustment(
        month='2024-08',
        rate_adjustments={'USDJPY': -5.0},
        description='JPY rate hike correction'
    )

    # 保存
    engine.error_corrector.save_adjustments('my_adjustments.csv')
    print("調整値を my_adjustments.csv に保存しました")

    # 新しいエンジンを作成して読み込み
    print("\n--- 調整値を読み込み ---")
    engine2 = AdaptiveForecastEngine()
    engine2.error_corrector.load_adjustments('my_adjustments.csv')

    print(f"読み込んだ調整: {len(engine2.error_corrector.external_adjustments)}件")
    for month, adj in engine2.error_corrector.external_adjustments.items():
        print(f"  {month}: {adj['description']}")


def main():
    """すべての例を実行"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "MCI 外部調整機能の使用例" + " " * 22 + "║")
    print("╚" + "═" * 58 + "╝")

    example_delta_m_adjustment()
    example_rate_adjustment()
    example_regime_addition()
    example_combined_adjustment()
    example_save_and_load_adjustments()

    print("\n\n" + "=" * 60)
    print("すべての例が完了しました！")
    print("詳細は README.md を参照してください。")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
