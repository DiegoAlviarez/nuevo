import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils import generar_valores_mensuales

def plot_league_evolution_comparison(data_laliga, data_bundesliga, col_inicial, col_final):
    st.subheader("Evolución Comparativa entre Ligas")
    
    # Calcular promedios por liga
    avg_laliga_inicial = data_laliga[col_inicial].mean()
    avg_laliga_final = data_laliga[col_final].mean()
    
    avg_bundesliga_inicial = data_bundesliga[col_inicial].mean()
    avg_bundesliga_final = data_bundesliga[col_final].mean()
    
    # Generar valores mensuales para cada liga
    meses_laliga, valores_laliga = generar_valores_mensuales(avg_laliga_inicial, avg_laliga_final)
    meses_bundesliga, valores_bundesliga = generar_valores_mensuales(avg_bundesliga_inicial, avg_bundesliga_final)
    
    # Crear gráfico
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=meses_laliga,
        y=valores_laliga,
        name="LaLiga",
        mode='lines+markers'
    ))
    
    fig.add_trace(go.Scatter(
        x=meses_bundesliga,
        y=valores_bundesliga,
        name="Bundesliga",
        mode='lines+markers'
    ))
    
    fig.update_layout(
        title="Evolución del Valor de Mercado Promedio por Liga",
        xaxis_title="Mes",
        yaxis_title="Valor de Mercado Promedio (€)",
        showlegend=True
    )
    
    st.plotly_chart(fig)

def plot_league_comparison_stats(data_laliga, data_bundesliga):
    st.subheader("Estadísticas Comparativas")
    
    # Calcular estadísticas por liga
    stats_laliga = data_laliga["Valor de Mercado Actual"].agg(['mean', 'median', 'std', 'min', 'max'])
    stats_bundesliga = data_bundesliga["Valor de Mercado Actual"].agg(['mean', 'median', 'std', 'min', 'max'])
    
    comparison_df = pd.DataFrame({
        'LaLiga': stats_laliga,
        'Bundesliga': stats_bundesliga
    })
    
    st.dataframe(comparison_df)