import streamlit as st
import pandas as pd
import requests

# Configuración de página
st.set_page_config(layout="wide", page_title="Mi Catálogo Digital")
st.title("🎬 Mi Catálogo Digital")

# CONFIGURACIÓN COMPLETA
TMDB_API_KEY = "cbae36d0e4d2a6f4c53efc4bf55d59fd"
URL_SHEET = "https://docs.google.com/spreadsheets/d/1SA5BN6QT56xEyvK7cb3vuLFGPZDCG2oCgAuCkHf12qs/export?format=csv"

@st.cache_data
def cargar_datos():
    return pd.read_csv(URL_SHEET)

try:
    df = cargar_datos()
    
    # Filtros laterales
    st.sidebar.header("Filtros")
    cats = st.sidebar.multiselect("Categoría:", options=df['Categoría'].unique(), default=df['Categoría'].unique())
    gens = st.sidebar.multiselect("Género:", options=df['Género'].unique(), default=df['Género'].unique())

    # Aplicar filtros
    df_f = df[(df['Categoría'].isin(cats)) & (df['Género'].isin(gens))]

    # Visualización
    cols = st.columns(3)
    for i, row in df_f.iterrows():
        with cols[i % 3]:
            st.image(row['URL de la imagen'], use_column_width=True)
            st.subheader(row['Título'])
            st.write(f"**Género:** {row['Género']} | **Categoría:** {row['Categoría']}")
            st.markdown(f"[Ver Tráiler]({row['Tráiler']})")
            st.write("---")
            
except Exception as e:
    st.error(f"Error: Revisa que tu archivo tenga estas columnas exactas: Título, Categoría, Género, URL de la imagen y Tráiler. Detalle: {e}")