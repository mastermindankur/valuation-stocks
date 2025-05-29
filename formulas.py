import numpy as np
import pandas as pd

def calculate_fcf_cagr1(fcf_df: pd.DataFrame, years: int) -> float:
    """
    Calculates the CAGR of Free Cash Flow based on the most recent 'years' of data.
    """
    fcf_df = fcf_df.sort_index()
    start_fcf = fcf_df["free_cash_flow"].iloc[-(years+1)]
    end_fcf = fcf_df["free_cash_flow"].iloc[-1]
    print(f"\nCalculating FCF CAGR using last {years} years of data...")
    print(f"Start FCF: ₹{start_fcf/1e7:.2f} Cr | End FCF: ₹{end_fcf/1e7:.2f} Cr")
    cagr = ((end_fcf / start_fcf) ** (1 / years)) - 1
    print(f"Computed CAGR: {cagr:.2f}%")
    return cagr

def calculate_fcf_cagr(fcf_df: pd.DataFrame, max_years: int) -> float:
    """
    Calculates CAGR for the longest period up to max_years where
    start and end FCF are both positive or both negative (to avoid complex numbers).
    """
    fcf_df = fcf_df.sort_index()
    fcf_series = fcf_df["free_cash_flow"]
    n = len(fcf_series)
    # Ensure max_years is not more than available data length - 1
    max_years = min(max_years, n - 1)

    end_fcf = fcf_series.iloc[-1]
    end_idx = n - 1

    def cagr_calc(start, end, period):
        return ((end / start) ** (1 / period)) - 1

    # Search for longest period from max_years down to 1
    for years in range(max_years, 0, -1):
        start_idx = end_idx - years
        start_fcf = fcf_series.iloc[start_idx]

        # Check if start and end have the same sign and neither is zero
        if start_fcf != 0 and end_fcf != 0:
            if (start_fcf > 0 and end_fcf > 0) or (start_fcf < 0 and end_fcf < 0):
                print(f"\nCalculating FCF CAGR using last {years} years of data...")
                print(f"Start FCF: ₹{start_fcf/1e7:.2f} Cr | End FCF: ₹{end_fcf/1e7:.2f} Cr")
                cagr = cagr_calc(start_fcf, end_fcf, years)
                return cagr

    raise ValueError("No suitable period found where start and end FCF have the same sign.")

def project_future_fcfs(last_fcf: float, growth_rate: float, projection_years: int = 5) -> list:
    """
    Projects future FCFs using the provided CAGR or growth rate.
    """
    print(f"\nProjecting future FCFs for {projection_years} years using CAGR: {growth_rate:.2%}")
    future_fcfs = []
    for year in range(1, projection_years + 1):
        projected_fcf = last_fcf * ((1 + growth_rate) ** year)
        future_fcfs.append(projected_fcf)
        #print(f"Year {year}: Projected FCF = ₹{projected_fcf/1e7:.2f} Cr")
    return future_fcfs

def discount_fcfs(future_fcfs: list, discount_rate: float) -> list:
    """
    Discounts future FCFs to present value using the discount rate.
    """
    print(f"\nDiscounting projected FCFs using Discount Rate: {discount_rate:.2%}")
    discounted_fcfs = []
    for t, fcf in enumerate(future_fcfs, start=1):
        pv = fcf / ((1 + discount_rate) ** t)
        discounted_fcfs.append(pv)
        #print(f"Year {t}: Discounted FCF = ₹{pv/1e7:.2f} Cr")
    return discounted_fcfs


def calculate_terminal_value(last_fcf: float, terminal_growth_rate: float, discount_rate: float) -> float:
    """
    Calculate terminal value using the Gordon Growth Model.
    TV = FCF * (1 + g) / (r - g)
    """
    tv = last_fcf * (1 + terminal_growth_rate) / (discount_rate - terminal_growth_rate)
    print(f"Calculated Terminal Value: ₹{tv/1e7:,.2f} Cr")
    return tv

def discount_terminal_value(terminal_value: float, discount_rate: float, year: int) -> float:
    """
    Discount terminal value back to present value.
    """
    discounted_tv = terminal_value / ((1 + discount_rate) ** year)
    print(f"Discounted Terminal Value (Present Value): ₹{discounted_tv/1e7:,.2f} Cr")
    return discounted_tv


# Test code
if __name__ == "__main__":
    from data import get_stock_ticker
    from fcf import get_historical_fcf

    print("Starting Intrinsic Value Calculation Test...\n")

    ticker = get_stock_ticker("SBIN.BO")
    print(f"Selected Ticker: {ticker}")

    fcf_df = get_historical_fcf(ticker)
    print(f"\nFetched Historical Free Cash Flow data:\n{fcf_df.tail()}")

    cagr = calculate_fcf_cagr(fcf_df)

    last_fcf = fcf_df["free_cash_flow"].iloc[-1]
    print(f"\nLast Year’s FCF (used as base): ₹{last_fcf/1e7:.2f} Cr")

    future_fcfs = project_future_fcfs(last_fcf, cagr, projection_years=5)

    discount_rate = 0.10  # Assumption: 10% WACC or required return
    discounted_fcfs = discount_fcfs(future_fcfs, discount_rate)

