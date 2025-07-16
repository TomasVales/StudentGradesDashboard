import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuración visual
plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("pastel")

# Cargar datos
df = pd.read_csv("data/student_grades.csv")

# === KPI 1: Promedio general ===
overall_avg = df["Grade"].mean()
print(f"Overall average grade: {overall_avg:.2f}")

# === KPI 2: Porcentaje de aprobados ===
approved_pct = (df["Grade"] >= 6).mean() * 100
print(f"Percentage of approved grades: {approved_pct:.2f}%")

# === KPI 3: Promedio por materia ===
subject_avg = df.groupby("Subject")["Grade"].mean().sort_values()
plt.figure(figsize=(8, 5))
sns.barplot(x=subject_avg.values, y=subject_avg.index, alpha=0.6)
plt.title("Average Grade per Subject")
plt.xlabel("Grade")
plt.ylabel("Subject")
plt.tight_layout()
plt.show()

# === KPI 4: Comparación de promedio por trimestre ===
term_avg = df.groupby("Term")["Grade"].mean()
plt.figure(figsize=(6, 4))
sns.barplot(x=term_avg.index, y=term_avg.values)
plt.title("Average Grade per Term")
plt.ylabel("Grade")
plt.xlabel("Term")
plt.tight_layout()
plt.show()

# === KPI 5: Boxplot por materia ===
plt.figure(figsize=(10, 6))
sns.boxplot(x="Subject", y="Grade", data=df)
plt.title("Grade Distribution by Subject")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# === KPI 6: Promedio por estudiante ===
student_avg = df.groupby("Name")["Grade"].mean().sort_values()
plt.figure(figsize=(10, 5))
sns.barplot(x=student_avg.index, y=student_avg.values)
plt.title("Average Grade per Student")
plt.ylabel("Grade")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# === KPI 7: Materias con más desaprobados ===
fails_by_subject = df[df["Grade"] < 6].groupby(
    "Subject").size().sort_values(ascending=False)
plt.figure(figsize=(8, 5))
sns.barplot(x=fails_by_subject.values, y=fails_by_subject.index)
plt.title("Failed Grades per Subject")
plt.xlabel("Count")
plt.tight_layout()
plt.show()

# === NEW: Histograma de notas por materia ===
plt.figure(figsize=(10, 6))
for subject in df["Subject"].unique():
    sns.histplot(df[df["Subject"] == subject]["Grade"],
                 label=subject, kde=True, alpha=0.4)
plt.title("Grade Distribution by Subject (Histogram)")
plt.xlabel("Grade")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.show()

# === NEW: Porcentaje de aprobados por materia ===
approved_by_subject = df.groupby("Subject").apply(
    lambda x: (x["Grade"] >= 6).mean() * 100)
plt.figure(figsize=(8, 5))
sns.barplot(x=approved_by_subject.values, y=approved_by_subject.index)
plt.title("Percentage of Approved Grades by Subject")
plt.xlabel("Approval Rate (%)")
plt.ylabel("Subject")
plt.tight_layout()
plt.show()

# === NEW: Identificar materia más fácil y más difícil ===
easiest_subject = subject_avg.idxmax()
hardest_subject = subject_avg.idxmin()
print(f"Easiest subject: {easiest_subject} (Avg: {subject_avg.max():.2f})")
print(f"Hardest subject: {hardest_subject} (Avg: {subject_avg.min():.2f})")

# === NEW: Evolución de un alumno en el tiempo ===
# Example for one student (modify to select specific student if needed)
student_name = df["Name"].iloc[0]  # Taking first student as example
student_data = df[df["Name"] == student_name].groupby("Term")["Grade"].mean()
plt.figure(figsize=(8, 5))
sns.lineplot(x=student_data.index, y=student_data.values, marker="o")
plt.title(f"Grade Trend for {student_name} by Term")
plt.xlabel("Term")
plt.ylabel("Average Grade")
plt.tight_layout()
plt.show()

# === NEW: Ranking de estudiantes ===
# Top 3 mejores promedios
top_3_students = student_avg.tail(3)[::-1]
print("\nTop 3 students by average grade:")
for student, avg in top_3_students.items():
    print(f"{student}: {avg:.2f}")

# Top 3 peores promedios
bottom_3_students = student_avg.head(3)
print("\nBottom 3 students by average grade:")
for student, avg in bottom_3_students.items():
    print(f"{student}: {avg:.2f}")

# === NEW: Alumnos en riesgo (promedio general < 6) ===
at_risk_students = student_avg[student_avg < 6]
print("\nStudents at risk (average grade < 6):")
for student, avg in at_risk_students.items():
    print(f"{student}: {avg:.2f}")

# === KPI 8: Exportar KPIs a CSV ===
kpis = {
    "Overall Average": [overall_avg],
    "Approved Percentage": [approved_pct],
    "Easiest Subject": [easiest_subject],
    "Hardest Subject": [hardest_subject]
}
kpis_df = pd.DataFrame(kpis)
os.makedirs("data", exist_ok=True)
kpis_df.to_csv("data/kpis_summary.csv", index=False)
print("KPIs exported to data/kpis_summary.csv")
