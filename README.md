# SEC Filing Connector

A Python CLI and library for looking up SEC company information and filings.

## Installation

```bash
pip install -e .
```

This installs the package in editable mode with all dependencies from `pyproject.toml` (httpx, pydantic, pytest).

## Running Tests

```bash
pytest
```

Run all tests in `tests/test_client.py`. Tests cover:
- Company lookup with CIK zero-padding to 10 digits
- Filings filtering by form type and date range
- Results sorting and limiting

## CLI Usage

Look up a company and retrieve filings:

```bash
python -m sec_connector.cli AAPL --form 10-K --limit 5
```

**Arguments:**
- `TICKER` (required): Stock ticker symbol (e.g., AAPL, MSFT)
- `--form`: Filter by form type (e.g., 10-K, 10-Q)
- `--limit`: Max number of results (default: 10)

**Example:**
```bash
python -m sec_connector.cli MSFT --form 10-Q --limit 3
```

## Fixtures

Sample data is in `tests/fixtures/`:
- `company_tickers.json`: Ticker → CIK/name mapping
- `filings_sample.json`: Sample SEC filings

Currently, `_fetch_filings_from_sec()` loads from the fixture file. To use real SEC EDGAR data, implement an httpx-based API call.

## Project Structure

```
sec_connector/
  __init__.py
  cli.py          # CLI entry point
  client.py       # SECClient class
  models.py       # Pydantic models (Company, Filing, FilingFilter)
tests/
  test_client.py  # Unit tests
  fixtures/
    company_tickers.json
    filings_sample.json
```
