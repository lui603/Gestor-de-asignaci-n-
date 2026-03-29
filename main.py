Gestor-de-asignaci-n-
import streamlit as st
import pandas as pd
import random
from fpdf import FPDF
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Generador de Roles", layout="wide")

def generar_pdf(asignaciones, fecha):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    # Título
    pdf.cell(190, 10, f"PROGRAMA DE ASIGNACIONES - {fecha}", ln=True, align='C')
    pdf.ln(10)

    # Tabla de Acomodadores y Micrófonos
    pdf.set_fill_color(200, 200, 200)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 10, "ACOMODADORES Y MICRÓFONOS", 1, ln=True, align='C', fill=True)
    
    pdf.set_font("Arial", '', 11)
    for puesto, nombre in asignaciones['servicio'].items():
        pdf.cell(95, 10, puesto, 1)
        pdf.cell(95, 10, nombre, 1, ln=True)
    
    pdf.ln(10)

    # Tabla de Presidencia y Lectura
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 10, "PLATAFORMA Y LECTURA", 1, ln=True, align='C', fill=True)
    
    pdf.set_font("Arial", '', 11)
    for puesto, nombre in asignaciones['plataforma'].items():
        pdf.cell(95, 10, puesto, 1)
        pdf.cell(95, 10, nombre, 1, ln=True)

    return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ DE LA APP ---
st.title("📋 Generador Automático de Formatos")

# Lista de voluntarios (los 30 que mencionaste)
voluntarios = ["Luis Flores", "Jean C Mendoza", "Carlos Herrera", "Pedro Caro", "Rupertino P.", 
               "Rolando N.", "Alberto M.", "Roimer N.", "Juan C. Bracho", "Orlando N."] # Añadir todos aquí

fecha_selec = st.date_input("Selecciona la fecha del programa:", datetime.date.today())

if st.button("🎲 Generar Sorteo y Vista Previa"):
    pool = random.sample(voluntarios, len(voluntarios))
    
    # Creamos el diccionario de asignaciones
    asig = {
        'servicio': {
            "Entrada": pool[0],
            "Auditorio": pool[1],
            "Estacionamiento": pool[2],
            "Micrófonos": f"{pool[3]} / {pool[4]}"
        },
        'plataforma': {
            "Presidencia": pool[5],
            "Lector Estudio": pool[6],
            "Lector Atalaya": pool[7]
        }
    }
    
    st.session_state.asig_actual = asig
    
    # Mostrar vista previa en la App
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Servicio")
        st.table(pd.DataFrame(asig['servicio'].items(), columns=["Puesto", "Nombre"]))
    with col2:
        st.write("### Plataforma")
        st.table(pd.DataFrame(asig['plataforma'].items(), columns=["Puesto", "Nombre"]))
requirements.txt
streamlit
pandas
fpdf

# Botón de Descarga (Solo aparece si ya se generó algo)
if 'asig_actual' in st.session_state:
    pdf_bytes = generar_pdf(st.session_state.asig_actual, fecha_selec)
    st.download_button(
        label="📥 Descargar Programa en PDF",
        data=pdf_bytes,
        file_name=f"Programa_{fecha_selec}.pdf",
        mime="application/pdf"
    )
