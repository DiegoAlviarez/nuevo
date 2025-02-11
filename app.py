import streamlit as st
import joblib
import numpy as np
import string
import random
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from google.generativeai import configure, generate_content

configure(api_key="TU_API_KEY_GEMINI")

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

def chat_with_gemini(prompt):
    response = generate_content(prompt)
    return response.text if response else "No se pudo obtener respuesta."

def main():
    st.set_page_config(
        page_title="WildPass Local",
        page_icon="🔒",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    
    st.title("🔐 WildPass Local - Generador Seguro")
    st.markdown("---")
    
    model = PasswordModel()
    
    menu = st.sidebar.selectbox(
        "Menú Principal",
        ["🏠 Inicio", "📊 Analizar Contraseña", "💬 Chat de Seguridad"]
    )
    
    if menu == "🏠 Inicio":
        st.subheader("Generar Contraseñas")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔒 Generar Contraseña Fuerte"):
                animated_message("Generando contraseña fuerte")
                password = model.generate_strong_password()
                st.code(password, language="text")
                
        with col2:
            if st.button("⚠ Generar Contraseña Débil"):
                animated_message("Generando contraseña débil")
                password = model.generate_weak_password()
                st.code(password, language="text")
                
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
                except Exception as e:
                    st.error(f"Error en análisis: {str(e)}")

    elif menu == "💬 Chat de Seguridad":
        st.subheader("Asistente de Seguridad - Gemini AI")
        user_input = st.text_area("Escribe tu duda sobre seguridad de contraseñas:")
        if st.button("Preguntar"):
            if user_input:
                response = chat_with_gemini(user_input)
                st.write(response)
            else:
                st.warning("Por favor, escribe una pregunta.")

if __name__ == "__main__":
    main()
