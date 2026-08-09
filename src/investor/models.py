"""Data model describing a company's fundamentals used for analysis."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Stock:
    """A snapshot of a company's fundamentals.

    Attributes:
        symbol: Ticker symbol, e.g. "KO".
        name: Company name.
        annual_sales: Most recent annual sales/revenue (in the same
            currency units used by ``current_ratio`` etc.).
        current_assets: Total current assets.
        current_liabilities: Total current liabilities.
        long_term_debt: Total long-term debt.
        eps_history: Earnings per share for the trailing years, oldest
            first. At least 10 years is recommended by Graham, but any
            number of years can be supplied.
        dividend_years_paid: Consecutive number of years dividends have
            been paid without interruption.
        price: Current market price per share.
        pe_ratio: Price-to-earnings ratio (price divided by average
            trailing earnings).
        pb_ratio: Price-to-book ratio (price divided by book value per
            share).
    """

    symbol: str
    name: str
    annual_sales: float
    current_assets: float
    current_liabilities: float
    long_term_debt: float
    eps_history: List[float] = field(default_factory=list)
    dividend_years_paid: int = 0
    price: float = 0.0
    pe_ratio: float = 0.0
    pb_ratio: float = 0.0

    @property
    def current_ratio(self) -> float:
        """Current assets divided by current liabilities.

        A ratio of 2 or higher is Graham's classic rule of thumb for a
        financially sound (defensive) company.
        """
        if self.current_liabilities == 0:
            return float("inf")
        return self.current_assets / self.current_liabilities

    @property
    def working_capital(self) -> float:
        """Current assets minus current liabilities."""
        return self.current_assets - self.current_liabilities
