# Stock Intrinsic Value Calculator

## Concept

This project provides a web-based tool to calculate the intrinsic value of a stock using a Free Cash Flow (FCF) based Discounted Cash Flow (DCF) model. It allows users to input a stock ticker symbol and various financial parameters to estimate the stock's fair value.

## Idea

The core idea is to provide a simple and accessible interface for individual investors or analysts to perform fundamental stock valuation based on projected future cash flows. By automating the data retrieval and calculation process, the tool aims to make DCF analysis more approachable.

## Solution

The solution is a Flask web application that serves as the front-end. It interacts with backend Python scripts responsible for:

1.  **Data Retrieval:** Fetching historical stock data, including financial statements and stock prices, likely using a library like `yfinance`.
2.  **FCF Calculation:** Estimating historical Free Cash Flow based on retrieved financial data.
3.  **Projection:** Projecting future Free Cash Flows based on user-defined growth rates (initial and reduced CAGR) and projection years.
4.  **Discounting:** Discounting future FCFs and a terminal value back to the present using a specified discount rate.
5.  **Intrinsic Value Calculation:** Calculating the total intrinsic value of the company and the intrinsic value per share based on the number of outstanding shares.

The application provides a form for user input and displays the calculation results, including a breakdown of projected and discounted cash flows.

## Deployment

To deploy this project, follow these steps:

1.  **Prerequisites:**
    *   Python 3.6+
    *   `uv` or `pip` for dependency management
    *   Internet connection to fetch stock data.

2.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd valuation-stocks
    ```
    (Replace `<repository_url>` with the actual URL of your repository)

3.  **Set up the virtual environment and install dependencies:**
    If using `uv` (recommended, as indicated by `uv.lock`):
    ```bash
    uv sync
    ```
    *(Note: Based on `uv.lock` and `pyproject.toml`, `uv sync` is the likely intended method for dependency management)*

4.  **Run the Flask application:**
    ```bash
    export FLASK_APP=app.py
    export FLASK_ENV=development # Optional: for development mode
    flask run
    ```
    Alternatively, you can run directly:
    ```bash
    python app.py
    ```

5.  **Access the application:**
    Open your web browser and go to `http://127.0.0.1:5000/` (or the address shown in the terminal output).

## Usage

1.  Open the application in your web browser.
2.  Enter the stock ticker symbol you want to value (e.g., `TCS.NS.`, `HDFCBANK.NS.`).
3.  Adjust the valuation parameters (projection years, discount rate, terminal growth rate, optional initial and reduced CAGRs) as needed.
4.  Click the "Calculate Intrinsic Value" button.
5.  The page will refresh, displaying the calculated intrinsic value per share, the current stock price (if available), and a breakdown of the projected and discounted Free Cash Flows.


