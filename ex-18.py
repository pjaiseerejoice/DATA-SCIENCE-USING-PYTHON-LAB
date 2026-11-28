
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(11)

departments = [
    "Cardiology",
    "Orthopaedics",
    "Neurology",
    "Paediatrics",
    "General",
]

budget_share = [28, 18, 22, 12, 20]
patients_2025 = [820, 640, 410, 930, 1500]
patients_2026 = [910, 700, 455, 880, 1620]

wait = {
    d: np.random.gamma(shape=k, scale=6, size=120)
    for d, k in zip(departments, [3, 2.5, 4, 1.8, 5])
}

ages = np.concatenate([
    np.random.normal(8, 4, 300),
    np.random.normal(45, 12, 700),
    np.random.normal(70, 8, 300),
])

ages = ages[(ages > 0) & (ages < 100)]

print("Hospital Operations Dashboard: Choosing the Right Graph")
print("=" * 56)

print("\nBudget share (%) :", dict(zip(departments, budget_share)))

print("Patients 2025 vs 2026 :")

for d, a, b in zip(departments, patients_2025, patients_2026):
    print(
        f" {d:<13} {a:>5} {b:>5} "
        f"change = {100 * (b - a) / a:+.1f}%"
    )

print(
    "\nPatient age: n = {}, mean = {:.1f}, median = {:.1f}, std = {:.1f}".format(
        len(ages),
        ages.mean(),
        np.median(ages),
        ages.std()
    )
)

print("\nWaiting time (minutes) summary by department:")

summary = (
    pd.DataFrame(wait)
    .describe()
    .T[["mean", "25%", "50%", "75%", "max"]]
    .round(1)
)

print(summary.to_string())

# Create dashboard with 4 subplots
fig, ax = plt.subplots(2, 2, figsize=(12, 9))

# 1. Parts of a Whole -> Pie Chart

explode = [
    0.08 if s == max(budget_share) else 0
    for s in budget_share
]

ax[0, 0].pie(
    budget_share,
    labels=departments,
    autopct="%1.0f%%",
    startangle=90,
    explode=explode,
    shadow=True,
)

ax[0, 0].set_title("Parts of a Whole: Budget Share")

# 2. Comparisons -> Grouped Bar Chart

x = np.arange(len(departments))
w = 0.38

b1 = ax[0, 1].bar(
    x - w / 2,
    patients_2025,
    w,
    label="2025",
    color="#5b8fd1"
)

b2 = ax[0, 1].bar(
    x + w / 2,
    patients_2026,
    w,
    label="2026",
    color="#f28e2b"
)

ax[0, 1].bar_label(b2, fontsize=8)
ax[0, 1].set_xticks(x, departments, rotation=20)
ax[0, 1].set_ylabel("Patients")
ax[0, 1].legend()
ax[0, 1].set_title("Comparison: Patients per Department")

# 3. Distribution -> Histogram

ax[1, 0].hist(
    ages,
    bins=25,
    color="#59a14f",
    edgecolor="white"
)

ax[1, 0].axvline(
    ages.mean(),
    color="red",
    linestyle="--",
    label=f"Mean = {ages.mean():.1f}"
)

ax[1, 0].set_xlabel("Age (years)")
ax[1, 0].set_ylabel("Number of patients")
ax[1, 0].set_title("Distribution: Patient Age")
ax[1, 0].legend()

# 4. Groups -> Box Plot

ax[1, 1].boxplot(
    wait.values(),
    labels=[d[:5] for d in departments],
    patch_artist=True,
    boxprops=dict(facecolor="#edc948"),
)

ax[1, 1].set_ylabel("Waiting time (minutes)")
ax[1, 1].set_title("Groups: Waiting Time by Department")

plt.tight_layout()
plt.savefig("exp18_dashboard.png", dpi=150)
plt.show()

# Horizontal Bar Ranked View

fig, ax = plt.subplots(figsize=(7, 3.5))

order = np.argsort(patients_2026)

ax.barh(
    np.array(departments)[order],
    np.array(patients_2026)[order],
    color="#76b7b2"
)

ax.set_xlabel("Patients in 2026")
ax.set_title("Ranked Comparison (Horizontal Bar)")

plt.tight_layout()
plt.savefig("exp18_barh.png", dpi=150)

plt.show()

print("\nSaved figures: exp18_dashboard.png, exp18_barh.png")
