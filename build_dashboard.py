import pandas as pd, json
d = pd.read_csv("cleaned_sales.csv")
prods = sorted(d["Product Name"].unique()); pi = {p:i for i,p in enumerate(prods)}
oids = {o:i for i,o in enumerate(d["Order ID"].unique())}
rows = [[int(r.Year), r.Month, r.Region, r.Category, r["Sub-Category"], pi[r["Product Name"]], oids[r["Order ID"]], round(r.Sales,2), round(r.Profit,2), int(r.Quantity)] for _,r in d.iterrows()]
html = open("dashboard_template.html").read().replace("__ROWS__", json.dumps(rows, separators=(",",":"))).replace("__PRODS__", json.dumps(prods))
open("dashboard.html","w").write(html)