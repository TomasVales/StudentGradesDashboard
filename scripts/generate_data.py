import pandas as pd
import random
import os

# Crear carpeta si no existe
os.makedirs("data", exist_ok=True)

# Estudiantes y materias
students = [
    "Juan Pérez", "Carla Gómez", "Lautaro Ruiz", "Sofía Díaz", "Nicolás Torres",
    "Martina Fernández", "Bruno Castro", "Camila López", "Lucas Vega", "Valentina Ríos"
]
subjects = ["Math", "History", "Physics", "Biology", "English", "Geography"]
terms = ["Term 1", "Term 2", "Term 3"]
genders = ["Male", "Female"]

# Generar datos
rows = []
for student_id, name in enumerate(students, start=1):
    gender = random.choice(genders)
    age = random.randint(17, 21)
    for term in terms:
        for subject in subjects:
            grade = round(random.uniform(3, 10), 1)
            rows.append({
                "StudentID": f"{student_id:03d}",
                "Name": name,
                "Gender": gender,
                "Age": age,
                "Term": term,
                "Subject": subject,
                "Grade": grade,
                "MaxGrade": 10
            })

# Guardar CSV
df = pd.DataFrame(rows)
df.to_csv("data/student_grades.csv", index=False)
print("✅ student_grades.csv generado correctamente.")
