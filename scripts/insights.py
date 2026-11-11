"""Quick pandas cross-check of the numbers the Power BI dashboard should show."""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("data/sales_data.csv", parse_dates=["OrderDate"])
df["Year"] = df["OrderDate"].dt.year

print("Total sales :", round(df.Sales.sum(), 2))
print("Total profit:", round(df.Profit.sum(), 2))
print("Margin %    :", round(df.Profit.sum() / df.Sales.sum() * 100, 2))
print("Orders      :", df.OrderID.nunique())
print("\nBy sub-category:")
sub = df.groupby("SubCategory")[["Sales", "Profit"]].sum()
sub["Margin %"] = (sub.Profit / sub.Sales * 100).round(1)
print(sub.sort_values("Profit").round(0))
print("\nBy region:")
print(df.groupby("Region")[["Sales", "Profit"]].sum().round(0))
print("\nYearly sales / YoY %:")
yr = df.groupby("Year").Sales.sum()
print(pd.concat([yr.round(0), (yr.pct_change() * 100).round(1)], axis=1, keys=["Sales", "YoY %"]))
print("\nProfit by discount level:")
print(df.groupby("Discount")[["Sales", "Profit"]].sum().assign(margin=lambda d: (d.Profit / d.Sales * 100).round(1)).round(0))

fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
sub.sort_values("Profit")["Profit"].plot.barh(ax=ax[0], color=["#d62728" if v < 0 else "#2ca02c" for v in sub.sort_values("Profit")["Profit"]])
ax[0].set_title("Profit by Sub-Category")
df.set_index("OrderDate").resample("ME").Sales.sum().plot(ax=ax[1], color="#1f77b4")
ax[1].set_title("Monthly Sales")
plt.tight_layout()
plt.savefig("images/insights_preview.png", dpi=120)
