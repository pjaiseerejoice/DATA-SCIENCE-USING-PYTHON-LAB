import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

np.random.seed(5)

centres = [(25, 80), (55, 20), (85, 85), (55, 50), (25, 20)]
rows = []
for i, (inc, score) in enumerate(centres):
    for _ in range(40):
        rows.append([np.random.normal(inc, 7), np.random.normal(score, 7)])

customers = pd.DataFrame(
    np.round(rows, 1), columns=["annual_income_k", "spending_score"]
)
customers.insert(0, "customer_id", range(1, len(customers) + 1))

print("Mall Customer Segmentation using K-Means Clustering")
print("=" * 52)
print(customers.head().to_string(index=False))
print("Total customers:", len(customers))

X = StandardScaler().fit_transform(
    customers[["annual_income_k", "spending_score"]]
)

# ---------- Choosing k: elbow (WCSS) and silhouette ----------
print("\n k WCSS Silhouette")
wcss, sil = [], []
for k in range(2, 9):
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    wcss.append(km.inertia_)
    sil.append(silhouette_score(X, km.labels_))
    print(f"{k:>2} {km.inertia_:>8.2f} {sil[-1]:.4f}")

best_k = range(2, 9)[int(np.argmax(sil))]
print("\nBest k by silhouette score:", best_k)

# ---------- Final model ----------
km = KMeans(n_clusters=best_k, n_init=10, random_state=0).fit(X)
customers["cluster"] = km.labels_

profile = (
    customers.groupby("cluster")[["annual_income_k", "spending_score"]]
    .mean()
    .round(1)
)
profile["size"] = customers["cluster"].value_counts().sort_index()

def describe(row):
    inc = (
        "High income"
        if row.annual_income_k > 70
        else "Low income" if row.annual_income_k < 40 else "Mid income"
    )
    sp = (
        "high spender"
        if row.spending_score > 65
        else "low spender" if row.spending_score < 35 else "average spender"
    )
    return f"{inc}, {sp}"

profile["segment"] = profile.apply(describe, axis=1)
print("\nCluster profiles:")
print(profile.to_string())

fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
ax[0].plot(range(2, 9), wcss, "o-")
ax[0].set_xlabel("Number of clusters k")
ax[0].set_ylabel("WCSS (inertia)")
ax[0].set_title("Elbow Method")

sc = ax[1].scatter(
    customers["annual_income_k"],
    customers["spending_score"],
    c=customers["cluster"],
    cmap="tab10",
    s=20,
)
centres = customers.groupby("cluster")[
    ["annual_income_k", "spending_score"]
].mean()
ax[1].scatter(
    centres.iloc[:, 0],
    centres.iloc[:, 1],
    c="black",
    marker="X",
    s=150,
    label="Centroids",
)
ax[1].set_xlabel("Annual income (k Rs.)")
ax[1].set_ylabel("Spending score")
ax[1].set_title(f"Customer Segments (k = {best_k})")
ax[1].legend()
plt.tight_layout()
plt.savefig("exp08_kmeans.png", dpi=150)
plt.show()