# ---------- Variables and basic data types ----------
hospital = "City Care Clinic"  # str
patients_today = 4  # int
consultation_fee = 350.0  # float
is_open = True  # bool
emergency_contact = None  # NoneType
complex_reading = 3 + 4j  # complex (used here only to show the type)

print("Patient Health Indicator System")
print("=" * 40)
print("Variables and their types:")
for name, value in [
    ("hospital", hospital),
    ("patients_today", patients_today),
    ("consultation_fee", consultation_fee),
    ("is_open", is_open),
    ("emergency_contact", emergency_contact),
    ("complex_reading", complex_reading),
]:
    print(f"  {name:<18} = {str(value):<18} type = {type(value).__name__}")

# ---------- Expressions and operators ----------
print("\nExpressions:")
print("  Total fee (arithmetic)        :", patients_today * consultation_fee)
print("  17 // 5, 17 % 5, 2 ** 10      :", 17 // 5, 17 % 5, 2**10)
print("  Fee > 300 and clinic open     :", consultation_fee > 300 and is_open)
print("  Type conversion int('45') + 5 :", int("45") + 5)
print("  abs(complex_reading)          :", abs(complex_reading))

# ---------- Functions ----------
def bmi(weight_kg, height_m):
    """Return Body Mass Index rounded to 2 decimals."""
    return round(weight_kg / height_m**2, 2)

def bmi_category(value):
    if value < 18.5:
        return "Underweight"
    elif value < 25:
        return "Normal"
    elif value < 30:
        return "Overweight"
    return "Obese"

def bp_status(systolic, diastolic=80):  # default argument
    if systolic >= 140 or diastolic >= 90:
        return "High"
    if systolic < 90 or diastolic < 60:
        return "Low"
    return "Normal"

def average(*values):  # variable-length arguments
    return round(sum(values) / len(values), 2)

def summary(**details):  # keyword arguments
    return ", ".join(f"{k}={v}" for k, v in details.items())

risk_score = lambda age, bmi_val: round(0.03 * age + 0.05 * bmi_val, 2)  # lambda

# ---------- Objects (class) ----------
class Patient:
    count = 0  # class attribute

    def __init__(self, name, age, weight, height, systolic, diastolic):
        self.name, self.age = name, age
        self.weight, self.height = weight, height
        self.systolic, self.diastolic = systolic, diastolic
        Patient.count += 1

    def report(self):
        b = bmi(self.weight, self.height)
        return (
            f"{self.name:<8} Age {self.age:>2} | BMI {b:>5} ({bmi_category(b):<11}) | "
            f"BP {self.systolic}/{self.diastolic} "
            f"({bp_status(self.systolic, self.diastolic)}) | "
            f"Risk {risk_score(self.age, b)}"
        )

    def __str__(self):
        return f"Patient({self.name}, {self.age})"

patients = [
    Patient("Arun", 52, 82, 1.70, 145, 92),
    Patient("Sneha", 28, 54, 1.62, 112, 74),
    Patient("Gopal", 65, 60, 1.68, 88, 58),
    Patient("Nisha", 41, 95, 1.60, 130, 85),
]

print("\nPatient reports (objects + functions):")
for p in patients:
    print(" ", p.report())

print("\nObjects created     :", Patient.count)
print("str() of an object  :", patients[0])
print("isinstance check    :", isinstance(patients[0], Patient))
print("Average age (*args) :", average(*[p.age for p in patients]))
print(
    "Summary (**kwargs)  :",
    summary(clinic=hospital, patients=Patient.count, fee=consultation_fee),
)
print("bp_status(120) uses default diastolic ->", bp_status(120))
print("Docstring of bmi()  :", bmi.__doc__)