from flask import Flask, render_template, request, jsonify
import csv

# Assuming your existing files are in the same directory or accessible
# from the directory where you run this Flask app
from final import calculate_intrinsic_value
from data import get_stock_ticker, get_current_price

app = Flask(__name__)

def load_stock_list(csv_filepath="ind_nifty200list.csv"):
    """
    Reads the stock list from a CSV file and returns a list of dictionaries.
    Each dictionary contains 'Company Name' and 'Symbol'.
    """
    stock_list = []
    try:
        with open(csv_filepath, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            # Assuming the CSV has 'Company Name' and 'Symbol' columns
            for row in reader:
                # Basic check to ensure required columns exist
                if 'Company Name' in row and 'Symbol' in row:
                     # Optionally filter for EQ series if needed, but for autocomplete, include all
                    stock_list.append({
                        'Company Name': row['Company Name'],
                        'Symbol': row['Symbol']
                    })
                else:
                    print(f"Warning: Skipping row due to missing columns: {row}")
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_filepath}")
        # Return an empty list or raise an error as appropriate
        return [] # Return empty list if file not found
    except Exception as e:
        print(f"Error reading CSV file {csv_filepath}: {e}")
        return [] # Return empty list on other errors
    return stock_list

@app.route('/')
def index():
    """Render the main form page."""
    stock_list = load_stock_list()
    # Render with empty results/error and no initial form data, passing stock_list
    return render_template('index.html', results={}, error=None, form_data={}, stock_list=stock_list)

@app.route('/calculate', methods=['POST'])
def calculate():
    """Handle the calculation request."""
    stock_list = load_stock_list() # Load stock list for rendering the page again
    # Get form data. request.form is a dictionary-like object.
    form_data = request.form
    ticker_symbol = form_data.get('ticker')

    # Safely convert form data, providing defaults and handling potential errors
    try:
        projection_years = int(form_data.get('projection_years', 10))
        discount_rate = float(form_data.get('discount_rate', 0.10))
        terminal_growth_rate = float(form_data.get('terminal_growth_rate', 0.02))

        # Handle optional overrides
        initial_cagr_str = form_data.get('initial_cagr')
        reduced_cagr_str = form_data.get('reduced_cagr')
        # Convert whole number percentages to decimals if provided
        initial_cagr = float(initial_cagr_str) / 100.0 if initial_cagr_str else None
        reduced_cagr = float(reduced_cagr_str) / 100.0 if reduced_cagr_str else None

    except ValueError as e:
        # Pass form data back on error to retain user input, also pass stock_list
        return render_template('index.html', error=f"Invalid input for numerical fields: {e}", form_data=form_data, stock_list=stock_list)
    except Exception as e:
        # Pass form data back on error to retain user input, also pass stock_list
        return render_template('index.html', error=f"An unexpected error occurred with form data: {e}", form_data=form_data, stock_list=stock_list)

    results = {}
    error = None
    current_price = None

    try:
        # Your calculate_intrinsic_value function expects a yfinance.Ticker object
        # Let's get the ticker object first
        ticker = get_stock_ticker(ticker_symbol)

        # Call your existing calculation function (now returns a dictionary)
        calculation_results = calculate_intrinsic_value(
            ticker=ticker,
            projection_years=projection_years,
            discount_rate=discount_rate,
            terminal_growth_rate=terminal_growth_rate,
            initial_cagr=initial_cagr,
            reduced_cagr=reduced_cagr
        )

        # Fetch current price
        try:
            current_price = get_current_price(ticker)
        except ValueError as e:
             # If current price cannot be fetched, note it but don't fail the whole calculation
             print(f"Warning: {e}") # Log the warning
             current_price = "N/A"

        # Prepare results to pass to template, including detailed breakdown and input parameters
        results = {
            "ticker": ticker_symbol.upper(),
            "intrinsic_value_total": calculation_results["intrinsic_value_total"],
            "intrinsic_value_per_share": calculation_results["intrinsic_value_per_share"],
            "future_fcfs": calculation_results["future_fcfs"],
            "discounted_fcfs": calculation_results["discounted_fcfs"],
            "discounted_terminal_value": calculation_results["discounted_terminal_value"],
            "outstanding_shares": calculation_results["outstanding_shares"],
            "last_fcf": calculation_results["last_fcf"],
            "initial_cagr_used": calculation_results["initial_cagr_used"],
            "reduced_cagr_used": calculation_results["reduced_cagr_used"],
            "historical_cagr": calculation_results["historical_cagr"],
            "current_price": current_price,
            "projection_years": projection_years, # Add input parameter
            "discount_rate": discount_rate,     # Add input parameter
            "terminal_growth_rate": terminal_growth_rate # Add input parameter
        }

    except Exception as e:
        # Catch any errors during data fetching or calculation
        error = f"An error occurred during calculation: {e}"
        print(f"Calculation Error: {e}") # Print error for debugging
        # Pass form data back on error to retain user input, also pass stock_list
        return render_template('index.html', results={}, error=error, form_data=form_data, stock_list=stock_list)

    # Render the index page again, passing the results, error (should be None here), form_data, and stock_list
    return render_template('index.html', results=results, error=error, form_data=form_data, stock_list=stock_list)

if __name__ == '__main__':
    app.run(debug=True)
