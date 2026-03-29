import streamlit as st
import pandas as pd
import random
from fpdf import FPDF
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Gestor de Asignaciones", layout="wide")
st.title("📋 Programa de Asignaciones")

# Lista de voluntarios basada en tus fotos
voluntarios = [
    "Luis Flores", "Jean C Mendoza", "Carlos Herrera", "Pedro Caro",
    "Rupertino Pimentel", "Rolando Nuñez", "Alberto Martinez", "Roimer Nuñez",
    "Juan C Bracho", "Orlando Nuñez", "Roberto Sanchez", "Romaldo Nuñez",
    "Guillermo Mendez", "Eliexer Aular", "Ricardo Piña", "Alexander Machado",
    "Emilio Sivira", "Santiago Díaz", "Darwin Rodriguez", "Juan Fernandez"
]

fecha_selec = st.date_input("Selecciona la fecha:", datetime.date.today())

if st.button("🎲 Generar Sorteo Aleatorio"):
    if len(voluntarios) >= 8:
        # Seleccionamos 8 personas al azar sin repetir
        pool = random.sample(voluntarios, 8)
        
        # Creamos el diccionario de asignaciones
        asig = {
            "Entrada": pool[0],
            "Auditorio": pool[1],
            "Estacionamiento": pool[2],
            "Micrófonos": f"{pool[3]} / {pool[4]}",
            "Presidencia": pool[5],
            "Lector Estudio": pool[6],
            "Lector Atalaya": pool[7]
        }
        
        # Guardamos en la memoria de la sesión
        st.session_state.asig_actual = asig
        
        # Mostramos la tabla en pantalla (Aquí estaba el error del paréntesis)
        df = pd.DataFrame(asig.items(), columns=["Asignación", "Nombre"])
        st.table(df)
    else:
        st.error("No hay suficientes voluntarios en la lista.")

# Sección del Botón PDF (Solo aparece si ya se generó el sorteo)
if 'asig_actual' in st.session_state:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, f"PROGRAMA - {fecha_selec}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    for puesto, nombre in st.session_state.asig_actual.items():
        pdf.cell(90, 10, puesto, 1)
        pdf.cell(100, 10, nombre, 1, ln=True)
    
    pdf_output = pdf.output(dest='S').encode('latin-1')
    
    st.download_button(
        label="📥 Descargar Formato en PDF",
        data=pdf_output,
        file_name=f"Programa_{fecha_selec}.pdf",
        mime="application/pdf"
    )
    
