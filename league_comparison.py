import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def show_league_comparison(data_laliga, data_bundesliga):
    st.subheader("Comparativa entre LaLiga y Bundesliga")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### LaLiga")
        st.dataframe(data_laliga)
        
    with col2:
        st.markdown("### Bundesliga")
        st.dataframe(data_bundesliga)
        
    # Análisis estadístico comparativo
    st.subheader("Análisis Estadístico Comparativo")
    
    stats_laliga = data_laliga["Valor de Mercado Actual"].describe()
    stats_bundesliga = data_bundesliga["Valor de Mercado Actual"].describe()
    
    comparison_df = pd.DataFrame({
        'LaLiga': stats_laliga,
        'Bundesliga': stats_bundesliga
    })
    
    st.dataframe(comparison_df)
    
    # Gráfico comparativo de distribución de valores
    fig = go.Figure()
    
    fig.add_trace(go.Box(
        y=data_laliga["Valor de Mercado Actual"].dropna(),
        name="LaLiga",
        boxpoints='outliers'
    ))
    
    fig.add_trace(go.Box(
        y=data_bundesliga["Valor de Mercado Actual"].dropna(),
        name="Bundesliga",
        boxpoints='outliers'
    ))
    
    fig.update_layout(
        title="Distribución de Valores de Mercado por Liga",
        yaxis_title="Valor de Mercado (€)",
        showlegend=True
    )
    
    st.plotly_chart(fig)