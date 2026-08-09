from investor import Stock, analyze
from investor.models import Stock as ModelStock


def make_strong_stock() -> Stock:
    """A stock that satisfies every defensive-investor criterion."""
    return Stock(
        symbol="STRONG",
        name="Strong Co",
        annual_sales=1_000_000_000,
        current_assets=300_000_000,
        current_liabilities=100_000_000,
        long_term_debt=50_000_000,
        eps_history=[1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9],
        dividend_years_paid=25,
        price=20.0,
        pe_ratio=12.0,
        pb_ratio=1.2,
    )


def make_weak_stock() -> Stock:
    """A stock that fails every defensive-investor criterion."""
    return Stock(
        symbol="WEAK",
        name="Weak Co",
        annual_sales=1_000_000,
        current_assets=10,
        current_liabilities=100,
        long_term_debt=1_000_000,
        eps_history=[-1.0, -2.0],
        dividend_years_paid=0,
        price=100.0,
        pe_ratio=50.0,
        pb_ratio=5.0,
    )


def test_current_ratio_and_working_capital():
    stock = make_strong_stock()
    assert stock.current_ratio == 3.0
    assert stock.working_capital == 200_000_000


def test_current_ratio_handles_zero_liabilities():
    stock = ModelStock(
        symbol="X",
        name="X Co",
        annual_sales=1,
        current_assets=1,
        current_liabilities=0,
        long_term_debt=0,
    )
    assert stock.current_ratio == float("inf")


def test_strong_stock_passes_all_criteria():
    report = analyze(make_strong_stock())
    assert report.is_suitable_for_defensive_investor
    assert report.passed_count == report.total_count == 7
    assert all(result.passed for result in report.results)


def test_weak_stock_fails_all_criteria():
    report = analyze(make_weak_stock())
    assert not report.is_suitable_for_defensive_investor
    assert report.passed_count == 0


def test_adequate_size_threshold_is_configurable():
    stock = make_strong_stock()
    report = analyze(stock, min_annual_sales=2_000_000_000)
    size_result = next(r for r in report.results if r.name == "Adequate size of the enterprise")
    assert not size_result.passed


def test_financial_condition_requires_ratio_and_debt_coverage():
    stock = make_strong_stock()
    stock.long_term_debt = 250_000_000  # exceeds working capital of 200M
    report = analyze(stock)
    result = next(
        r for r in report.results if r.name == "Sufficiently strong financial condition"
    )
    assert not result.passed


def test_earnings_growth_requires_enough_history():
    stock = make_strong_stock()
    stock.eps_history = [1.0]
    report = analyze(stock)
    result = next(r for r in report.results if r.name == "Earnings growth")
    assert not result.passed


def test_earnings_growth_handles_non_positive_starting_eps():
    stock = make_strong_stock()
    stock.eps_history = [-1.0, 2.0]
    report = analyze(stock)
    result = next(r for r in report.results if r.name == "Earnings growth")
    assert not result.passed
    assert "not positive" in result.detail


def test_moderate_pb_allows_combined_pe_pb_rule():
    stock = make_strong_stock()
    # Fails the strict P/B <= 1.5 rule but passes via the P/E x P/B <= 22.5 rule.
    stock.pe_ratio = 10.0
    stock.pb_ratio = 2.0
    report = analyze(stock)
    result = next(r for r in report.results if r.name == "Moderate price-to-book ratio")
    assert result.passed
