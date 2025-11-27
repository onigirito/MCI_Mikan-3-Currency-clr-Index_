#!/usr/bin/env python3
"""
Recalculate 2025 monthly MCI data with updated IMF WEO October 2025 PPP values.
Updates from:
  PPP_JPY: 93.2 -> 93.52
  PPP_TRY: 16.63 -> 16.51
"""

import csv
import math
from typing import List, Dict

# IMF WEO October 2025 PPP values
PPP_JPY_2025 = 93.52
PPP_TRY_2025 = 16.51

def calculate_mci(S_USDJPY: float, S_USDTRY: float, PPP_JPY: float, PPP_TRY: float) -> Dict:
    """Calculate MCI coordinates and related metrics."""
    # PPP deviation rates
    d_USDJPY = math.log(S_USDJPY / PPP_JPY)
    d_USDTRY = math.log(S_USDTRY / PPP_TRY)

    # MCI coordinates (clr transformation)
    m_USD = (d_USDJPY + d_USDTRY) / 3
    m_JPY = (-2 * d_USDJPY + d_USDTRY) / 3
    m_TRY = (d_USDJPY - 2 * d_USDTRY) / 3

    # Cross rates
    S_TRYJPY = S_USDJPY / S_USDTRY
    PPP_TRYJPY = PPP_JPY / PPP_TRY
    d_TRYJPY = math.log(S_TRYJPY / PPP_TRYJPY)

    return {
        'd_USDJPY': d_USDJPY,
        'd_USDTRY': d_USDTRY,
        'm_USD': m_USD,
        'm_JPY': m_JPY,
        'm_TRY': m_TRY,
        'S_TRYJPY': S_TRYJPY,
        'PPP_TRYJPY': PPP_TRYJPY,
        'd_TRYJPY': d_TRYJPY
    }

def update_monthly_mci_analysis():
    """Update monthly_mci_analysis.csv with new 2025 PPP values."""
    print("Updating monthly_mci_analysis.csv...")

    rows = []
    with open('monthly_mci_analysis.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Track previous m_TRY for D_mTRY calculation
    prev_m_TRY = None

    for i, row in enumerate(rows):
        date = row['date']

        # Only update 2025 data
        if not date.startswith('2025'):
            prev_m_TRY = float(row['m_TRY'])
            continue

        S_USDJPY = float(row['S_USDJPY'])
        S_USDTRY = float(row['S_USDTRY'])

        # Calculate with new PPP values
        result = calculate_mci(S_USDJPY, S_USDTRY, PPP_JPY_2025, PPP_TRY_2025)

        # Update row
        row['PPP_JPY'] = str(PPP_JPY_2025)
        row['PPP_TRY'] = str(PPP_TRY_2025)
        row['d_USDJPY'] = str(result['d_USDJPY'])
        row['d_USDTRY'] = str(result['d_USDTRY'])
        row['m_USD'] = str(result['m_USD'])
        row['m_JPY'] = str(result['m_JPY'])
        row['m_TRY'] = str(result['m_TRY'])

        # Calculate D_mTRY (monthly change)
        if prev_m_TRY is not None:
            D_mTRY = result['m_TRY'] - prev_m_TRY
            row['D_mTRY'] = str(D_mTRY)

            # Calculate percentage change in TRY/JPY
            if i > 0:
                prev_S_TRYJPY = float(rows[i-1]['S_TRYJPY'])
                pct_TRYJPY = ((result['S_TRYJPY'] - prev_S_TRYJPY) / prev_S_TRYJPY) * 100
                row['pct_TRYJPY'] = str(pct_TRYJPY)

        prev_m_TRY = result['m_TRY']

        # Update PPP_changed flag for January 2025
        if date == '2025-01':
            row['PPP_changed'] = 'YES'

    # Write updated data
    with open('monthly_mci_analysis.csv', 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['date', 'S_USDJPY', 'S_USDTRY', 'S_TRYJPY', 'PPP_JPY', 'PPP_TRY',
                     'PPP_changed', 'd_USDJPY', 'd_USDTRY', 'm_USD', 'm_JPY', 'm_TRY',
                     'D_mTRY', 'pct_TRYJPY']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Updated {sum(1 for r in rows if r['date'].startswith('2025'))} rows for 2025")

def update_mci_monthly_recent():
    """Update mci_monthly_recent.csv with new 2025 PPP values."""
    print("Updating mci_monthly_recent.csv...")

    rows = []
    with open('mci_monthly_recent.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for row in rows:
        date = row['date']

        # Only update 2025 data
        if not date.startswith('2025'):
            continue

        S_USDJPY = float(row['S_USDJPY'])
        S_USDTRY = float(row['S_USDTRY'])

        # Calculate with new PPP values
        result = calculate_mci(S_USDJPY, S_USDTRY, PPP_JPY_2025, PPP_TRY_2025)

        # Update row
        row['PPP_JPY'] = str(PPP_JPY_2025)
        row['PPP_TRY'] = str(PPP_TRY_2025)
        row['d_USDJPY'] = str(result['d_USDJPY'])
        row['d_USDTRY'] = str(result['d_USDTRY'])
        row['m_USD'] = str(result['m_USD'])
        row['m_JPY'] = str(result['m_JPY'])
        row['m_TRY'] = str(result['m_TRY'])
        row['S_TRYJPY'] = str(result['S_TRYJPY'])
        row['PPP_TRYJPY'] = str(result['PPP_TRYJPY'])
        row['d_TRYJPY'] = str(result['d_TRYJPY'])

    # Write updated data
    with open('mci_monthly_recent.csv', 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['date', 'S_USDJPY', 'S_USDTRY', 'PPP_JPY', 'PPP_TRY',
                     'd_USDJPY', 'd_USDTRY', 'm_USD', 'm_JPY', 'm_TRY',
                     'S_TRYJPY', 'PPP_TRYJPY', 'd_TRYJPY']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Updated {sum(1 for r in rows if r['date'].startswith('2025'))} rows for 2025")

def update_monthly_mci_interpolated():
    """Update monthly_mci_interpolated.csv with new 2025 PPP values.
    Note: This uses monthly interpolated PPP, so we need to recalculate interpolation for 2025.
    """
    print("Updating monthly_mci_interpolated.csv...")

    # Read existing data
    rows = []
    with open('monthly_mci_interpolated.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # For 2025, we only have one year's PPP value (no next year for interpolation)
    # So we'll use the same PPP value throughout 2025
    # In 2026 when we get new values, we can interpolate between 2025 and 2026

    prev_m_TRY = None

    for i, row in enumerate(rows):
        date = row['date']

        # Only update 2025 data
        if not date.startswith('2025'):
            prev_m_TRY = float(row['m_TRY'])
            continue

        S_USDJPY = float(row['S_USDJPY'])
        S_USDTRY = float(row['S_USDTRY'])

        # For 2025, use constant PPP (no interpolation without 2026 data)
        PPP_JPY = PPP_JPY_2025
        PPP_TRY = PPP_TRY_2025

        # Calculate with new PPP values
        result = calculate_mci(S_USDJPY, S_USDTRY, PPP_JPY, PPP_TRY)

        # Update row
        row['PPP_JPY'] = str(PPP_JPY)
        row['PPP_TRY'] = str(PPP_TRY)
        row['d_USDJPY'] = str(result['d_USDJPY'])
        row['d_USDTRY'] = str(result['d_USDTRY'])
        row['m_USD'] = str(result['m_USD'])
        row['m_JPY'] = str(result['m_JPY'])
        row['m_TRY'] = str(result['m_TRY'])

        # Calculate D_mTRY (monthly change)
        if prev_m_TRY is not None:
            D_mTRY = result['m_TRY'] - prev_m_TRY
            row['D_mTRY'] = str(D_mTRY)

            # Calculate percentage change in TRY/JPY
            if i > 0:
                prev_S_TRYJPY = float(rows[i-1]['S_TRYJPY'])
                pct_TRYJPY = ((result['S_TRYJPY'] - prev_S_TRYJPY) / prev_S_TRYJPY) * 100
                row['pct_TRYJPY'] = str(pct_TRYJPY)

        prev_m_TRY = result['m_TRY']

    # Write updated data
    with open('monthly_mci_interpolated.csv', 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['date', 'S_USDJPY', 'S_USDTRY', 'S_TRYJPY', 'PPP_JPY', 'PPP_TRY',
                     'd_USDJPY', 'd_USDTRY', 'm_USD', 'm_JPY', 'm_TRY',
                     'D_mTRY', 'pct_TRYJPY']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Updated {sum(1 for r in rows if r['date'].startswith('2025'))} rows for 2025")

def main():
    """Main execution."""
    print("=" * 60)
    print("Recalculating 2025 Monthly MCI Data")
    print("=" * 60)
    print(f"Old PPP values: JPY=93.2, TRY=16.63")
    print(f"New PPP values: JPY={PPP_JPY_2025}, TRY={PPP_TRY_2025}")
    print(f"Source: IMF WEO October 2025")
    print("=" * 60)
    print()

    update_monthly_mci_analysis()
    update_mci_monthly_recent()
    update_monthly_mci_interpolated()

    print()
    print("=" * 60)
    print("✓ All 2025 monthly MCI data has been recalculated!")
    print("=" * 60)

if __name__ == '__main__':
    main()
