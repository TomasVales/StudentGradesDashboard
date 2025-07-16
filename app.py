# app.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Configuración visual
plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("pastel")

# Cargar datos
df = pd.read_csv("data/student_grades.csv")

# Configuración de Streamlit
st.set_page_config(layout="wide")
st.title("Dashboard de Notas de Estudiantes")

# Sidebar para filtros
with st.sidebar:
    st.header("Opciones de Filtro")
    selected_subject = st.selectbox(
        "Seleccionar Materia", ["Todas"] + list(df["Subject"].unique()))
    selected_term = st.selectbox("Seleccionar Trimestre", [
                                 "Todos"] + list(df["Term"].unique()))

    # Aplicar filtros
    if selected_subject != "Todas":
        df = df[df["Subject"] == selected_subject]
    if selected_term != "Todos":
        df = df[df["Term"] == selected_term]

# === KPIs Principales ===
st.subheader("Indicadores Clave")

col1, col2, col3, col4 = st.columns(4)

# KPI 1: Promedio general
overall_avg = df["Grade"].mean()
col1.metric("Promedio General", f"{overall_avg:.2f}")

# KPI 2: Porcentaje de aprobados
approved_pct = (df["Grade"] >= 6).mean() * 100
col2.metric("Porcentaje de Aprobados", f"{approved_pct:.2f}%")

# KPI 3: Materias más fácil y difícil (solo si no hay filtro de materia)
if selected_subject == "Todas":
    subject_avg = df.groupby("Subject")["Grade"].mean()
    easiest_subject = subject_avg.idxmax()
    hardest_subject = subject_avg.idxmin()
    col3.metric("Materia Más Fácil",
                f"{easiest_subject} ({subject_avg.max():.2f})")
    col4.metric("Materia Más Difícil",
                f"{hardest_subject} ({subject_avg.min():.2f})")

# === Visualizaciones ===
st.subheader("Visualizaciones")

# KPI 3: Promedio por materia
if selected_subject == "Todas":
    st.write("### Promedio por Materia")
    subject_avg = df.groupby("Subject")["Grade"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=subject_avg.values, y=subject_avg.index, ax=ax)
    st.pyplot(fig)

# KPI 4: Comparación de promedio por trimestre
if selected_term == "Todos":
    st.write("### Promedio por Trimestre")
    term_avg = df.groupby("Term")["Grade"].mean()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=term_avg.index, y=term_avg.values, ax=ax)
    st.pyplot(fig)

# KPI 5: Boxplot por materia
st.write("### Distribución de Notas")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x="Subject" if selected_subject == "Todas" else None,
            y="Grade",
            data=df,
            ax=ax)
if selected_subject != "Todas":
    ax.set_title(f"Distribución de Notas para {selected_subject}")
st.pyplot(fig)

# KPI 6: Promedio por estudiante
st.write("### Promedio por Estudiante")
student_avg = df.groupby("Name")["Grade"].mean().sort_values()
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=student_avg.index, y=student_avg.values, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# KPI 7: Materias con más desaprobados
if selected_subject == "Todas":
    st.write("### Materias con Más Desaprobados")
    fails_by_subject = df[df["Grade"] < 6].groupby(
        "Subject").size().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=fails_by_subject.values, y=fails_by_subject.index, ax=ax)
    st.pyplot(fig)

# NEW: Histograma de notas
st.write("### Distribución de Notas (Histograma)")
fig, ax = plt.subplots(figsize=(10, 6))
if selected_subject == "Todas":
    for subject in df["Subject"].unique():
        sns.histplot(df[df["Subject"] == subject]["Grade"],
                     label=subject, kde=True, alpha=0.4, ax=ax)
    plt.legend()
else:
    sns.histplot(df["Grade"], kde=True, ax=ax)
st.pyplot(fig)

# NEW: Porcentaje de aprobados por materia
if selected_subject == "Todas":
    st.write("### Porcentaje de Aprobados por Materia")
    approved_by_subject = df.groupby("Subject").apply(
        lambda x: (x["Grade"] >= 6).mean() * 100)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=approved_by_subject.values,
                y=approved_by_subject.index, ax=ax)
    st.pyplot(fig)

# NEW: Evolución de un alumno en el tiempo
st.write("### Evolución de Notas por Trimestre")
selected_student = st.selectbox("Seleccionar Estudiante", df["Name"].unique())
student_data = df[df["Name"] == selected_student].groupby("Term")[
    "Grade"].mean()
fig, ax = plt.subplots(figsize=(8, 5))
sns.lineplot(x=student_data.index, y=student_data.values, marker="o", ax=ax)
ax.set_title(f"Evolución de {selected_student}")
st.pyplot(fig)

# NEW: Ranking de estudiantes
st.write("### Ranking de Estudiantes")
col1, col2 = st.columns(2)

with col1:
    st.write("**Top 3 Mejores Promedios**")
    top_3 = student_avg.tail(3)[::-1]
    for student, avg in top_3.items():
        st.write(f"- {student}: {avg:.2f}")

with col2:
    st.write("**Top 3 Peores Promedios**")
    bottom_3 = student_avg.head(3)
    for student, avg in bottom_3.items():
        st.write(f"- {student}: {avg:.2f}")

# NEW: Alumnos en riesgo
st.write("### Alumnos en Riesgo (promedio < 6)")
at_risk = student_avg[student_avg < 6]
if not at_risk.empty:
    for student, avg in at_risk.items():
        st.write(f"- {student}: {avg:.2f}")
else:
    st.write("No hay alumnos en riesgo")

# Exportar KPIs
if st.button("Exportar KPIs a CSV"):
    kpis = {
        "Overall Average": [overall_avg],
        "Approved Percentage": [approved_pct],
        "Easiest Subject": [easiest_subject] if selected_subject == "Todas" else [selected_subject],
        "Hardest Subject": [hardest_subject] if selected_subject == "Todas" else [selected_subject]
    }
    kpis_df = pd.DataFrame(kpis)
    os.makedirs("data", exist_ok=True)
    kpis_df.to_csv("data/kpis_summary.csv", index=False)
    st.success("KPIs exportados a data/kpis_summary.csv")
