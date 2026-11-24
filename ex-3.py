import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(7)
n = 60
students = pd.DataFrame(
{
"roll_no": range(1, n + 1),
"gender": np.random.choice(["Male", "Female"], n), "department": np.random.choice(
["CSE", "ECE", "MECH", "AI&DS"], n, p=[0.3, 0.25, 0.2, 0.25]
),
"grade": np.random.choice(
["A", "B", "C", "D"], n, p=[0.25, 0.4, 0.25, 0.1]
),
"attendance": np.random.randint(60, 100, n), "study_hours": np.round(np.random.uniform(1, 8, n), 1),
}
)
students["marks"] = np.clip( (
35
+ 6 * students["study_hours"]
+ 0.2 * students["attendance"]
+ np.random.normal(0, 6, n)
).round(), 0,
100,
).astype(int)

print("Student Performance: Exploratory Data Analysis") 
print("=" * 50)
print("\nFirst 5 records:") 
print(students.head().to_string(index=False))

# ---------- Classification of data ----------
data_types = {
"roll_no": "Nominal (identifier)", "gender": "Qualitative - Nominal", "department": "Qualitative - Nominal", "grade": "Qualitative - Ordinal", "attendance": "Quantitative - Discrete", "study_hours": "Quantitative - Continuous", "marks": "Quantitative - Discrete",
}
print("\nClassification of attributes:") 
for col, t in data_types.items():
 print(f" {col:<12} : {t}")

# ---------- Descriptive statistics ----------
num = students[["attendance", "study_hours", "marks"]] 
print("\nSummary statistics:") 
print(num.describe().round(2).to_string()) 
print("\nMedian :", num.median().to_dict()) 
print("Mode of grade :", students["grade"].mode()[0])
print("Skewness of marks :", round(students["marks"].skew(), 3))

print("\nFrequency table - department:") 
print(students["department"].value_counts().to_string()) 
print("\nCross table - department vs grade:")
print(pd.crosstab(students["department"], students["grade"]).to_string())
print("\nCorrelation matrix:")
print(num.corr().round(3).to_string())

# ---------- Graphical presentation ----------
fig, ax = plt.subplots(2, 2, figsize=(10, 8))
 
ax[0, 0].hist(students["marks"], bins=8, color="steelblue", edgecolor="black")
ax[0, 0].set_title("Histogram of Marks")
ax[0, 0].set_xlabel("Marks") 
ax[0, 0].set_ylabel("Frequency")

dept = students["department"].value_counts() 
ax[0, 1].bar(
dept.index, dept.values, color=["#4c72b0", "#dd8452", "#55a868", "#c44e52"]
)
ax[0, 1].set_title("Students per Department")

grade = students["grade"].value_counts().sort_index()
ax[1, 0].pie(grade.values, labels=grade.index, autopct="%1.1f%%", startangle=90)
ax[1, 0].set_title("Grade Distribution")

ax[1, 1].scatter(students["study_hours"], students["marks"], c="darkgreen") 
ax[1, 1].set_title("Study Hours vs Marks")
ax[1, 1].set_xlabel("Study hours per day") 
ax[1, 1].set_ylabel("Marks")

plt.tight_layout() 
plt.savefig("exp03_eda.png", dpi=150) 
plt.show()
print("\nPlot saved as exp03_eda.png")
