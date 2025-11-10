import json
import argparse
from pathlib import Path
from sec_connector.client import SECClient
from sec_connector.models import FilingFilter

def main():
    """
    Usage: python -m sec_connector.cli AAPL --form 10-K --limit 5
    """
    # TODO: Parse args (use argparse or simple sys.argv)
    # Load fixtures
    # Call client methods
    # Print results as table or JSON
    parser = argparse.ArgumentParser(description="SEC Filing CLI")
    parser.add_argument("ticker", type = str, help="Company ticker symbol")
    parser.add_argument("--form", type=str, help="Form type(s)")
    parser.add_argument("--limit", type=int, default=10, help="Result limit")

    args = parser.parse_args()

    # Load data
    fixture_path = Path(__file__).parent / "fixtures" / "company_tickers.json"
    companies_data = json.load(open(fixture_path))
    client = SECClient(companies_data)
    filters = FilingFilter(
        form_types=[args.form] if args.form else None, # Wrap in list
        limit=args.limit
    )

    company = client.lookup_company(args.ticker)
    filings = client.list_filings(company.cik, filters)
    print(filings)

if __name__ == "__main__":
    main()