import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from streamlit_particles import particles
import hydralit_components as hc
from streamlit_card import card
from streamlit_extras.metric_cards import style_metric_cards

# Configuración inicial de la página
st.set_page_config(
    page_title="Análisis Futbolístico",
    page_icon="⚽",
    layout="wide"
)

# Custom CSS para mejorar la apariencia
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #1a1a1a, #2d2d2d);
        color: white;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
    }
    .glass-container {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Configuración de partículas para el fondo
def load_particles():
    particles(
        options={
            "particles": {
                "number": {"value": 30, "density": {"enable": True, "value_area": 800}},
                "color": {"value": "#ffffff"},
                "shape": {"type": "circle"},
                "opacity": {"value": 0.3},
                "size": {"value": 3},
                "line_linked": {
                    "enable": True,
                    "distance": 150,
                    "color": "#ffffff",
                    "opacity": 0.2,
                    "width": 1
                },
                "move": {"enable": True, "speed": 2}
            }
        }
    )

# Función para cargar animaciones Lottie
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Función para cargar datos
@st.cache_data
def load_data():
    file_path = 'https://raw.githubusercontent.com/AndersonP444/PROYECTO-SIC-JAKDG/main/valores_mercado_actualizados%20(3).csv'
    return pd.read_csv(file_path)

# Función para convertir valores de mercado
def convertir_valor(valor):
    if isinstance(valor, str):
        if "mil €" in valor:
            return int(float(valor.replace(" mil €", "").replace(",", ".")) * 1_000)
        elif "mill. €" in valor:
            return int(float(valor.replace(" mill. €", "").replace(",", ".")) * 1_000_000)
    return None

# Función para convertir URLs a imágenes
def convertir_urls_a_imagenes(df):
    df_copy = df.copy()
    for col in df_copy.columns:
        if df_copy[col].astype(str).str.startswith('http').any():
            df_copy[col] = df_copy[col].apply(lambda url: f'<img src="{url}" width="50">' if isinstance(url, str) and url.startswith('http') else url)
    return df_copy

# Función para generar valores mensuales interpolados
def generar_valores_mensuales(valor_inicial, valor_final):
    fecha_inicio = datetime(2024, 1, 1)
    fecha_actual = datetime.now()
    meses = []
    valores = []
    
    fecha_actual = fecha_actual.replace(day=1)
    fecha = fecha_inicio
    while fecha <= fecha_actual:
        meses.append(fecha.strftime('%B %Y'))
        fecha += timedelta(days=32)
        fecha = fecha.replace(day=1)
    
    num_meses = len(meses)
    for i in range(num_meses):
        valor = valor_inicial + (valor_final - valor_inicial) * (i / (num_meses - 1))
        valores.append(valor)
    
    return meses, valores

# Cargar datos
data = load_data()
data["Valor de Mercado en 01/01/2024"] = data["Valor de Mercado en 01/01/2024"].apply(convertir_valor)
data["Valor de Mercado Actual"] = data["Valor de Mercado Actual"].apply(convertir_valor)

# Cargar partículas en el fondo
load_particles()

# Menú principal mejorado
with st.sidebar:
    menu_principal = option_menu(
        "Menú Principal",
        ["Introducción", "Objetivos", "Metodología", "Herramientas", "Resultados", "Conclusiones"],
        icons=['house', 'target', 'gear', 'tools', 'graph-up', 'check-circle'],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#262730"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px"},
            "nav-link-selected": {"background-color": "#0083B8"},
        }
    )

if menu_principal == "Introducción":
    st.title("Introducción")
    
    with st.container():
        st.markdown("""
        <div class="glass-container">
            <h3>La industria del fútbol ha evolucionado significativamente</h3>
            <p>Convirtiéndose en un mercado donde el valor de los jugadores es un indicador 
            crucial de su desempeño y potencial.</p>
        </div>
        """, unsafe_allow_html=True)
    
    lottie_url = "https://lottie.host/embed/3d48d4b9-51ad-4b7d-9d28-5e248cace11/Rz3QtSCq3.json"
    lottie_coding = load_lottieurl(lottie_url)
    if lottie_coding:
        st_lottie(lottie_coding, height=200, width=300)
    
    data_formateada = data.copy()
    data_formateada["Valor de Mercado en 01/01/2024"] = data_formateada["Valor de Mercado en 01/01/2024"].apply(lambda x: f"€{int(x):,}" if pd.notnull(x) else "N/A")
    data_formateada["Valor de Mercado Actual"] = data_formateada["Valor de Mercado Actual"].apply(lambda x: f"€{int(x):,}" if pd.notnull(x) else "N/A")

    data_con_imagenes = convertir_urls_a_imagenes(data_formateada)
    
    with st.container():
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.subheader("Datos de Jugadores")
        st.write("Tabla con imágenes de los jugadores y valores de mercado.")
        st.markdown(data_con_imagenes.to_html(escape=False), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif menu_principal == "Metodología":
    st.title("Metodología")
    
    with st.container():
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        visualizacion = st.selectbox(
            "Seleccione tipo de visualización:",
            ["Evolución Individual", "Comparación entre Jugadores", "Tendencias Generales"]
        )
        
        if visualizacion == "Evolución Individual":
            st.subheader("Evolución Individual del Valor de Mercado")
            nombre_jugador = st.selectbox("Selecciona un jugador:", data['Nombre'].unique())
            
            jugador = data[data['Nombre'] == nombre_jugador]
            if not jugador.empty:
                valor_inicial = jugador['Valor de Mercado en 01/01/2024'].iloc[0]
                valor_final = jugador['Valor de Mercado Actual'].iloc[0]
                
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
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig)
                
                df_mensual = pd.DataFrame({
                    'Mes': meses,
                    'Valor de Mercado (€)': [f"€{int(v):,}" for v in valores]
                })
                st.write("Valores mensuales:")
                st.dataframe(df_mensual)
        
        elif visualizacion == "Comparación entre Jugadores":
            st.subheader("Comparación entre Jugadores")
            col1, col2 = st.columns(2)
            with col1:
                jugador1 = st.selectbox("Primer jugador:", data['Nombre'].unique())
            with col2:
                jugador2 = st.selectbox("Segundo jugador:", data['Nombre'].unique())
            
            if jugador1 and jugador2:
                fig = go.Figure()
                
                for jugador in [jugador1, jugador2]:
                    datos_jugador = data[data['Nombre'] == jugador]
                    valor_inicial = datos_jugador['Valor de Mercado en 01/01/2024'].iloc[0]
                    valor_final = datos_jugador['Valor de Mercado Actual'].iloc[0]
                    
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
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig)
        
        elif visualizacion == "Tendencias Generales":
            st.subheader("Tendencias Generales del Mercado")
            
            fig = go.Figure()
            for _, jugador in data.iterrows():
                valor_inicial = jugador['Valor de Mercado en 01/01/2024']
                valor_final = jugador['Valor de Mercado Actual']
                
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
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig)
        st.markdown('</div>', unsafe_allow_html=True)

elif menu_principal == "Objetivos":
    st.title("Objetivos del Proyecto")
    
    with st.container():
        st.markdown("""
        <div class="glass-container">
            <h3>Objetivos Principales:</h3>
            <ul>
                <li>Analizar y visualizar el valor de mercado de los jugadores</li>
                <li>Evaluar el incremento porcentual del valor de mercado a lo largo del tiempo</li>
                <li>Identificar patrones y tendencias en la valoración de jugadores</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif menu_principal == "Herramientas":
    st.title("Herramientas y Tecnologías")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="glass-container">
            <h3>Tecnologías Principales</h3>
            <ul>
                <li>Python</li>
                <li>Pandas</li>
                <li>Streamlit</li>
                <li>Plotly</li>
                <li>Google Colab</li>
                <li>Jupiter Notebook</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-container">
            <h3>Bibliotecas Adicionales</h3>
            <ul>
                <li>Matplotlib</li>
                <li>Seaborn</li>
                <li>Streamlit-Lottie</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif menu_principal == "Resultados":
    st.title("Resultados")
    
    tab1, tab2, tab3 = st.tabs(["Estadísticas Generales", "Análisis de Tendencias", "Recomendaciones"])
    
    with tab1:
        with st.container():
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.header("Estadísticas Generales")
            st.write("Estadísticas descriptivas de los valores de mercado:")
            st.dataframe(data[['Valor de Mercado en 01/01/2024', 'Valor de Mercado Actual']].describe())
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        with st.container():
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.header("Análisis de Tendencias")
            fig = go.Figure()
            fig.add_trace(go.Box(
                y=data['Valor de Mercado en 01/01/2024'],
                name='Enero 2024'
            ))
            fig.add_trace(go.Box(
                y=data['Valor de Mercado Actual'],
                name='Actual'
            ))
            fig.update_layout(
                title='Distribución de Valores de Mercado',
                yaxis_title='Valor de Mercado (€)',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        with st.container():
            st.markdown("""
            <div class="glass-container">
                <h3>Recomendaciones</h3>
                <p>Basadas en el análisis de datos:</p>
                <ul>
                    <li>Recomendaciones para clubes</li>
                    <li>Estrategias de inversión</li>
                    <li>Oportunidades de mercado</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

else:  # Conclusiones
    st.title("Conclusiones")
    
    with st.container():
        st.markdown("""
        <div class="glass-container">
            <h3>Principales Hallazgos:</h3>
            <ul>
                <li>El análisis de datos en el fútbol ofrece insights valiosos para la toma de decisiones</li>
                <li>Las tendencias del mercado muestran patrones significativos en la valoración de jugadores</li>
                <li>La gestión basada en datos puede mejorar significativamente las estrategias de los equipos</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer mejorado
with st.sidebar:
    st.markdown("---")
    st.markdown("""
        <div class="glass-container">
            <small>ANÁLISIS DE LAS ESTADÍSTICAS QUE TIENEN MAYOR CORRELACIÓN 
            CON EL VALOR DE MERCADO DE LOS JUGADORES DE FUTBOL EN ESPAÑA</small>
        </div>
        """, unsafe_allow_html=True)