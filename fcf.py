import yfinance as yf
import pandas as pd

def get_stock_ticker(stock_symbol: str):
    return yf.Ticker(stock_symbol)

def get_historical_fcf(ticker: yf.Ticker) -> pd.DataFrame:
    """
    Calculates Free Cash Flow (FCF) using:
    FCF = Operating Cash Flow - Capital Expenditure
    Returns a DataFrame with yearly values.
    """
    cashflow_df = ticker.cashflow.T  # Transpose for years as rows

    # Rename exact columns
    try:
        cashflow_df = cashflow_df.rename(columns={
            "Operating Cash Flow": "operating_cash_flow",
            "Capital Expenditure": "capex"
        })
    except KeyError as e:
        raise KeyError("Expected columns not found in cash flow data") from e

    # Keep only relevant and non-null rows
    cashflow_df = cashflow_df[["operating_cash_flow", "capex"]].dropna()

    # Calculate Free Cash Flow
    cashflow_df["free_cash_flow"] = (
        cashflow_df["operating_cash_flow"] + cashflow_df["capex"]
    )  # capex is negative, so we add
    print("Number of years of FCF data:", len(cashflow_df))
    return cashflow_df[["operating_cash_flow", "capex", "free_cash_flow"]]

# Testable entry point
if __name__ == "__main__":
    stock_symbol = "RELIANCE.BO"
    ticker = get_stock_ticker(stock_symbol)
    fcf_df = get_historical_fcf(ticker)
    print("===  Historical Free Cash Flow ===")
    print(fcf_df)