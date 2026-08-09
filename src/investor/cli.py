"""Command-line interface for analyzing a stock's fundamentals.

Example:
    python -m investor.cli --symbol KO --name "Coca-Cola" \\
        --annual-sales 4.3e10 --current-assets 3e10 \\
        --current-liabilities 2.5e10 --long-term-debt 3e10 \\
        --eps-history 1.0 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 \\
        --dividend-years-paid 25 --price 60 --pe-ratio 14 --pb-ratio 1.2
"""

import argparse

from .analysis import analyze
from .models import Stock


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Analyze a stock against Benjamin Graham's defensive-investor "
            "criteria for safety of principal and adequate return."
        )
    )
    parser.add_argument("--symbol", required=True, help="Ticker symbol")
    parser.add_argument("--name", required=True, help="Company name")
    parser.add_argument("--annual-sales", type=float, required=True)
    parser.add_argument("--current-assets", type=float, required=True)
    parser.add_argument("--current-liabilities", type=float, required=True)
    parser.add_argument("--long-term-debt", type=float, required=True)
    parser.add_argument(
        "--eps-history",
        type=float,
        nargs="*",
        default=[],
        help="Earnings per share for each year, oldest first",
    )
    parser.add_argument("--dividend-years-paid", type=int, default=0)
    parser.add_argument("--price", type=float, default=0.0)
    parser.add_argument("--pe-ratio", type=float, default=0.0)
    parser.add_argument("--pb-ratio", type=float, default=0.0)
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    stock = Stock(
        symbol=args.symbol,
        name=args.name,
        annual_sales=args.annual_sales,
        current_assets=args.current_assets,
        current_liabilities=args.current_liabilities,
        long_term_debt=args.long_term_debt,
        eps_history=args.eps_history,
        dividend_years_paid=args.dividend_years_paid,
        price=args.price,
        pe_ratio=args.pe_ratio,
        pb_ratio=args.pb_ratio,
    )

    report = analyze(stock)

    print(f"Analysis for {stock.name} ({stock.symbol})")
    print("-" * 60)
    for result in report.results:
        status = "PASS" if result.passed else "FAIL"
        print(f"[{status}] {result.name}: {result.detail}")
    print("-" * 60)
    print(f"{report.passed_count}/{report.total_count} criteria satisfied.")
    if report.is_suitable_for_defensive_investor:
        print("Verdict: Suitable for a defensive investor.")
    else:
        print("Verdict: Not suitable for a defensive investor.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
