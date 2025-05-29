import yfinance as yf
import pandas as pd

def get_stock_ticker(stock_symbol: str):
    """
    Initialize yfinance Ticker object.
    
    Args:
        stock_symbol (str): Stock ticker symbol (e.g., 'TCS.BO')
    
    Returns:
        yfinance.Ticker object
    """
    return yf.Ticker(stock_symbol)


def get_income_statement(ticker):
    """
    Get the income statement (TTM or annual).
    
    Args:
        ticker (yfinance.Ticker): Ticker object
    
    Returns:
        pd.DataFrame: Income statement
    """
    return ticker.financials.T  # Transposed for easier reading


def get_balance_sheet(ticker):
    """
    Get the balance sheet.
    
    Args:
        ticker (yfinance.Ticker): Ticker object
    
    Returns:
        pd.DataFrame: Balance sheet
    """
    return ticker.balance_sheet.T


def get_cashflow_statement(ticker):
    """
    Get the cash flow statement.
    
    Args:
        ticker (yfinance.Ticker): Ticker object
    
    Returns:
        pd.DataFrame: Cashflow statement
    """
    return ticker.cashflow.T


def get_key_info(ticker):
    """
    Get key stock info: shares outstanding, debt, and cash.
    
    Args:
        ticker (yfinance.Ticker): Ticker object
    
    Returns:
        dict: Basic info required for DCF
    """
    info = ticker.info
    return {
        "shares_outstanding": info.get("sharesOutstanding", None),
        "total_debt": info.get("totalDebt", None),
        "cash": info.get("totalCash", None),
        "beta": info.get("beta", None),
        "sector": info.get("sector", None),
        "company_name": info.get("longName", None)
    }

def get_outstanding_shares(ticker_or_symbol) -> int:
    """
    Get the number of outstanding shares.
    
    Args:
        ticker_or_symbol (str or yfinance.Ticker): Stock ticker symbol or yfinance.Ticker object
    
    Returns:
        int: Number of outstanding shares
    """
    if isinstance(ticker_or_symbol, str):
        ticker = get_stock_ticker(ticker_or_symbol)
    else:
        ticker = ticker_or_symbol
    
    key_info = get_key_info(ticker)
    shares = key_info.get("shares_outstanding")
    
    if shares is None:
        raise ValueError("Could not retrieve shares outstanding for the ticker.")
    
    return shares


def get_current_price(ticker_or_symbol) -> float:
    """
    Get the current price of the stock.

    Args:
        ticker_or_symbol (str or yfinance.Ticker): Stock ticker symbol or yfinance.Ticker object

    Returns:
        float: Current stock price
    """
    if isinstance(ticker_or_symbol, str):
        ticker = get_stock_ticker(ticker_or_symbol)
    else:
        ticker = ticker_or_symbol

    info = ticker.info
    current_price = info.get("currentPrice")

    if current_price is None:
        raise ValueError(f"Could not retrieve current price for the ticker {ticker.info.get('symbol')}.")

    return current_price


if __name__ == "__main__":
    stock_symbol = "INFY.BO"
    ticker = get_stock_ticker(stock_symbol)
    income_statement = get_income_statement(ticker)
    balance_sheet = get_balance_sheet(ticker)
    cashflow_statement = get_cashflow_statement(ticker)
    key_info = get_key_info(ticker)
    outstanding_shares = get_outstanding_shares(ticker)
    current_price = get_current_price(ticker)

    print("===  Income Statement ===")
    print(income_statement)
    print("===  Balance Sheet ===")
    print(balance_sheet)
    print("===  Cashflow Statement ===")
    print(cashflow_statement)
    print("===  Key Info ===")
    print(key_info)
    print("===  Outstanding Shares ===")
    print(outstanding_shares)
    print("===  Current Price ===")
    print(current_price)


