from .models import Company, Filing, FilingFilter

class SECClient:
    def __init__(self, companies_data: dict[str, dict]):
        """Initialize with company ticker->info mapping."""
        self._companies = companies_data
    
    def lookup_company(self, ticker: str) -> Company:
        """Find company by ticker, raise ValueError if not found."""
        company_info = self._companies.get(ticker.upper())
        if not company_info:
            raise ValueError(f"Company with ticker {ticker} not found.")
        return Company(
            ticker=ticker.upper(),
            cik=str(company_info["cik"]).zfill(10),
            name=company_info["name"],
        )

    def list_filings(self, cik: str, filters: FilingFilter) -> list[Filing]:
        """
        Get filings for a CIK, applying filters.

        - Filter by form_types (if provided)
        - Filter by date range (if provided)
        - Sort by date descending
        - Limit results
        """
        # Fetch filings from SEC
        filings = self._fetch_filings_from_sec(cik)

        # Filter by form types if provided
        if filters.form_types:
            filings = [f for f in filings if f.form_type in filters.form_types]
        
        # Filter by date range if provided (use model field names date_from/date_to)
        if filters.date_from:
            filings = [f for f in filings if f.filing_date >= filters.date_from]
        if filters.date_to:
            filings = [f for f in filings if f.filing_date <= filters.date_to]
        
        # Sort by date descending (newest first)
        filings.sort(key=lambda f: f.filing_date, reverse=True)

        # Limit results if limit is set
        if filters.limit:
           filings = filings[:filters.limit]
        
        return filings

    def _fetch_filings_from_sec(self, cik: str):
        """Fetch filings from fixture (placeholder for real SEC API)."""
        from pathlib import Path
        import json
        from datetime import date
        from .models import Filing
        
        fixture_path = Path(__file__).parent.parent / "tests" / "fixtures" / "filings_sample.json"
        data = json.load(open(fixture_path))
        
        return [
            Filing(
                filing_date=date.fromisoformat(item["filing_date"]),
                form_type=item["form_type"],
                accession=item.get("accession"),
                url=item.get("url"),
                description=item.get("description"),
            )
            for item in data
        ]