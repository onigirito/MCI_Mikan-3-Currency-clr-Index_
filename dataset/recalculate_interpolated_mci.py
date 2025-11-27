#!/usr/bin/env python3

"""
Recalculate monthly_mci_interpolated.csv with proper linear interpolation of PPP values.

Interpolation logic:
- Each year's January uses that year's annual PPP value
- From January to December, PPP linearly interpolates to next year's value
- Example: 2024-01 uses 2024 PPP, 2024-12 approaches 2025 PPP

Annual PPP values:
- 2022: JPY=92.5, TRY=4.975
- 2023: JPY=92.84, TRY=8.074
- 2024: JPY=93.2, TRY=12.55
- 2025: JPY=93.52, TRY=16.51 (IMF WEO October 2025 estimate)
"""

import csv
import math
from typing import Dict

# Annual PPP values
ANNUAL_PPP = {
    2022: {"JPY": 92.5, "TRY": 4.975},
    2023: {"JPY": 92.84, "TRY": 8.074},
    2024: {"JPY": 93.2, "TRY": 12.55},
    2025: {"JPY": 93.52, "TRY": 16.51},
}

def interpolate_ppp(year: int, month: int) -> Dict[str, float]:
    """
    Calculate interpolated PPP for a given year-month.

    Logic: PPP(year, month) = PPP(year) + (PPP(year+1) - PPP(year)) * (month - 1) / 12
    """
    current_year_ppp = ANNUAL_PPP[year]

    # For December 2025, use 2025 value (no next year data)
    if year == 2025:
        next_year_ppp = current_year_ppp
    else:
        next_year_ppp = ANNUAL_PPP[year + 1]

    # Linear interpolation
    ppp_jpy = current_year_ppp["JPY"] + (next_year_ppp["JPY"] - current_year_ppp["JPY"]) * (month - 1) / 12
    ppp_try = current_year_ppp["TRY"] + (next_year_ppp["TRY"] - current_year_ppp["TRY"]) * (month - 1) / 12

    return {"JPY": ppp_jpy, "TRY": ppp_try}

def calculate_mci(S_USDJPY: float, S_USDTRY: float, PPP_JPY: float, PPP_TRY: float) -> Dict:
    """Calculate MCI coordinates and related metrics with interpolated PPP."""
    # PPP deviation rates
    d_USDJPY = math.log(S_USDJPY / PPP_JPY)
    d_USDTRY = math.log(S_USDTRY / PPP_TRY)

    # MCI coordinates (centered log-ratio transformation)
    d_sum = d_USDJPY + d_USDTRY
    m_USD = (2 * 0 - d_sum) / 3  # d_USDUSD = 0
    m_JPY = (2 * d_USDJPY - d_sum) / 3
    m_TRY = (2 * d_USDTRY - d_sum) / 3

    # Cross rate
    S_TRYJPY = S_USDJPY / S_USDTRY
    PPP_TRYJPY = PPP_JPY / PPP_TRY
    d_TRYJPY = math.log(S_TRYJPY / PPP_TRYJPY)

    return {
        "d_USDJPY": d_USDJPY,
        "d_USDTRY": d_USDTRY,
        "m_USD": m_USD,
        "m_JPY": m_JPY,
        "m_TRY": m_TRY,
        "S_TRYJPY": S_TRYJPY,
        "PPP_TRYJPY": PPP_TRYJPY,
        "d_TRYJPY": d_TRYJPY,
    }

def main():
    # Read monthly exchange rate data
    with open("monthly_rates_data.csv", "r") as f:
        reader = csv.DictReader(f)
        rates_data = list(reader)

    # Recalculate with interpolated PPP
    output_rows = []
    prev_m_TRY = None

    for row in rates_data:
        date = row["date"]
        year, month = map(int, date.split("-"))

        S_USDJPY = float(row["S_USDJPY"])
        S_USDTRY = float(row["S_USDTRY"])

        # Interpolate PPP
        ppp = interpolate_ppp(year, month)
        PPP_JPY = ppp["JPY"]
        PPP_TRY = ppp["TRY"]

        # Calculate MCI
        mci = calculate_mci(S_USDJPY, S_USDTRY, PPP_JPY, PPP_TRY)

        # Calculate D_mTRY (monthly change in TRY coordinate)
        if prev_m_TRY is not None:
            D_mTRY = mci["m_TRY"] - prev_m_TRY
        else:
            D_mTRY = None
        prev_m_TRY = mci["m_TRY"]

        # Calculate pct_TRYJPY (percentage change from PPP)
        pct_TRYJPY = (mci["S_TRYJPY"] / mci["PPP_TRYJPY"] - 1) * 100

        output_rows.append({
            "date": date,
            "S_USDJPY": S_USDJPY,
            "S_USDTRY": S_USDTRY,
            "S_TRYJPY": mci["S_TRYJPY"],
            "PPP_JPY": PPP_JPY,
            "PPP_TRY": PPP_TRY,
            "d_USDJPY": mci["d_USDJPY"],
            "d_USDTRY": mci["d_USDTRY"],
            "m_USD": mci["m_USD"],
            "m_JPY": mci["m_JPY"],
            "m_TRY": mci["m_TRY"],
            "D_mTRY": D_mTRY if D_mTRY is not None else "",
            "pct_TRYJPY": pct_TRYJPY,
        })

    # Write to CSV
    with open("monthly_mci_interpolated.csv", "w", newline="") as f:
        fieldnames = ["date", "S_USDJPY", "S_USDTRY", "S_TRYJPY", "PPP_JPY", "PPP_TRY",
                      "d_USDJPY", "d_USDTRY", "m_USD", "m_JPY", "m_TRY", "D_mTRY", "pct_TRYJPY"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    print("=" * 60)
    print("✓ monthly_mci_interpolated.csv has been recalculated!")
    print("=" * 60)
    print("\nInterpolated PPP values (sample):")
    print(f"2024-01: JPY={interpolate_ppp(2024, 1)['JPY']:.2f}, TRY={interpolate_ppp(2024, 1)['TRY']:.2f}")
    print(f"2024-06: JPY={interpolate_ppp(2024, 6)['JPY']:.2f}, TRY={interpolate_ppp(2024, 6)['TRY']:.2f}")
    print(f"2024-12: JPY={interpolate_ppp(2024, 12)['JPY']:.2f}, TRY={interpolate_ppp(2024, 12)['TRY']:.2f}")
    print(f"2025-01: JPY={interpolate_ppp(2025, 1)['JPY']:.2f}, TRY={interpolate_ppp(2025, 1)['TRY']:.2f}")
    print(f"2025-11: JPY={interpolate_ppp(2025, 11)['JPY']:.2f}, TRY={interpolate_ppp(2025, 11)['TRY']:.2f}")
    print("\n✓ All d (PPP deviation) and m (MCI coordinates) recalculated with interpolated PPP!")

if __name__ == "__main__":
    main()
