import csv 
import json 
import os
import pandas as pd 
os.makedirs("data", exist_ok=True)
# ---------- Step 1: Data collection from three different sources ----------# Source 1: CSV file exported from the in-store billing (POS) system 
pos_rows = [
["order_id", "customer", "product", "qty", "unit_price", "branch"], [101, "Anitha", "Laptop", 1, 54000, "Chennai"],
[102, "Rahul", "Mouse", 3, 450, "Chennai"],
[103, "Priya", "Keyboard", 2, 1200, "Chennai"],
[104, "Karthik", "Monitor", 1, 9500, "Chennai"],
]
with open("data/pos_orders.csv", "w", newline="") as f: csv.writer(f).writerows(pos_rows)

# Source 2: JSON response from the online store (web API) 
web_orders = [
{
"order_id": 201, "customer": "Divya",
"product": "Laptop", "qty": 2,
"unit_price": 52500, "branch": "Online",
},
{
"order_id": 202, "customer": "Arjun", "product": "Headset", "qty": 1,
"unit_price": 2300, "branch": "Online",
},
{
"order_id": 203, "customer": "Meena",
"product": "Mouse", "qty": 5,
"unit_price": 430, "branch": "Online",
},
]
with open("data/web_orders.json", "w") as f: json.dump(web_orders, f, indent=2)

# Source 3: Plain-text log written by the mobile app (pipe separated) 
log_lines = [
"301|Suresh|Monitor|2|9300|Mobile", "302|Lakshmi|Keyboard|1|1150|Mobile", "303|Vignesh|Laptop|1|55000|Mobile",
]
with open("data/mobile_orders.txt", "w") as f: f.write("\n".join(log_lines))

print("Retail Order Data: Collection, Storage and Retrieval") 
print("=" * 55)

# ---------- Step 2: Reading the data back from each file ----------
df_pos = pd.read_csv("data/pos_orders.csv")
print("\n[1] CSV source -> rows:", len(df_pos))
print(df_pos.to_string(index=False))

with open("data/web_orders.json") as f:
 
 df_web = pd.DataFrame(json.load(f)) 
print("\n[2] JSON source -> rows:", len(df_web)) 
print(df_web.to_string(index=False))

cols = ["order_id", "customer", "product", "qty", "unit_price", "branch"]
df_mob = pd.read_csv("data/mobile_orders.txt", sep="|", header=None, names=cols) 
print("\n[3] TXT source -> rows:", len(df_mob)) 
print(df_mob.to_string(index=False))

# ---------- Step 3: Integration into a single dataset ----------
orders = pd.concat([df_pos, df_web, df_mob], ignore_index=True) 
orders["amount"] = orders["qty"] * orders["unit_price"]
print("\n--- Integrated Dataset ---") 
print(orders.to_string(index=False)) 
print("\nShape		:", orders.shape) 
print("Data types	:") 
print(orders.dtypes.to_string())

# ---------- Step 4: Storage in different formats ----------
orders.to_csv("data/all_orders.csv", index=False) 
orders.to_json("data/all_orders.json", orient="records", indent=2) 
orders.to_excel("data/all_orders.xlsx", index=False) 
print("\nFiles stored :")
for name in ["all_orders.csv", "all_orders.json", "all_orders.xlsx"]: print(f" data/{name:<16} {os.path.getsize('data/' + name):>6} bytes")

# ---------- Step 5: Retrieval and a quick query ----------
back = pd.read_excel("data/all_orders.xlsx") 
print("\nRetrieved from Excel, rows:", len(back)) 
print("\nRevenue by branch:")
print(
back.groupby("branch")["amount"]
.sum()
.sort_values(ascending=False)
.to_string()
)
print("\nOrders with amount > 10000:")
print(
back.loc[
back["amount"] > 10000, ["order_id", "customer", "product", "amount"]
].to_string(index=False)
)

