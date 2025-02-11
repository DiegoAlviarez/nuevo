import streamlit as st
import joblib
import numpy as np
import string
import random
import time
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from google.generativeai import configure, Chat

# Configurar Gemini 2.0 (debes agregar tu API key de Gemini)
GEMINI_API_KEY = "AIzaSyDYz170jq43MyNw8W14GPYb25ZdcNafSnE"
configure(api_key=GEMINI_API_KEY)
chatbot = Chat()

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
        ["🏠 Inicio", "🔧 Entrenar Modelo", "📊 Analizar Contraseña", "💬 Chatbot de Seguridad"]
    )
    
    if menu == "🔧 Entrenar Modelo":
        st.subheader("Entrenamiento del Modelo IA")
        st.write("El modelo se entrena con muestras de contraseñas débiles y fuertes para mejorar su precisión en la clasificación.")
        if st.button("🚀 Iniciar Entrenamiento"):
            try:
                X, y = model.generate_training_data()
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

                model.model = RandomForestClassifier(n_estimators=100)
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                training_panel = st.empty()

                acc_history = []

                def create_training_panel(epoch, accuracy, feature_importances):
                    feature_bars = "\n".join([
                        f"Longitud   {'▮' * int(fi * 40)} {fi * 100:.1f}%" for fi in feature_importances
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

                for epoch in range(1, 101):
                    model.model.fit(X_train, y_train)
                    acc = model.model.score(X_test, y_test)
                    acc_history.append(acc)
                    fi = getattr(model.model, 'feature_importances_', [0.35, 0.25, 0.20, 0.15, 0.05])
                    
                    progress_bar.progress(epoch / 100)
                    status_text.text(f"Época: {epoch} - Precisión: {acc:.2%}")
                    training_panel.code(create_training_panel(epoch, acc, fi))
                    
                    time.sleep(0.1)
                
                joblib.dump(model.model, "local_pass_model.pkl")
                st.success(f"Modelo entrenado! Precisión: {acc:.2%}")
                st.balloons()

                st.subheader("📊 Evolución de la Precisión")
                plt.plot(range(1, 101), acc_history, marker='o')
                plt.xlabel("Épocas")
                plt.ylabel("Precisión")
                plt.title("Precisión del Modelo a lo Largo del Entrenamiento")
                st.pyplot(plt)
            except Exception as e:
                st.error(f"Error en entrenamiento: {str(e)}")
    
    elif menu == "📊 Analizar Contraseña":
        st.subheader("Analizador de Seguridad")
        st.write("Este módulo evalúa la seguridad de una contraseña dada en base a un modelo de IA.")
        password = st.text_input("Introduce una contraseña para analizar:", type="password")
        
        if password:
            if model.model is None:
                st.error("Primero entrena el modelo!")
            else:
                try:
                    score = model.model.predict_proba([model.extract_features(password)])[0][1] * 100
                    st.metric("Puntuación de Seguridad", f"{score:.1f}%")
                except Exception as e:
                    st.error(f"Error en análisis: {str(e)}")
    
    elif menu == "💬 Chatbot de Seguridad":
        st.subheader("💬 Chatbot de Seguridad - WildPass AI")
        st.write("Habla con el chatbot sobre la seguridad de tus contraseñas.")
        chat_input = st.text_input("Escribe tu pregunta sobre seguridad de contraseñas:")
        
        if st.button("Enviar"):
            if chat_input:
                with st.spinner("Pensando..."):
                    response = chatbot.send_message(chat_input)
                    st.write("**Chatbot:**", response.text)
            else:
                st.warning("Por favor, escribe una pregunta primero.")

if __name__ == "__main__":
    main()
