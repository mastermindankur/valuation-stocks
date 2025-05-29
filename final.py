from formulas import calculate_fcf_cagr, discount_fcfs, calculate_terminal_value, discount_terminal_value
from data import get_stock_ticker, get_outstanding_shares, get_current_price
from fcf import get_historical_fcf


def calculate_intrinsic_value(
    ticker: str, 
    projection_years: int = 10, 
    discount_rate: float = 0.10, 
    terminal_growth_rate: float = 0.02, 
    initial_cagr: float = None,
    reduced_cagr: float = None):
    """
    Calculate the intrinsic value using two-stage FCF projection:
    - First 5 years with initial CAGR
    - Next 5 years with reduced CAGR
    """
    print("\n--- Assumptions Used ---")
    print(f"Projection Years: {projection_years}")
    print(f"Discount Rate: {discount_rate:.2%}")
    print(f"Terminal Growth Rate: {terminal_growth_rate:.2%}")
    print("-------------------------\n")

    print(f"Fetching historical free cash flow data for {ticker}...")
    fcf_df = get_historical_fcf(ticker)
    print(f"Free Cash Flow Data:\n{fcf_df.tail()}\n")

    historical_cagr = calculate_fcf_cagr(fcf_df, max_years=len(fcf_df)-1)
    print(f"Calculated FCF CAGR over last {len(fcf_df)-1} years: {historical_cagr:.2%}")

    last_fcf = fcf_df["free_cash_flow"].iloc[-1]
    print(f"Last reported Free Cash Flow: ₹{last_fcf / 1e7:,.2f} Cr")

    if initial_cagr is None:
        initial_cagr = historical_cagr  # Default: use historical CAGR
    if reduced_cagr is None:
        reduced_cagr = initial_cagr * 0.5  # Default: reduce CAGR by 50%

    print(f"\nProjecting future Free Cash Flows:")
    future_fcfs = []

    # First 5 years at initial_cagr
    fcf = last_fcf
    for year in range(1, 6):
        fcf *= (1 + initial_cagr)
        future_fcfs.append(fcf)
        print(f"Year {year} (Initial CAGR @ {initial_cagr:.2%}): ₹{fcf / 1e7:,.2f} Cr")

    # Next 5 years at reduced_cagr
    for year in range(6, 11):
        fcf *= (1 + reduced_cagr)
        future_fcfs.append(fcf)
        print(f"Year {year} (Reduced CAGR @ {reduced_cagr:.2%}): ₹{fcf / 1e7:,.2f} Cr")

    print(f"\nDiscounting projected Free Cash Flows at {discount_rate:.2%}...")
    discounted_fcfs = discount_fcfs(future_fcfs, discount_rate)
    for i, pv in enumerate(discounted_fcfs, 1):
        print(f"Year {i} discounted FCF: ₹{pv / 1e7:,.2f} Cr")

    terminal_value = calculate_terminal_value(future_fcfs[-1], terminal_growth_rate, discount_rate)
    discounted_tv = discount_terminal_value(terminal_value, discount_rate, projection_years)

    intrinsic_value = sum(discounted_fcfs) + discounted_tv
    print(f"\nSum of discounted projected FCFs: ₹{sum(discounted_fcfs)/1e7:,.2f} Cr")
    print(f"Discounted Terminal Value: ₹{discounted_tv/1e7:,.2f} Cr")
    print(f"Total Intrinsic Value (Enterprise Value): ₹{intrinsic_value/1e7:,.2f} Cr")

    print(f"\nFetching outstanding shares for {ticker}...")
    outstanding_shares = get_outstanding_shares(ticker)
    print(f"Outstanding Shares: {outstanding_shares:,}")

    intrinsic_value_per_share = intrinsic_value / outstanding_shares
    print(f"Intrinsic Value Per Share: ₹{intrinsic_value_per_share:,.2f}")

    # Return detailed results
    return {
        "intrinsic_value_total": intrinsic_value,
        "intrinsic_value_per_share": intrinsic_value_per_share,
        "future_fcfs": future_fcfs,
        "discounted_fcfs": discounted_fcfs,
        "discounted_terminal_value": discounted_tv,
        "outstanding_shares": outstanding_shares,
        "last_fcf": last_fcf,
        "initial_cagr_used": initial_cagr,
        "reduced_cagr_used": reduced_cagr,
        "historical_cagr": historical_cagr
    }


if __name__ == "__main__":
    ticker = get_stock_ticker("SBIN.BO")
    results = calculate_intrinsic_value(ticker) # Capture dictionary output
    print(f"\nFinal Results for {ticker}:") # Use direct ticker symbol for clarity
    print(f"Intrinsic Value: ₹{results['intrinsic_value_total']/1e7:,.2f} Cr") # Access dictionary keys
    print(f"Intrinsic Value Per Share: ₹{results['intrinsic_value_per_share']:,.2f}") # Access dictionary keys
