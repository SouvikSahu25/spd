"""Generate a synthetic retail sales dataset (10,000 rows) for the Power BI dashboard.

Run:  python scripts/generate_data.py
Output: data/sales_data.csv
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 10_000

catalog = {
    "Technology": {"Phones": (300, 0.18), "Laptops": (900, 0.12), "Accessories": (40, 0.30)},
    "Furniture": {"Chairs": (150, 0.10), "Tables": (400, 0.02), "Bookcases": (250, -0.04)},
    "Office Supplies": {"Paper": (20, 0.35), "Binders": (30, 0.25), "Storage": (60, 0.15)},
}
regions = {"North": 0.22, "South": 0.28, "East": 0.25, "West": 0.25}
segments = ["Consumer", "Corporate", "Home Office"]
ship_modes = ["Standard", "Second Class", "First Class", "Same Day"]

rows = []
dates = pd.to_datetime("2023-01-01") + pd.to_timedelta(rng.integers(0, 3 * 365, N), unit="D")
for i in range(N):
    cat = rng.choice(list(catalog))
    sub = rng.choice(list(catalog[cat]))
    base_price, base_margin = catalog[cat][sub]
    qty = int(rng.integers(1, 9))
    discount = float(rng.choice([0, 0, 0, 0.1, 0.2, 0.3]))
    price = base_price * rng.uniform(0.85, 1.15)
    sales = round(price * qty * (1 - discount), 2)
    margin = base_margin - discount * 0.6 + rng.normal(0, 0.04)
    profit = round(sales * margin, 2)
    rows.append({
        "OrderID": f"ORD-{100000 + i}",
        "OrderDate": dates[i].date().isoformat(),
        "ShipMode": rng.choice(ship_modes, p=[0.6, 0.2, 0.15, 0.05]),
        "Segment": rng.choice(segments, p=[0.52, 0.30, 0.18]),
        "Region": rng.choice(list(regions), p=list(regions.values())),
        "Category": cat,
        "SubCategory": sub,
        "Quantity": qty,
        "Discount": discount,
        "Sales": sales,
        "Profit": profit,
    })

df = pd.DataFrame(rows).sort_values("OrderDate").reset_index(drop=True)
df.to_csv("data/sales_data.csv", index=False)
print(df.shape)
print(df.groupby("Category")[["Sales", "Profit"]].sum().round(0))
