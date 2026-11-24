"""
Two chained MapReduce jobs (Hadoop Streaming style):
Job 1 - reduce-side natural join of CUSTOMERS(cust_id, name, city)
and ORDERS(order_id, cust_id, amount)
Job 2 - grouping and aggregation: revenue, order count and maximum order per city
"""
from itertools import groupby

customers = [
    "C1,Kavya,Chennai",
    "C2,Ravi,Bengaluru",
    "C3,Sana,Chennai",
    "C4,Tarun,Hyderabad",
    "C5,Uma,Bengaluru",
]
orders = [
    "O1,C1,2500",
    "O2,C2,1800",
    "O3,C1,700",
    "O4,C3,4200",
    "O5,C4,1500",
    "O6,C2,3100",
    "O7,C5,950",
    "O8,C3,600",
    "O9,C9,800",
]

# ---------------- Job 1: Join ----------------
def join_mapper(source, line):
    f = line.split(",")
    if source == "customers":  # tag each record with its relation
        return f[0], ("C", f[1], f[2])
    return f[1], ("O", f[0], int(f[2]))

def join_reducer(cust_id, values):
    cust = [v for v in values if v[0] == "C"]
    ords = [v for v in values if v[0] == "O"]
    for c in cust:  # inner join: needs both sides
        for o in ords:
            yield cust_id, c[1], c[2], o[1], o[2]

# ---------------- Job 2: Group by city ----------------
def agg_mapper(joined_row):
    _, _, city, _, amount = joined_row
    return city, amount

def agg_reducer(city, amounts):
    return city, sum(amounts), len(amounts), max(amounts)

def shuffle(pairs):
    pairs = sorted(pairs, key=lambda kv: kv[0])
    return [
        (k, [v for _, v in g]) for k, g in groupby(pairs, key=lambda kv: kv[0])
    ]

print("Sales Analytics: Join and Aggregation using MapReduce")
print("=" * 55)

print("\nJOB 1 - MAP (key = cust_id, value tagged with relation):")
mapped = [join_mapper("customers", l) for l in customers] + [
    join_mapper("orders", l) for l in orders
]
for k, v in mapped:
    print(f" {k} -> {v}")

print("\nJOB 1 - SHUFFLE AND SORT:")
groups = shuffle(mapped)
for k, vals in groups:
    print(f" {k}: {vals}")

print("\nJOB 1 - REDUCE (joined records):")
joined = [row for k, vals in groups for row in join_reducer(k, vals)]
print(f" {'cust':<5}{'name':<7}{'city':<11}{'order':<7}amount")
for row in joined:
    print(f" {row[0]:<5}{row[1]:<7}{row[2]:<11}{row[3]:<7}{row[4]}")
print(" Note: order O9 (cust C9) has no matching customer and is dropped.")

print("\nJOB 2 - MAP (key = city, value = amount):")
mapped2 = [agg_mapper(r) for r in joined]
print(" ", mapped2)

print("\nJOB 2 - SHUFFLE AND SORT:")
groups2 = shuffle(mapped2)
for city, vals in groups2:
    print(f" {city}: {vals}")

print("\nJOB 2 - REDUCE (aggregates per city):")
print(f" {'City':<11}{'Revenue':>8}{'Orders':>8}{'Max':>7}{'Avg':>9}")
results = [agg_reducer(c, v) for c, v in groups2]
for city, total, cnt, mx in sorted(results, key=lambda r: -r[1]):
    print(f" {city:<11}{total:>8}{cnt:>8}{mx:>7}{total / cnt:>9.2f}")

print("\nGrand total revenue:", sum(r[1] for r in results))