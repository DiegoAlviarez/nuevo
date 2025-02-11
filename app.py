import streamlit as st
import joblib
import numpy as np
import string
import random
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from google.generativeai import configure, ChatModel

configure(api_key="AIzaSyDYz170jq43MyNw8W14GPYb25ZdcNafSnE")
chatbot = ChatModel("gemini-2.0")

st.set_page_config(
    page_title="WildPass Local",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded")

st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: #ffffff;
        }
        .stButton>button {
            border-radius: 12px;
            background: linear-gradient(135deg, #ff7eb3, #ff758c);
            color: white;
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            background: #222;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

class PasswordModel:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        try:
            self.model = joblib.load("local_pass_model.pkl")
            st.success("Modelo de seguridad cargado!")
        except Exception:
            st.warning("Modelo no encontrado, por favor entrénalo primero")
            self.model = None

    def generate_weak_password(self):
        patterns = [
            lambda: ''.join(random.choice(string.ascii_lowercase) for _ in range(8)),
            lambda: ''.join(random.choice(["123456", "password", "qwerty", "admin"])),
            lambda: ''.join(random.choice(string.digits) for _ in range(6))
        ]
        return random.choice(patterns)()

    def generate_strong_password(self):
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.SystemRandom().choice(chars) for _ in range(16))

    def extract_features(self, password):
        return [
            len(password),
            sum(c.isupper() for c in password),
            sum(c.isdigit() for c in password),
            sum(c in string.punctuation for c in password),
            len(set(password)) / max(len(password), 1)
        ]

def animated_message(message):
    with st.empty():
        for _ in range(3):
            st.write(f"{message}.")
            time.sleep(0.3)
            st.write(f"{message}..")
            time.sleep(0.3)
            st.write(f"{message}...")
            time.sleep(0.3)

def create_training_panel(epoch, accuracy, feature_importances):
    feature_bars = "\n".join([
        f"Longitud   {'▮' * int(feature_importances[0]*40)} {feature_importances[0]*100:.1f}%",
        f"Mayúsculas {'▮' * int(feature_importances[1]*40)} {feature_importances[1]*100:.1f}%",
        f"Dígitos    {'▮' * int(feature_importances[2]*40)} {feature_importances[2]*100:.1f}%",
        f"Símbolos   {'▮' * int(feature_importances[3]*40)} {feature_importances[3]*100:.1f}%",
        f"Unicidad   {'▮' * int(feature_importances[4]*40)} {feature_importances[4]*100:.1f}%"
    ])

    panel = f"""
    ╭────────────────── WildPassPro - Entrenamiento de IA ──────────────────╮
    │                                                                        │
    │ Progreso del Entrenamiento:                                            │
    │ Árboles creados: {epoch}/100                                           │
    │ Precisión actual: {accuracy:.1%}                                      │
    │                                                                        │
    │ Características más importantes:                                       │
    {feature_bars}
    │                                                                        │
    │ Creando protección inteligente...                                      │
    ╰────────────────────────────────────────────────────────────────────────╯
    """
    return panel

def chat_with_gemini(user_input):
    response = chatbot.chat(user_input)
    return response.text

def main():
    st.title("🔐 WildPass Local - Generador Seguro")
    st.markdown("---")
    model = PasswordModel()
    
    menu = st.sidebar.selectbox(
        "Menú Principal",
        ["🏠 Inicio", "📊 Analizar Contraseña", "💬 Chatbot de Seguridad"]
    )
    
    if menu == "🏠 Inicio":
        st.subheader("Generar Contraseñas")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔒 Generar Contraseña Fuerte"):
                animated_message("Generando contraseña fuerte")
                password = model.generate_strong_password()
                st.code(password, language="text")
                st.balloons()
                
        with col2:
            if st.button("⚠ Generar Contraseña Débil"):
                animated_message("Generando contraseña débil")
                password = model.generate_weak_password()
                st.code(password, language="text")
                st.warning("Esta contraseña es débil. Considera generar una más fuerte.")
    
    elif menu == "📊 Analizar Contraseña":
        st.subheader("Analizador de Seguridad")
        password = st.text_input("Introduce una contraseña para analizar:", type="password")
        
        if password:
            animated_message("Analizando contraseña")
            if model.model is None:
                st.error("Primero entrena el modelo!")
            else:
                try:
                    score = model.model.predict_proba([model.extract_features(password)])[0][1] * 100
                    st.metric("Puntuación de Seguridad", f"{score:.1f}%")
                    if score > 80:
                        st.success("¡Buena elección! Tu contraseña es segura.")
                    else:
                        st.warning("Tu contraseña podría ser vulnerable. Intenta mejorarla.")
                except Exception as e:
                    st.error(f"Error en análisis: {str(e)}")
    
    elif menu == "💬 Chatbot de Seguridad":
        st.subheader("Chatbot de Seguridad")
        user_input = st.text_input("Pregúntame sobre seguridad de contraseñas")
        if user_input:
            animated_message("Procesando respuesta")
            response = chat_with_gemini(user_input)
            st.write(response)

if __name__ == "__main__":
    main()
