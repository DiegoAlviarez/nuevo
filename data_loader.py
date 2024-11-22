import pandas as pd
import streamlit as st
from utils import convertir_valor

@st.cache_data
def load_data():
    # Cargar datos originales
    file_path = 'https://raw.githubusercontent.com/AndersonP444/PROYECTO-SIC-JAKDG/main/valores_mercado_actualizados%20(3).csv'
    data_original = pd.read_csv(file_path)
    
    # Cargar datos de Bundesliga
    bundesliga_path = 'https://raw.githubusercontent.com/AndersonP444/PROYECTO-SIC-JAKDG/main/valores_mercado_bundesliga.csv'
    data_bundesliga = pd.read_csv(bundesliga_path)
    
    # Preparar datos originales
    data_original["Valor de Mercado en 01/01/2024"] = data_original["Valor de Mercado en 01/01/2024"].apply(convertir_valor)
    data_original["Valor de Mercado Actual"] = data_original["Valor de Mercado Actual"].apply(convertir_valor)
    
    # Preparar datos de Bundesliga
    data_bundesliga["Valor de Mercado en 01/01/2024"] = data_bundesliga["Valor de Mercado en 01/01/2024"].apply(convertir_valor)
    data_bundesliga["Valor de Mercado Actual"] = data_bundesliga["Valor de Mercado Actual"].apply(convertir_valor)
    
    return data_original, data_bundesliga