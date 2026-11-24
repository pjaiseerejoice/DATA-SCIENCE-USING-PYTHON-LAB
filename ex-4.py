import numpy as np 
import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler

np.random.seed(42) 
n = 200
df = pd.DataFrame(
{
"customer_id": range(1001, 1001 + n),
"age": np.random.randint(18, 70, n).astype(float), "income": np.random.normal(45000, 12000, n).round(), "city": np.random.choice(
["Chennai", "chennai ", "Madurai", "Coimbatore"], n
),
"purchases": np.random.poisson(6, n).astype(float), "churn": np.random.choice(["Yes", "No"], n, p=[0.3, 0.7]),
}
)
# Inject typical data-quality problems 
df.loc[np.random.choice(n, 15, replace=False), "age"] = np.nan 
df.loc[np.random.choice(n, 10, replace=False), "income"] = np.nan
df.loc[[5, 50, 120], "income"] = [450000, 520000, -3000] # outliers / invalid 
df = pd.concat(
[df, df.iloc[[10, 20, 30, 40, 50]]], ignore_index=True
) # duplicates

print("Customer Data: Cleaning and Sampling for Modeling") 
print("=" * 50)
print("Raw shape:", df.shape)

# ---------- 1. Missing values ----------
print("\n[1] Missing values per column:") 
print(df.isnull().sum().to_string())

#	2. Duplicates 
dups = df.duplicated().sum() 
df = df.drop_duplicates()
print(f"\n[2] Duplicate rows removed: {dups} -> shape {df.shape}")

# ---------- 3. Inconsistent categories  ----------
print("\n[3] City values before:", sorted(df["city"].unique())) 
df["city"] = df["city"].str.strip().str.title()
print("	City values after :", sorted(df["city"].unique()))

# ---------- 4. Invalid values and outliers (IQR rule) ----------
df.loc[df["income"] < 0, "income"] = np.nan
q1, q3 = df["income"].quantile([0.25, 0.75]) 
iqr = q3 - q1
low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
outliers = df[(df["income"] < low) | (df["income"] > high)] 
print(f"\n[4] Income IQR bounds: {low:.0f} to {high:.0f}") 
print("	Outliers found:", len(outliers)) 
print(outliers[["customer_id", "income"]].to_string(index=False)) 
df["income"] = df["income"].clip(low, high)

#	5. Imputation
df["age"] = df["age"].fillna(df["age"].median())
df["income"] = df["income"].fillna(df["income"].mean()).round()
print("\n[5] Missing values after imputation:", int(df.isnull().sum().sum()))

# ---------- 6. Encoding and scaling ----------
df["churn"] = df["churn"].map({"No": 0, "Yes": 1})
df = pd.get_dummies(df, columns=["city"], drop_first=True, dtype=int) 
scaler = StandardScaler()
df[["age", "income", "purchases"]] = scaler.fit_transform(
 
df[["age", "income", "purchases"]]
)
print("\n[6] Cleaned and transformed data (first 5 rows):") 
print(df.head().round(3).to_string(index=False))

#	7. Sampling
X = df.drop(columns=["customer_id", "churn"]) 
y = df["churn"]
simple = df.sample(frac=0.2, random_state=1) 
print(
"\n[7] Simple random sample (20%):", len(simple),
"rows, churn rate =", round(simple["churn"].mean(), 3),
)

X_train, X_temp, y_train, y_temp = train_test_split( X, y, test_size=0.3, stratify=y, random_state=1
)
X_val, X_test, y_val, y_test = train_test_split(
X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=1
)
print("\nStratified Train / Validation / Test split (70/15/15):") 
for name, part in [
("Overall", y),
("Train", y_train), ("Validation", y_val), ("Test", y_test),
]:
 print(f" {name:<11} rows = {len(part):>3}	churn rate = {part.mean():.3f}")
