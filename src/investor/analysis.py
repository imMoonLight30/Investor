"""Analysis of a stock against Benjamin Graham's defensive-investor
criteria from "The Intelligent Investor".

Graham proposed a set of simple, quantitative rules that a defensive
(non-professional) investor could use to screen stocks for adequate
size, financial strength, earnings stability, dividend history,
earnings growth, and a moderate purchase price -- all in the service
of protecting principal while still earning an adequate return.
"""

from dataclasses import dataclass
from typing import List

from .models import Stock


@dataclass
class CriterionResult:
    """The outcome of evaluating a single Graham criterion."""

    name: str
    passed: bool
    detail: str


@dataclass
class AnalysisReport:
    """The full result of analyzing a stock."""

    stock: Stock
    results: List[CriterionResult]

    @property
    def passed_count(self) -> int:
        return sum(1 for result in self.results if result.passed)

    @property
    def total_count(self) -> int:
        return len(self.results)

    @property
    def is_suitable_for_defensive_investor(self) -> bool:
        """True only if every criterion is satisfied.

        Graham was strict: a defensive investor should look for stocks
        that meet all of the criteria, prioritizing safety of principal
        over any single attractive metric.
        """
        return self.passed_count == self.total_count


def _check_adequate_size(stock: Stock, min_annual_sales: float) -> CriterionResult:
    passed = stock.annual_sales >= min_annual_sales
    return CriterionResult(
        name="Adequate size of the enterprise",
        passed=passed,
        detail=(
            f"Annual sales of {stock.annual_sales:,.0f} "
            f"{'meets' if passed else 'is below'} the minimum of "
            f"{min_annual_sales:,.0f}."
        ),
    )


def _check_financial_condition(stock: Stock) -> CriterionResult:
    ratio_ok = stock.current_ratio >= 2.0
    debt_ok = stock.long_term_debt <= stock.working_capital
    passed = ratio_ok and debt_ok
    return CriterionResult(
        name="Sufficiently strong financial condition",
        passed=passed,
        detail=(
            f"Current ratio is {stock.current_ratio:.2f} "
            f"({'>= 2.0' if ratio_ok else '< 2.0'}) and long-term debt "
            f"({stock.long_term_debt:,.0f}) "
            f"{'does not exceed' if debt_ok else 'exceeds'} working capital "
            f"({stock.working_capital:,.0f})."
        ),
    )


def _check_earnings_stability(stock: Stock, min_years: int) -> CriterionResult:
    years = stock.eps_history
    has_enough_years = len(years) >= min_years
    all_positive = bool(years) and all(eps > 0 for eps in years)
    passed = has_enough_years and all_positive
    return CriterionResult(
        name="Earnings stability",
        passed=passed,
        detail=(
            f"Positive earnings in {sum(1 for eps in years if eps > 0)} of "
            f"{len(years)} years on record (minimum required: {min_years})."
        ),
    )


def _check_dividend_record(stock: Stock, min_years: int) -> CriterionResult:
    passed = stock.dividend_years_paid >= min_years
    return CriterionResult(
        name="Uninterrupted dividend record",
        passed=passed,
        detail=(
            f"Dividends paid for {stock.dividend_years_paid} consecutive "
            f"years (minimum required: {min_years})."
        ),
    )


def _check_earnings_growth(stock: Stock, min_growth: float) -> CriterionResult:
    years = stock.eps_history
    if len(years) < 2:
        return CriterionResult(
            name="Earnings growth",
            passed=False,
            detail="Not enough earnings history to evaluate growth.",
        )
    first, last = years[0], years[-1]
    if first <= 0:
        return CriterionResult(
            name="Earnings growth",
            passed=False,
            detail=(
                f"Cannot compute earnings growth because the earliest EPS "
                f"({first:.2f}) is not positive."
            ),
        )
    growth = (last - first) / first
    passed = growth >= min_growth
    return CriterionResult(
        name="Earnings growth",
        passed=passed,
        detail=(
            f"EPS grew {growth * 100:.1f}% from {first:.2f} to {last:.2f} "
            f"(minimum required: {min_growth * 100:.0f}%)."
        ),
    )


def _check_moderate_pe(stock: Stock, max_pe: float) -> CriterionResult:
    passed = 0 < stock.pe_ratio <= max_pe
    return CriterionResult(
        name="Moderate price-to-earnings ratio",
        passed=passed,
        detail=(
            f"P/E ratio is {stock.pe_ratio:.2f} "
            f"({'within' if passed else 'outside'} the maximum of {max_pe:.1f})."
        ),
    )


def _check_moderate_pb(stock: Stock, max_pb: float, max_combined: float) -> CriterionResult:
    pb_ok = 0 < stock.pb_ratio <= max_pb
    combined = stock.pe_ratio * stock.pb_ratio
    combined_ok = 0 < combined <= max_combined
    passed = pb_ok or combined_ok
    return CriterionResult(
        name="Moderate price-to-book ratio",
        passed=passed,
        detail=(
            f"P/B ratio is {stock.pb_ratio:.2f} (max {max_pb:.1f}); "
            f"P/E x P/B is {combined:.2f} (max {max_combined:.1f})."
        ),
    )


def analyze(
    stock: Stock,
    min_annual_sales: float = 500_000_000,
    min_earnings_years: int = 10,
    min_dividend_years: int = 20,
    min_earnings_growth: float = 1.0 / 3.0,
    max_pe: float = 15.0,
    max_pb: float = 1.5,
    max_combined_pe_pb: float = 22.5,
) -> AnalysisReport:
    """Evaluate ``stock`` against Graham's defensive-investor criteria.

    All thresholds have sensible defaults drawn from "The Intelligent
    Investor" but can be overridden to fit different markets or eras.
    """
    results = [
        _check_adequate_size(stock, min_annual_sales),
        _check_financial_condition(stock),
        _check_earnings_stability(stock, min_earnings_years),
        _check_dividend_record(stock, min_dividend_years),
        _check_earnings_growth(stock, min_earnings_growth),
        _check_moderate_pe(stock, max_pe),
        _check_moderate_pb(stock, max_pb, max_combined_pe_pb),
    ]
    return AnalysisReport(stock=stock, results=results)
