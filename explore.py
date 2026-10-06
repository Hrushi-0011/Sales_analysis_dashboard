import pandas as pd
df = pd.read_csv("raw_superstore.csv", encoding="latin1")
print(df.shape)
print(df.isna().sum())
print(df.duplicated().sum())