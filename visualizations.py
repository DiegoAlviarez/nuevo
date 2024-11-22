import plotly.graph_objects as go
import streamlit as st
from utils import generar_valores_mensuales
import pandas as pd

def plot_evolucion_individual(datos_analizar, nombre_jugador, col_inicial, col_final):
    jugador = datos_analizar[datos_analizar['Nombre'] == nombre_jugador]
    if not jugador.empty:
        valor_inicial = jugador[col_inicial].iloc[0]
        valor_final = jugador[col_final].iloc[0]
        
        meses, valores = generar_valores_mensuales(valor_inicial, valor_final)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=meses,
            y=valores,
            mode='lines+markers',
            name=nombre_jugador,
            line=dict(width=3),
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            title=f'Evolución Mensual del Valor de Mercado de {nombre_jugador}',
            xaxis_title='Mes',
            yaxis_title='Valor de Mercado (€)',
            hovermode='x unified',
            showlegend=True
        )
        
        st.plotly_chart(fig)
        
        df_mensual = pd.DataFrame({
            'Mes': meses,
            'Valor de Mercado (€)': [f"€{int(v):,}" for v in valores]
        })
        st.write("Valores mensuales:")
        st.dataframe(df_mensual)

def plot_comparacion_jugadores(datos_analizar, jugador1, jugador2, col_inicial, col_final):
    if jugador1 and jugador2:
        fig = go.Figure()
        
        for jugador in [jugador1, jugador2]:
            datos_jugador = datos_analizar[datos_analizar['Nombre'] == jugador]
            valor_inicial = datos_jugador[col_inicial].iloc[0]
            valor_final = datos_jugador[col_final].iloc[0]
            
            meses, valores = generar_valores_mensuales(valor_inicial, valor_final)
            
            fig.add_trace(go.Scatter(
                x=meses,
                y=valores,
                mode='lines+markers',
                name=jugador,
                line=dict(width=3),
                marker=dict(size=10)
            ))
        
        fig.update_layout(
            title='Comparación de Evolución Mensual del Valor de Mercado',
            xaxis_title='Mes',
            yaxis_title='Valor de Mercado (€)',
            hovermode='x unified',
            showlegend=True
        )
        st.plotly_chart(fig)

def plot_tendencias_generales(datos_analizar, col_inicial, col_final):
    fig = go.Figure()
    for _, jugador in datos_analizar.iterrows():
        valor_inicial = jugador[col_inicial]
        valor_final = jugador[col_final]
        
        meses, valores = generar_valores_mensuales(valor_inicial, valor_final)
        
        fig.add_trace(go.Scatter(
            x=meses,
            y=valores,
            mode='lines',
            name=jugador['Nombre'],
            opacity=0.5
        ))
    
    fig.update_layout(
        title='Tendencias Generales del Valor de Mercado',
        xaxis_title='Mes',
        yaxis_title='Valor de Mercado (€)',
        hovermode='x unified',
        showlegend=True
    )
    st.plotly_chart(fig)

def plot_distribucion_valores(datos_analizar, col_inicial, col_final):
    fig = go.Figure()
    fig.add_trace(go.Box(
        y=datos_analizar[col_inicial],
        name='Enero 2024'
    ))
    fig.add_trace(go.Box(
        y=datos_analizar[col_final],
        name='Actual'
    ))
    fig.update_layout(
        title='Distribución de Valores de Mercado',
        yaxis_title='Valor de Mercado (€)'
    )
    st.plotly_chart(fig)