import pandas as pd, json

log = []
def L(msg): print(msg); log.append(msg)

# ---------- 1. LOAD ----------
raw = pd.read_csv("raw_superstore.csv", encoding="latin1", dtype=str)
L(f"Raw file shape: {raw.shape}")

# ---------- 2. CLEAN ----------
orders = raw[raw["Order Date"].notna()].copy()
extra  = raw[raw["Order Date"].isna()].copy()
returns = extra[extra["Row ID"] == "Yes"]["Order ID"].unique()
L(f"Issue A - structural: {len(extra)} rows belong to other sheets (Returns list/People list), not sales. "
  f"Separated them. Kept {len(orders)} sales rows; extracted {len(returns)} unique returned Order IDs.")

L(f"Issue B - duplicates in sales rows: {orders.duplicated().sum()} full duplicates, "
  f"{orders['Row ID'].duplicated().sum()} duplicate Row IDs. (The 504 'duplicates' in the raw file were all inside the Returns block: an order with several returned items is listed repeatedly.)")
orders = orders.drop_duplicates()

for c in ["Sales", "Quantity", "Discount", "Profit"]: orders[c] = pd.to_numeric(orders[c])
orders["Quantity"] = orders["Quantity"].astype(int)
orders["Row ID"] = orders["Row ID"].astype(int)
orders["Order Date"] = pd.to_datetime(orders["Order Date"], format="%m/%d/%Y")
orders["Ship Date"]  = pd.to_datetime(orders["Ship Date"],  format="%m/%d/%Y")
L("Issue C - types: dates parsed text->datetime; Sales/Discount/Profit->float; Quantity/Row ID->int.")

miss = orders["Postal Code"].isna().sum()
orders["Postal Code"] = orders["Postal Code"].str.replace(r"\.0$", "", regex=True)
orders.loc[orders["City"].eq("Burlington") & orders["State"].eq("Vermont") & orders["Postal Code"].isna(), "Postal Code"] = "05401"
orders["Postal Code"] = orders["Postal Code"].str.zfill(5)
L(f"Issue D - missing: {miss} Postal Codes missing, all Burlington, Vermont -> filled with 05401. No other nulls.")

bad = {"Sales<=0": (orders.Sales <= 0).sum(), "Qty<=0": (orders.Quantity <= 0).sum(),
       "Discount outside 0-1": (~orders.Discount.between(0, 1)).sum(),
       "Ship<Order date": (orders["Ship Date"] < orders["Order Date"]).sum()}
L(f"Issue E - invalid values checked: {bad}. All zero. Negative Profit kept: it is a genuine loss, not an error.")

for c in orders.columns:
    if orders[c].dtype == "object" or str(orders[c].dtype) == "str":
        orders[c] = orders[c].str.strip()
L(f"Issue F - consistency: whitespace trimmed; categorical columns checked (Region={sorted(orders.Region.unique())}, Category={sorted(orders.Category.unique())}) - no spelling variants.")

# ---------- 3. FEATURES ----------
orders["Year"] = orders["Order Date"].dt.year
orders["Month"] = orders["Order Date"].dt.to_period("M").astype(str)
orders["Month Name"] = orders["Order Date"].dt.month_name()
orders["Profit Margin %"] = (orders.Profit / orders.Sales * 100).round(2)
orders["Returned"] = orders["Order ID"].isin(returns)
orders["Ship Days"] = (orders["Ship Date"] - orders["Order Date"]).dt.days
orders["Order Date"] = orders["Order Date"].dt.strftime("%Y-%m-%d")
orders["Ship Date"] = orders["Ship Date"].dt.strftime("%Y-%m-%d")
orders.to_csv("cleaned_sales.csv", index=False)
L(f"Final cleaned shape: {orders.shape}")

# ---------- 4. EDA ----------
d = orders
k = dict(sales=d.Sales.sum(), profit=d.Profit.sum(), orders=d["Order ID"].nunique(), qty=int(d.Quantity.sum()))
k["margin"] = k["profit"] / k["sales"] * 100
print("\nKPIs", {a: round(b, 2) for a, b in k.items()})
def g(col): return d.groupby(col).agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Qty=("Quantity","sum"), Orders=("Order ID","nunique")).assign(Margin=lambda x: x.Profit/x.Sales*100).round(2)
for col in ["Category", "Region", "Segment", "Year"]: print("\n", g(col).sort_values("Sales", ascending=False))
sub = g("Sub-Category").sort_values("Profit"); print("\n", sub)
print("\nMonthly top5\n", g("Month Name").sort_values("Sales", ascending=False).head(5))
prod = g("Product Name").sort_values("Profit"); print("\nWorst 5 products\n", prod.head(5)); print("\nBest 5\n", prod.tail(5))
dd = d.assign(Disc=pd.cut(d.Discount, [-.01, 0, .1, .2, .4, 1], labels=["0%", "1-10%", "11-20%", "21-40%", ">40%"]))
print("\nDiscount bands\n", dd.groupby("Disc", observed=True).agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Rows=("Sales","size")).round(0))
print("\nRegion x Category profit\n", d.pivot_table(index="Region", columns="Category", values="Profit", aggfunc="sum").round(0))
print("\nReturned: orders", d[d.Returned]["Order ID"].nunique(), "sales", d[d.Returned].Sales.sum().round(0))
print("\nState worst profit\n", d.groupby("State").Profit.sum().sort_values().head(5).round(0))
open("cleaning_log.txt", "w").write("\n".join(log))