# app.py
import streamlit as st
import joblib
import numpy as np
import string
import random
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="WildPass Pro",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Estilos del chat
st.markdown("""
<style>
.chat-container {
    max-height: 500px;
    overflow-y: auto;
    padding: 20px;
    background: #f5f5f5;
    border-radius: 10px;
    margin-bottom: 20px;
}
.user-message {
    background: #DCF8C6;
    padding: 10px;
    border-radius: 15px;
    margin: 5px 0;
    max-width: 70%;
    float: right;
    clear: both;
}
.bot-message {
    background: white;
    padding: 10px;
    border-radius: 15px;
    margin: 5px 0;
    max-width: 70%;
    float: left;
    clear: both;
}
.timestamp {
    font-size: 0.7em;
    color: #666;
    margin-top: 3px;
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
            st.success("✅ Modelo de seguridad cargado!")
        except Exception:
            st.warning("⚠ Modelo no encontrado, entrénalo primero")
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

    def generate_training_data(self, samples=1000):
        X = []
        y = []
        for _ in range(samples//2):
            X.append(self.extract_features(self.generate_weak_password()))
            y.append(0)
            X.append(self.extract_features(self.generate_strong_password()))
            y.append(1)
        return np.array(X), np.array(y)

    def extract_features(self, password):
        return [
            len(password),
            sum(c.isupper() for c in password),
            sum(c.isdigit() for c in password),
            sum(c in string.punctuation for c in password),
            len(set(password))/max(len(password), 1)
        ]

    def train_model(self):
        try:
            X, y = self.generate_training_data()
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

            self.model = RandomForestClassifier(n_estimators=100)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            training_panel = st.empty()

            def create_training_panel(epoch, accuracy, feature_importances):
                feature_bars = "\n".join([
                    f"Longitud   {'▮' * int(fi[0]*40)} {fi[0]*100:.1f}%",
                    f"Mayúsculas {'▮' * int(fi[1]*40)} {fi[1]*100:.1f}%",
                    f"Dígitos    {'▮' * int(fi[2]*40)} {fi[2]*100:.1f}%",
                    f"Símbolos   {'▮' * int(fi[3]*40)} {fi[3]*100:.1f}%",
                    f"Unicidad   {'▮' * int(fi[4]*40)} {fi[4]*100:.1f}%"
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
                self.model.fit(X_train, y_train)
                acc = self.model.score(X_test, y_test)
                fi = self.model.feature_importances_ if hasattr(self.model, 'feature_importances_') else [0.35, 0.25, 0.20, 0.15, 0.05]
                
                progress_bar.progress(epoch/100)
                status_text.text(f"Época: {epoch} - Precisión: {acc:.2%}")
                training_panel.code(create_training_panel(epoch, acc, fi))
                time.sleep(0.05)

            joblib.dump(self.model, "local_pass_model.pkl")
            st.success(f"🎉 Modelo entrenado! Precisión: {acc:.2%}")
            return True
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            return False

def chat_interface():
    st.subheader("💬 Chat de Seguridad")
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for msg in st.session_state.chat_history:
            if msg['type'] == 'user':
                st.markdown(f'''
                <div class="user-message">
                    {msg["content"]}
                    <div class="timestamp">{msg["time"]}</div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="bot-message">
                    {msg["content"]}
                    <div class="timestamp">{msg["time"]}</div>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        user_input = st.text_input("Escribe tu mensaje:", key="chat_input")
        
        if st.button("Enviar") or user_input:
            if user_input:
                st.session_state.chat_history.append({
                    'type': 'user',
                    'content': user_input,
                    'time': datetime.now().strftime("%H:%M")
                })
                
                # Respuestas del bot
                respuestas = {
                    'hola': '¡Hola! Soy WildBot 🤖 ¿En qué puedo ayudarte?',
                    'ayuda': 'Puedo:\n🔸 Generar contraseñas seguras\n🔸 Analizar tu contraseña\n🔸 Entrenar el modelo IA\n🔸 Dar consejos de seguridad',
                    'seguridad': '🔒 Consejos de seguridad:\n1. 12+ caracteres\n2. Mayúsculas y minúsculas\n3. Números y símbolos\n4. Sin información personal',
                    'generar': 'Para generar:\n1. Ve a "🏠 Inicio"\n2. Click en "🔒 Generar"\n3. ¡Listo! 🎉',
                    'default': '🤖 No entendí. ¿Puedes reformularlo?'
                }
                
                respuesta = next((v for k, v in respuestas.items() if k in user_input.lower()), respuestas['default'])
                
                st.session_state.chat_history.append({
                    'type': 'bot',
                    'content': respuesta,
                    'time': datetime.now().strftime("%H:%M")
                })
                
                st.session_state.chat_input = ""
                st.experimental_rerun()

def main():
    st.title("🔐 WildPass Pro - Gestor de Contraseñas")
    st.markdown("---")
    
    model = PasswordModel()
    
    menu = st.sidebar.radio(
        "Menú Principal",
        ["🏠 Inicio", "📊 Analizar", "🔧 Entrenar IA", "💬 Chat"]
    )
    
    if menu == "🏠 Inicio":
        st.subheader("Generador de Contraseñas")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔒 Generar Fuerte"):
                password = model.generate_strong_password()
                st.code(password, language="text")
        
        with col2:
            if st.button("⚠ Generar Débil"):
                password = model.generate_weak_password()
                st.code(password, language="text")
    
    elif menu == "📊 Analizar":
        st.subheader("Analizador de Seguridad")
        password = st.text_input("Introduce una contraseña:", type="password")
        
        if password:
            if model.model is None:
                st.error("Primero entrena el modelo!")
            else:
                try:
                    features = model.extract_features(password)
                    score = model.model.predict_proba([features])[0][1] * 100
                    
                    st.metric("Puntuación de Seguridad", f"{score:.1f}%")
                    st.progress(score/100)
                    
                    st.json({
                        "Longitud": features[0],
                        "Mayúsculas": features[1],
                        "Dígitos": features[2],
                        "Símbolos": features[3],
                        "Unicidad": f"{features[4]*100:.1f}%"
                    })
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    elif menu == "🔧 Entrenar IA":
        st.subheader("Entrenamiento del Modelo")
        if st.button("🚀 Iniciar Entrenamiento"):
            with st.spinner("Entrenando IA..."):
                if model.train_model():
                    st.balloons()
    
    elif menu == "💬 Chat":
        chat_interface()

if __name__ == "__main__":
    main()
