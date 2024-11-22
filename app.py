import streamlit as st
from streamlit_lottie import st_lottie
from data_loader import load_data
from utils import load_lottieurl, convertir_urls_a_imagenes, generar_valores_mensuales
from visualizations import (
    plot_evolucion_individual,
    plot_comparacion_jugadores,
    plot_tendencias_generales,
    plot_distribucion_valores
)
from components.league_comparison import show_league_comparison
from components.league_evolution import plot_league_evolution_comparison, plot_league_comparison_stats

# Configuración inicial de la página
st.set_page_config(
    page_title="Análisis Futbolístico",
    page_icon="⚽",
    layout="wide"
)

# Cargar datos
data, data_bundesliga = load_data()

# Sidebar con menú principal
st.sidebar.title("Menú Principal")
menu_principal = st.sidebar.radio(
    "Seleccione una sección:",
    ["Introducción", "Objetivos", "Metodología", "Herramientas", "Resultados", "Conclusiones"]
)

if menu_principal == "Introducción":
    st.title("Introducción")
    st.write("""
    La industria del fútbol ha evolucionado significativamente, convirtiéndose en un mercado 
    donde el valor de los jugadores es un indicador crucial de su desempeño y potencial.
    """)
    
    # Mostrar comparativa de ligas
    show_league_comparison(data, data_bundesliga)
    
    lottie_url = "https://lottie.host/embed/3d48d4b9-51ad-4b7d-9d28-5e248cace11/Rz3QtSCq3.json"
    lottie_coding = load_lottieurl(lottie_url)
    if lottie_coding:
        st_lottie(lottie_coding, height=200, width=300)

elif menu_principal == "Metodología":
    st.title("Metodología")
    
    visualizacion = st.selectbox(
        "Seleccione tipo de visualización:",
        ["Evolución Individual", "Comparación entre Jugadores", "Tendencias Generales", "Comparativa entre Ligas"]
    )
    
    col_inicial = "Valor de Mercado en 01/01/2024"
    col_final = "Valor de Mercado Actual"
    
    if visualizacion == "Evolución Individual":
        liga_seleccionada = st.selectbox(
            "Seleccione la liga a analizar:",
            ["LaLiga", "Bundesliga"]
        )
        datos_analizar = data if liga_seleccionada == "LaLiga" else data_bundesliga
        st.subheader(f"Evolución Individual del Valor de Mercado - {liga_seleccionada}")
        nombre_jugador = st.selectbox("Selecciona un jugador:", datos_analizar['Nombre'].unique())
        plot_evolucion_individual(datos_analizar, nombre_jugador, col_inicial, col_final)
    
    elif visualizacion == "Comparación entre Jugadores":
        st.subheader("Comparación entre Jugadores")
        liga_seleccionada = st.selectbox(
            "Seleccione la liga a analizar:",
            ["LaLiga", "Bundesliga"]
        )
        datos_analizar = data if liga_seleccionada == "LaLiga" else data_bundesliga
        col1, col2 = st.columns(2)
        with col1:
            jugador1 = st.selectbox("Primer jugador:", datos_analizar['Nombre'].unique())
        with col2:
            jugador2 = st.selectbox("Segundo jugador:", datos_analizar['Nombre'].unique())
        plot_comparacion_jugadores(datos_analizar, jugador1, jugador2, col_inicial, col_final)
    
    elif visualizacion == "Tendencias Generales":
        liga_seleccionada = st.selectbox(
            "Seleccione la liga a analizar:",
            ["LaLiga", "Bundesliga"]
        )
        datos_analizar = data if liga_seleccionada == "LaLiga" else data_bundesliga
        st.subheader("Tendencias Generales del Mercado")
        plot_tendencias_generales(datos_analizar, col_inicial, col_final)
    
    elif visualizacion == "Comparativa entre Ligas":
        st.subheader("Análisis Comparativo entre LaLiga y Bundesliga")
        plot_league_evolution_comparison(data, data_bundesliga, col_inicial, col_final)
        plot_league_comparison_stats(data, data_bundesliga)

# ... (rest of the sections remain the same)

elif menu_principal == "Objetivos":
    st.title("Objetivos del Proyecto")
    st.write("""
    ### Objetivos Principales:
    - Analizar y visualizar el valor de mercado de los jugadores
    - Evaluar el incremento porcentual del valor de mercado a lo largo del tiempo
    - Identificar patrones y tendencias en la valoración de jugadores
    """)

elif menu_principal == "Herramientas":
    st.title("Herramientas y Tecnologías")
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Tecnologías Principales")
        st.write("""
        - Python
        - Pandas
        - Streamlit
        - Plotly
        - Google Colab
        - Jupiter Notebook
        """)
    
    with col2:
        st.header("Bibliotecas Adicionales")
        st.write("""
        - Matplotlib
        - Seaborn
        - Streamlit-Lottie
        """)

elif menu_principal == "Resultados":
    st.title("Resultados")
    
    liga_seleccionada = st.selectbox(
        "Seleccione la liga a analizar:",
        ["LaLiga", "Bundesliga", "Comparativa"]
    )
    
    if liga_seleccionada == "Comparativa":
        show_league_comparison(data, data_bundesliga)
    else:
        datos_analizar = data if liga_seleccionada == "LaLiga" else data_bundesliga
        col_inicial = "Valor de Mercado en 01/01/2024"
        col_final = "Valor de Mercado Actual"
        
        tab1, tab2, tab3 = st.tabs(["Estadísticas Generales", "Análisis de Tendencias", "Recomendaciones"])
        
        with tab1:
            st.header("Estadísticas Generales")
            st.write("Estadísticas descriptivas de los valores de mercado:")
            st.dataframe(datos_analizar[[col_inicial, col_final]].describe())
            
        with tab2:
            st.header("Análisis de Tendencias")
            plot_distribucion_valores(datos_analizar, col_inicial, col_final)
            
        with tab3:
            st.header("Recomendaciones")
            st.write("""
            Basadas en el análisis de datos:
            - Recomendaciones para clubes
            - Estrategias de inversión
            - Oportunidades de mercado
            """)

else:  # Conclusiones
    st.title("Conclusiones")
    st.write("""
    ### Principales Hallazgos:
    - El análisis de datos en el fútbol ofrece insights valiosos para la toma de decisiones
    - Las tendencias del mercado muestran patrones significativos en la valoración de jugadores
    - La gestión basada en datos puede mejorar significativamente las estrategias de los equipos
    """)

# Footer
st.sidebar.markdown("---")
st.sidebar.info("ANÁLISIS DE LAS ESTADÍSTICAS QUE TIENEN MAYOR CORRELACIÓN CON EL VALOR DE MERCADO DE LOS JUGADORES DE FUTBOL EN ESPAÑA")
