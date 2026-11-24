import array
import re
import numpy as np

reviews = [
    "  Excellent product! Battery life is GREAT and delivery was fast.  ",
    "Poor quality. The battery drained in 2 hours. Very disappointed!!",
    "Good value for money, but the charger is slow.",
    "Delivery was late; product is average. Contact: support@shopmart.in",
    "Great camera, great display, great price!",
]

print("Customer Review and Sensor Analytics: Strings and Arrays")
print("=" * 58)

# ---------- Part A: String operations ----------
r = reviews[0]
print("\nPart A - String operations on review 1")
print("  Original          :", repr(r))
print("  strip()           :", r.strip())
print("  lower()           :", r.strip().lower())
print("  upper()           :", r.strip().upper())
print("  Length            :", len(r.strip()))
print("  Slice [0:17]      :", r.strip()[0:17])
print("  Reverse [::-1]    :", r.strip()[::-1][:25], "...")
print("  find('Battery')   :", r.strip().find("Battery"))
print("  count('a')        :", r.lower().count("a"))
print("  replace           :", r.strip().replace("GREAT", "good"))
print("  split()           :", r.strip().split()[:5], "...")
print("  startswith('Exc') :", r.strip().startswith("Exc"))

positive = {"excellent", "great", "good", "fast"}
negative = {"poor", "disappointed", "slow", "late", "drained"}

print("\nSentiment of each review:")
for i, text in enumerate(reviews, 1):
    words = re.findall(r"[a-z]+", text.lower())
    score = sum(w in positive for w in words) - sum(w in negative for w in words)
    label = "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"
    print(f"  Review {i}: words={len(words):>2}  score={score:>2}  -> {label}")

emails = re.findall(r"[\w.]+@[\w.]+", " ".join(reviews))
print("\nEmail extracted with regex:", emails)
print("Joined keywords :", " | ".join(sorted(positive)))
print("Formatted string: {:<10}|{:^10}|{:>10}".format("left", "centre", "right"))

# ---------- Part B: Arrays ----------
print("\nPart B - Arrays of temperature sensor readings")
temps = array.array("f", [31.5, 32.0, 33.8, 35.2, 34.1, 30.9, 36.4])
print("  array module      :", temps.tolist())
temps.append(37.0)
temps.insert(0, 30.2)
print("  after append/insert:", [round(t, 1) for t in temps])
print(
    "  index of max      :",
    temps.index(max(temps)),
    "| typecode:",
    temps.typecode,
)

week = np.array(
    [
        [31.5, 32.0, 33.8, 35.2, 34.1, 30.9, 36.4],
        [29.8, 30.5, 31.2, 33.0, 32.7, 29.5, 34.0],
        [33.1, 34.2, 35.6, 37.1, 36.0, 32.8, 38.2],
    ]
)
print("\n  NumPy 2-D array (3 sensors x 7 days):")
print(week)
print("  shape, ndim, size :", week.shape, week.ndim, week.size)
print("  Sensor means      :", week.mean(axis=1).round(2))
print("  Daily maximum     :", week.max(axis=0))
print("  Readings > 35     :", week[week > 35])
print("  Sensor 2, days 2-4:", week[1, 1:4])
print("  In Fahrenheit (vectorised):")
print((week * 9 / 5 + 32).round(1))
print("  Reshape to 7x3    :", week.reshape(7, 3).shape)
print("  Sorted sensor 1   :", np.sort(week[0]))