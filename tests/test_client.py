from datetime import date
from types import SimpleNamespace

from sec_connector.client import SECClient
from sec_connector.models import FilingFilter


def test_lookup_company_zero_pads_cik():
    client = SECClient({"AAPL": {"cik": 320193, "name": "Apple Inc."}})
    company = client.lookup_company("aapl")
    assert company.ticker == "AAPL"
    assert company.cik == "0000320193"
    assert company.name == "Apple Inc."


def test_lookup_company_not_found_raises():
    client = SECClient({})
    try:
        client.lookup_company("FOO")
        raised = False
    except ValueError:
        raised = True
    assert raised


def test_list_filings_filters_sort_and_limit():
    # prepare client and stubbed filings (no network)
    client = SECClient({"AAPL": {"cik": "320193", "name": "Apple"}})
    sample_filings = [
        SimpleNamespace(filing_date=date.fromisoformat("2023-02-01"), form_type="10-K"),
        SimpleNamespace(filing_date=date.fromisoformat("2023-01-15"), form_type="10-Q"),
        SimpleNamespace(filing_date=date.fromisoformat("2022-12-31"), form_type="8-K"),
        SimpleNamespace(filing_date=date.fromisoformat("2023-02-10"), form_type="10-Q"),
    ]
    # replace network fetch with local data
    client._fetch_filings_from_sec = lambda cik: list(sample_filings)

    filters = FilingFilter(
        form_types=["10-K", "10-Q"],
        date_from=date.fromisoformat("2023-01-01"),
        date_to=None,
        limit=2,
    )

    results = client.list_filings("0000320193", filters)

    # only form types in filter, only on/after start_date, sorted newest-first, limited
    assert len(results) == 2
    assert results[0].filing_date >= results[1].filing_date
    assert all(f.form_type in ("10-K", "10-Q") for f in results)
