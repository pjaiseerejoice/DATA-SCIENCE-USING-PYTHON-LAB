import sqlite3
import pandas as pd

conn = sqlite3.connect(":memory:")
cur = conn.cursor()

# ---------- Step 1: Create the relational schema ----------
cur.executescript("""
CREATE TABLE doctors (
    doctor_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL
);
CREATE TABLE patients (
    patient_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    city TEXT
);
CREATE TABLE visits (
    visit_id INTEGER PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(patient_id),
    doctor_id INTEGER REFERENCES doctors(doctor_id),
    visit_date TEXT,
    fee REAL
);
""")

# ---------- Step 2: Insert records ----------
cur.executemany(
    "INSERT INTO doctors VALUES (?,?,?)", [
        (1, "Dr. Ramesh", "Cardiology"),
        (2, "Dr. Kavitha", "Orthopaedics"),
        (3, "Dr. Imran", "General Medicine"),
    ],
)
cur.executemany(
    "INSERT INTO patients VALUES (?,?,?,?,?)", [
        (1, "Ajay", 45, "M", "Chennai"),
        (2, "Bhavana", 32, "F", "Madurai"),
        (3, "Charles", 67, "M", "Chennai"),
        (4, "Deepa", 29, "F", "Coimbatore"),
        (5, "Elango", 54, "M", "Madurai"),
        (6, "Fathima", 38, "F", "Chennai"),
    ],
)
cur.executemany(
    "INSERT INTO visits VALUES (?,?,?,?,?)", [
        (1, 1, 1, "2026-01-05", 800),
        (2, 2, 2, "2026-01-06", 600),
        (3, 3, 1, "2026-01-08", 800),
        (4, 4, 3, "2026-01-09", 300),
        (5, 5, 1, "2026-01-12", 800),
        (6, 1, 3, "2026-01-15", 300),
        (7, 6, 2, "2026-01-18", 600),
        (8, 3, 3, "2026-01-20", 300),
        (9, 2, 2, "2026-01-22", 600),
        (10, 5, 3, "2026-01-25", 300),
    ],
)
conn.commit()

def run(title, sql):
    print(f"\n--- {title} ---")
    print("SQL:", " ".join(sql.split()))
    print(pd.read_sql_query(sql, conn).to_string(index=False))

print("Hospital Patient Records: Working with a Relational Database")
print("=" * 60)

run(
    "Q1. Patients older than 40",
    """
    SELECT name, age, city FROM patients WHERE age > 40 ORDER BY age DESC
    """,
)

run(
    "Q2. Visits with patient and doctor names (JOIN)",
    """
    SELECT v.visit_id, p.name AS patient, d.name AS doctor, d.department, v.fee FROM visits v
    JOIN patients p ON v.patient_id = p.patient_id JOIN doctors d ON v.doctor_id = d.doctor_id ORDER BY v.visit_id
    """,
)

run(
    "Q3. Revenue and visit count per department (GROUP BY)",
    """
    SELECT d.department, COUNT(*) AS visits, SUM(v.fee) AS revenue FROM visits v JOIN doctors d ON v.doctor_id = d.doctor_id GROUP BY d.department ORDER BY revenue DESC
    """,
)

run(
    "Q4. Patients with more than one visit (HAVING)",
    """
    SELECT p.name, COUNT(*) AS visits
    FROM visits v JOIN patients p ON v.patient_id = p.patient_id GROUP BY p.name HAVING COUNT(*) > 1
    """,
)

# ---------- Step 3: Update and delete ----------
cur.execute(
    "UPDATE doctors SET department = 'Internal Medicine' WHERE doctor_id = 3"
)
cur.execute("DELETE FROM visits WHERE visit_id = 10")
conn.commit()
print("\nUpdated doctor 3 department; deleted visit 10.")
run("Q5. Doctors table after update", "SELECT * FROM doctors")
print(
    "\nTotal visits after delete:",
    cur.execute("SELECT COUNT(*) FROM visits").fetchone()[0],
)

# ---------- Step 4: Load into pandas for analysis ----------
df = pd.read_sql_query(
    """
    SELECT p.city, p.gender, v.fee FROM visits v
    JOIN patients p ON v.patient_id = p.patient_id
    """, conn,
)
print("\n--- City-wise average fee using pandas ---")
print(df.groupby("city")["fee"].agg(["count", "mean"]).round(2).to_string())

# ---------- Step 5: Same data as a NoSQL document collection ----------
import json

rows = pd.read_sql_query(
    """
    SELECT p.patient_id, p.name, p.age, p.city, d.department, v.visit_date, v.fee FROM patients p JOIN visits v ON p.patient_id = v.patient_id
    JOIN doctors d ON v.doctor_id = d.doctor_id ORDER BY p.patient_id, v.visit_date
    """, conn,
)
conn.close()

collection = []
for pid, grp in rows.groupby("patient_id"):
    first = grp.iloc[0]
    collection.append(
        {
            "_id": int(pid),
            "name": first["name"],
            "age": int(first["age"]),
            "city": first["city"],
            "visits": [
                {"dept": r.department, "date": r.visit_date, "fee": float(r.fee)} for r in grp.itertuples()
            ],
        }
    )

with open("patients_nosql.json", "w") as f:
    json.dump(collection, f, indent=2)

print("\n--- NoSQL document model (one document per patient) ---")
print(json.dumps(collection[0], indent=2))

def find(coll, condition):
    """Mimics MongoDB's db.collection.find() using a Python predicate."""
    return [doc for doc in coll if condition(doc)]

print(
    "\nMongoDB query : db.patients.find({city: 'Chennai', 'visits.dept': 'Cardiology'})"
)
result = find(
    collection,
    lambda d: d["city"] == "Chennai"
    and any(v["dept"] == "Cardiology" for v in d["visits"]),
)
for doc in result:
    print(f" {doc['_id']} {doc['name']:<8} visits = {len(doc['visits'])}")