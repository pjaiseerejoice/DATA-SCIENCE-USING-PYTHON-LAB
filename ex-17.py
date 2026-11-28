
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

np.random.seed(1)

months = pd.date_range("2025-01-01", periods=24, freq="MS")
t = np.arange(24)

sales = pd.DataFrame(
    {
        "Electronics": (
            120 + 4.0 * t
            + 15 * np.sin(2 * np.pi * t / 12)
            + np.random.normal(0, 5, 24)
        ),
        "Clothing": (
            90 + 1.5 * t
            + 25 * np.sin(2 * np.pi * (t - 3) / 12)
            + np.random.normal(0, 5, 24)
        ),
        "Groceries": (
            150 + 0.8 * t
            + np.random.normal(0, 4, 24)
        ),
    },
    index=months,
).round(1)

print("Monthly Sales Trend Analysis using Line Plots")
print("=" * 46)

print(sales.head(6).to_string())
print("...")

print("\nYearly totals (Rs. lakhs):")
print(sales.groupby(sales.index.year).sum().round(1).to_string())

peak = sales["Electronics"].idxmax()

print(
    f"\nPeak Electronics month: "
    f"{peak:%b %Y} ({sales['Electronics'].max()} lakhs)"
)

# Trend line for Electronics using least squares
slope, intercept = np.polyfit(t, sales["Electronics"], 1)

print(
    f"Electronics trend line: "
    f"sales = {intercept:.2f} + {slope:.2f} * month_index"
)

# 3-month moving average
rolling = sales["Electronics"].rolling(3).mean()

# ---------- Figure 1: Formatted multi-line chart ----------

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(
    sales.index,
    sales["Electronics"],
    color="tab:blue",
    linestyle="-",
    linewidth=2,
    marker="o",
    markersize=5,
    label="Electronics",
)

ax.plot(
    sales.index,
    sales["Clothing"],
    color="tab:orange",
    linestyle="--",
    linewidth=2,
    marker="s",
    markersize=5,
    label="Clothing",
)

ax.plot(
    sales.index,
    sales["Groceries"],
    color="tab:green",
    linestyle=":",
    linewidth=2.5,
    marker="^",
    markersize=5,
    label="Groceries",
)

ax.plot(
    sales.index,
    intercept + slope * t,
    color="black",
    linestyle="-.",
    linewidth=1,
    label="Electronics trend",
)

ax.set_title(
    "Monthly Sales by Category (2025-2026)",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Month")
ax.set_ylabel("Sales (Rs. lakhs)")

ax.set_ylim(40, 260)
ax.set_yticks(range(40, 261, 20))

ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))

ax.grid(True, which="major", linestyle="--", alpha=0.5)

ax.annotate(
    f"Peak: {sales['Electronics'].max()}",
    xy=(peak, sales["Electronics"].max()),
    xytext=(peak - pd.Timedelta(days=200), 245),
    arrowprops=dict(arrowstyle="->", color="red"),
    color="red",
)

ax.text(
    months[1],
    55,
    "Clothing peaks every summer",
    fontsize=9,
    style="italic"
)

ax.legend(loc="upper left", ncol=2, frameon=True)

plt.tight_layout()
plt.savefig("exp17_line.png", dpi=150)

# ---------- Figure 2: Subplots with time-series smoothing ----------

fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

# Electronics monthly sales and moving average
axes[0].plot(
    sales.index,
    sales["Electronics"],
    label="Monthly",
    alpha=0.6
)

axes[0].plot(
    sales.index,
    rolling,
    color="red",
    linewidth=2,
    label="3-month moving average"
)

axes[0].set_title("Electronics: Smoothing a Time Series")
axes[0].legend()
axes[0].grid(alpha=0.4)

# Groceries month-on-month growth
growth = sales.pct_change().mul(100)

axes[1].bar(
    sales.index,
    growth["Groceries"],
    width=20,
    color="tab:green"
)

axes[1].axhline(0, color="black", linewidth=0.8)

axes[1].set_title("Groceries: Month-on-Month Growth (%)")
axes[1].set_ylabel("Growth (%)")
axes[1].grid(alpha=0.4)

axes[1].xaxis.set_major_formatter(
    mdates.DateFormatter("%b-%y")
)

plt.tight_layout()
plt.savefig("exp17_timeseries.png", dpi=150)

plt.show()

print("\nSaved figures: exp17_line.png, exp17_timeseries.png")
