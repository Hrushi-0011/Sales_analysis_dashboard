# Sales Data Analysis & Business Insights Dashboard

**Dataset:** Superstore US sales, 4 years (2015–2018), 9,994 order lines, 5,009 orders, 1,850 products.
**Tools:** Python (pandas) for cleaning/EDA; Chart.js interactive HTML dashboard (filters: year, region, category).

## Files
| File | Purpose |
|---|---|
| raw_superstore.csv | Original raw file |
| analysis.py | Cleaning + EDA |
| cleaning_log.txt | Documented cleaning steps |
| cleaned_sales.csv | Final clean dataset (+ Year, Month, Profit Margin %, Returned, Ship Days) |
| build_dashboard.py / dashboard.html | Builds the interactive dashboard |

## Cleaning summary
1. 806 rows were other sheets (Returns, People) pasted under the orders -> separated; 296 returned Order IDs kept as a `Returned` flag.
2. Duplicates: 0 in real sales rows .
3. Types: dates -> datetime; numerics fixed; Postal Code -> 5-char text.
4. Missing: 11 Postal Codes filled with 05401.
5. Invalid values (sales/qty <= 0, discount outside 0–1, ship before order): None. Negative profit is kept.
6. Text consistency: trimmed; no category/region spelling variants.

## KPIs
Sales $2,297,201 ·
 Profit $286,397 ·
  Margin 12.5% · 
  Orders 5,009 · 
  Quantity 37,873

## Top 5 insights
1. Furniture: 32% of sales but only 2.5% margin vs ~17% for Technology/Office Supplies.
2. Discounts >20% lost $135K; Undiscounted lines earned $321K. Tables lost $17.7K on $207K sales.
3. Central region: 7.9% margin vs 14.9% West; average discount 24% vs 11%.
4. Seasonality: Sep, Nov, Dec, Mar = 52% of sales; Nov peak $352K. Growth +29.5% (2017), +20.4% (2018).
5. Copiers: $55.6K profit at 37% margin on 234 units; 301 of 1,850 products lose money.


