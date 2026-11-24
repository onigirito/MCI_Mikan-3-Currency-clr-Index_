#!/usr/bin/env python3
"""
Rebuild the derived columns of monthly_mci_complete_2022_2025.csv.

Inputs
  - monthly_mci_complete_2022_2025.csv: date, S_USDJPY, S_USDTRY (monthly market rates from X-Rates and
    Exchange-Rates.org, as recorded in the original monthly_rates_data.csv)
  - annual_mci_2005_2024.csv: annual PPP_JPY, PPP_TRY (IMF WEO, same values as the paper's
    annual analysis), plus PPP_2025 below (IMF WEO October 2025 projection)

Monthly PPP (paper, Section 8.3): the annual value is the December value, and
  PPP(year, month) = PPP(year-1) + (PPP(year) - PPP(year-1)) * month / 12
so January 2022 starts from the 2021 annual value and December of each year equals
that year's annual value.

Derived columns (dataset/README.md, Section 4.3)
  S_TRYJPY = S_USDJPY / S_USDTRY
  d_USDJPY = ln(S_USDJPY / PPP_JPY), d_USDTRY = ln(S_USDTRY / PPP_TRY)
  m_USD = (d_USDJPY + d_USDTRY) / 3
  m_JPY = (-2 d_USDJPY + d_USDTRY) / 3
  m_TRY = (d_USDJPY - 2 d_USDTRY) / 3
  pct_TRYJPY = (S_TRYJPY[t] / S_TRYJPY[t-1] - 1) * 100 (month-over-month change of the
    TRY/JPY rate, the same quantity as in monthly_mci_fixed_ppp_2022_2025.csv)
  delta_m_* = m_*[t] - m_*[t-1]
  D_mTRY = delta_m_TRY (original column name for the monthly change in m_TRY)
  avg_delta_m_*_3m = mean of delta_m_* over months t-2..t

Prediction and error columns are left to backtest_with_rolling_avg.py --comprehensive.
Cells whose value does not change are kept byte-for-byte.

Usage:
  python build_monthly_mci.py
  python backtest_with_rolling_avg.py --comprehensive
"""

import csv
import math

MONTHLY_CSV = 'monthly_mci_complete_2022_2025.csv'
ANNUAL_CSV = 'annual_mci_2005_2024.csv'
PPP_2025 = {'JPY': 93.52, 'TRY': 16.51}  # IMF WEO October 2025 projection


def load_annual_ppp():
    with open(ANNUAL_CSV, encoding='utf-8', newline='') as f:
        ppp = {int(r['year']): {'JPY': float(r['PPP_JPY']), 'TRY': float(r['PPP_TRY'])}
               for r in csv.DictReader(f)}
    ppp[2025] = dict(PPP_2025)
    return ppp


def monthly_ppp(ppp, year, month, cur):
    prev, curr = ppp[year - 1][cur], ppp[year][cur]
    return prev + (curr - prev) * month / 12


def main():
    ppp = load_annual_ppp()
    with open(MONTHLY_CSV, encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)

    values = []
    for r in rows:
        year, month = map(int, r['date'].split('-'))
        s_uj, s_ut = float(r['S_USDJPY']), float(r['S_USDTRY'])
        p_j, p_t = monthly_ppp(ppp, year, month, 'JPY'), monthly_ppp(ppp, year, month, 'TRY')
        d_uj, d_ut = math.log(s_uj / p_j), math.log(s_ut / p_t)
        m_usd = (d_uj + d_ut) / 3
        m_jpy = (-2 * d_uj + d_ut) / 3
        m_try = (d_uj - 2 * d_ut) / 3
        s_tj = s_uj / s_ut
        values.append({
            'S_TRYJPY': s_tj, 'PPP_JPY': p_j, 'PPP_TRY': p_t,
            'd_USDJPY': d_uj, 'd_USDTRY': d_ut,
            'm_USD': m_usd, 'm_JPY': m_jpy, 'm_TRY': m_try,
        })
    for i, v in enumerate(values):
        v['pct_TRYJPY'] = None if i == 0 else (v['S_TRYJPY'] / values[i - 1]['S_TRYJPY'] - 1) * 100
        for c in ('USD', 'JPY', 'TRY'):
            v[f'delta_m_{c}'] = None if i == 0 else v[f'm_{c}'] - values[i - 1][f'm_{c}']
    for i, v in enumerate(values):
        for c in ('USD', 'JPY', 'TRY'):
            v[f'avg_delta_m_{c}_3m'] = (None if i < 3 else
                                        sum(values[j][f'delta_m_{c}'] for j in range(i - 2, i + 1)) / 3)

    changed = set()
    for r, v in zip(rows, values):
        for col, new in v.items():
            old = r[col]
            if new is None:
                if old != '':
                    r[col] = ''
                    changed.add(r['date'])
                continue
            if old == '' or abs(float(old) - new) > 1e-12 * max(1.0, abs(new)):
                r[col] = str(new)
                changed.add(r['date'])
        if r['D_mTRY'] != r['delta_m_TRY']:
            r['D_mTRY'] = r['delta_m_TRY']
            changed.add(r['date'])

    with open(MONTHLY_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f'Rows updated: {len(changed)}' + (f' ({min(changed)} .. {max(changed)})' if changed else ''))
    print('Next: python backtest_with_rolling_avg.py --comprehensive')


if __name__ == '__main__':
    main()
