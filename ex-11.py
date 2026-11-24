print("Pharmacy Inventory Management: Lists and Tuples")
print("=" * 50)

# ---------- Tuples: fixed product records (immutable) ----------
# (product_code, name, unit_price)
products = (
    ("P101", "Paracetamol", 25.0),
    ("P102", "Amoxicillin", 120.0),
    ("P103", "Cetirizine", 40.0),
    ("P104", "Vitamin D3", 210.0),
    ("P105", "Insulin", 450.0),
)

print("\nProduct catalogue (tuple of tuples):")
for code, name, price in products:  # tuple unpacking
    print(f" {code} {name:<12} Rs.{price:>7.2f}")

print("Number of products :", len(products))
print("Second product :", products[1])
print("Codes (slice) :", tuple(p[0] for p in products[:3]))
print(
    "Count / index :",
    products.count(products[0]),
    "/",
    products.index(("P103", "Cetirizine", 40.0)),
)

try:
    products[0][2] = 30.0
except TypeError as e:
    print("Attempt to change a tuple ->", "TypeError:", e)

# ---------- Lists: stock that changes every day ----------
stock = [120, 35, 80, 15, 8]
print("\nInitial stock list :", stock)
stock[3] += 50  # update by index
print("After restocking P104 (+50):", stock)

sold_today = [20, 10, 5, 12, 3]
stock = [s - d for s, d in zip(stock, sold_today)]  # list comprehension
print("After today's sales:", stock)

expiring = ["Amoxicillin", "Insulin"]
expiring.append("Cetirizine")
expiring.extend(["Paracetamol"])
expiring.insert(0, "Vitamin D3")
print("\nExpiring list after append/extend/insert:", expiring)

expiring.remove("Paracetamol")
last = expiring.pop()
print("After remove('Paracetamol') and pop() ->", expiring, "| popped:", last)

expiring.sort()
print("Sorted :", expiring)
expiring.reverse()
print("Reversed :", expiring)

# ---------- Combining lists and tuples ----------
inventory = [
    (code, name, price, qty) for (code, name, price), qty in zip(products, stock)
]
reorder = [name for _, name, _, qty in inventory if qty < 30]
value = [round(price * qty, 2) for _, _, price, qty in inventory]

print("\nInventory records (list of tuples):")
for item, v in zip(inventory, value):
    print(f" {item} stock value = Rs.{v:,.2f}")

print("Items to reorder (qty < 30):", reorder)
print("Total stock value : Rs.{:,.2f}".format(sum(value)))
print("Max / Min quantity :", max(stock), "/", min(stock))

by_value = sorted(inventory, key=lambda t: t[2] * t[3], reverse=True)
print("Highest value item :", by_value[0][1])

# ---------- Nested list as a weekly sales matrix ----------
weekly = [[20, 10, 5, 12, 3], [18, 8, 7, 10, 2], [25, 12, 6, 9, 4]]
totals = [sum(day[i] for day in weekly) for i in range(len(products))]
print("\nWeekly sales matrix (3 days x 5 products):", weekly)
print("Units sold per product:", dict(zip([p[1] for p in products], totals)))

copy_list = stock.copy()
copy_list.clear()
print("Copied then cleared list:", copy_list, "| original stock still:", stock)