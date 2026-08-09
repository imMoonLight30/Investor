# Investor

**Intelligent Investor** &mdash; a small toolkit for stock research inspired by
Benjamin Graham's *The Intelligent Investor*. It helps a defensive investor
manage stock research through simple, quantitative analysis that favors
**safety of principal** and an **adequate, rather than speculative, return**.

## What it does

The `investor` package evaluates a stock's fundamentals against Graham's
classic criteria for a defensive investor:

1. **Adequate size of the enterprise** &mdash; minimum annual sales.
2. **Sufficiently strong financial condition** &mdash; current ratio of at
   least 2, and long-term debt not exceeding working capital.
3. **Earnings stability** &mdash; positive earnings over the trailing years.
4. **Uninterrupted dividend record** &mdash; consecutive years of dividends
   paid.
5. **Earnings growth** &mdash; a minimum increase in earnings per share.
6. **Moderate price-to-earnings ratio**.
7. **Moderate price-to-book ratio** (or a moderate combined P/E &times; P/B).

A stock is deemed suitable for a defensive investor only when it satisfies
all seven criteria, keeping the focus on protecting principal rather than
chasing any single attractive metric.

## Installation

```bash
pip install -e .
```

## Usage

### As a library

```python
from investor import Stock, analyze

stock = Stock(
    symbol="KO",
    name="Coca-Cola",
    annual_sales=43_000_000_000,
    current_assets=30_000_000_000,
    current_liabilities=14_000_000_000,
    long_term_debt=15_000_000_000,
    eps_history=[1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9],
    dividend_years_paid=25,
    price=60,
    pe_ratio=14,
    pb_ratio=1.2,
)

report = analyze(stock)
for result in report.results:
    print(result.name, result.passed, result.detail)

print(report.is_suitable_for_defensive_investor)
```

### From the command line

```bash
investor --symbol KO --name "Coca-Cola" \
  --annual-sales 4.3e10 --current-assets 3e10 \
  --current-liabilities 1.4e10 --long-term-debt 1.5e10 \
  --eps-history 1.0 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 \
  --dividend-years-paid 25 --price 60 --pe-ratio 14 --pb-ratio 1.2
```

## Running the tests

```bash
pip install pytest
python -m pytest
```
