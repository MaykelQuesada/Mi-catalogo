import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide", page_title="Mi Catálogo Digital")
st.title("🎬 Mi Catálogo Digital")

# TUS DATOS
TMDB_API_KEY = "cbae36d0e4d2a6f4c53efc4bf55d59fd"
URL_SHEET = "https://docs.google.com/spreadsheets/d/1SA5BN6QT56xEyvK7cb3vuLFGPZDCG2oCgAuCkHf12qs/export?format=csv"

@st.cache_data
def cargar_datos():
    df = pd.read_csv(URL_SHEET)
    df.columns = df.columns.str.strip()
    return df

def obtener_info_tmdb(id_pelicula):
    """Busca detalles técnicos usando tu API KEY"""
    url = f"https://api.themoviedb.org/3/movie/{id_pelicula}?api_key={TMDB_API_KEY}&language=es-ES"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json()
    return None

try:
    df = cargar_datos()
    
    # Filtros
    st.sidebar.header("Filtrar")
    cats = st.sidebar.multiselect("Categoría:", options=df['Categoría'].unique(), default=df['Categoría'].unique())
    df = df[df['Categoría'].isin(cats)]

    # Mostrar
    cols = st.columns(3)
    for i, row in df.iterrows():
        with cols[i % 3]:
            st.subheader(row['Título'])
            # Aquí usamos el ID para traer la info de tu API
            if 'id_tmdb' in row:
                info = obtener_info_tmdb(row['id_tmdb'])
                if info and 'poster_path' in info:
                    st.image(f"https://image.tmdb.org/t/p/w500{info['poster_path']}", use_column_width=True)
            else:
                st.image(row['URL de la imagen'], use_column_width=True)
                
            st.markdown(f"[Ver Tráiler]({row['Tráiler']})")
            st.write("---")
            
except Exception as e:
    st.error(f"Error técnico: {e}")