import streamlit as st
import requests
import json

# ---------- CONFIGURAÇÃO GLOBAL ----------
st.set_page_config(page_title="NutraFlex", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #ffffff;
    }
    .main {
        background-color: #ffffff;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stButton > button {
        background-color: rgba(34, 139, 34, 0.75);
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton > button:hover {
        background-color: rgba(34, 139, 34, 0.95);
    }
    .menu-button {
        background-color: rgba(34, 139, 34, 0.1);
        border: none;
        color: #228B22;
        padding: 0.6rem 1.2rem;
        border-radius: 10px;
        font-weight: bold;
        margin-right: 0.5rem;
        margin-bottom: 1rem;
        cursor: pointer;
    }
    .menu-button:hover {
        background-color: rgba(34, 139, 34, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- BANCO DE USUÁRIOS (SIMPLIFICADO) ----------
users_db = {
    "teste@gmail.com": {"password": "123456"}
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------- FUNÇÃO DE LOGIN ----------
def login_screen():
    st.markdown("<h1 style='color:#228B22;'>NutraFlex</h1>", unsafe_allow_html=True)
    st.subheader("Acesse sua conta")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if email in users_db and users_db[email]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.email = email
        else:
            st.error("Credenciais inválidas")

# ---------- API DO GEMINI ----------
API_KEY = "AIzaSyA80-lpm2_GCi_Wdm7B-mcgzETFeSrszbw"

def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Erro: {response.status_code}\n{response.text}"

# ---------- INTERFACE PRINCIPAL ----------
def main_app():
    st.markdown("<h2 style='color:#228B22;'>NutraFlex — Seu Personal de Emagrecimento</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🧠 Personal Particular", key="menu1"):
            st.session_state.active_tab = "personal"
    with col2:
        if st.button("📅 Agenda Semanal", key="menu2"):
            st.session_state.active_tab = "agenda"
    with col3:
        if st.button("🛒 Produtos", key="menu3"):
            st.session_state.active_tab = "produtos"

    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "personal"

    # Aba 1 — Chat IA
    if st.session_state.active_tab == "personal":
        st.markdown("### 🧠 Personal Particular")
        st.info("Converse com seu coach virtual. Descreva seu objetivo, rotina e restrições.")
        for item in st.session_state.chat_history:
            st.markdown(f"**Você:** {item['user']}")
            st.markdown(f"**NutraFlex:** {item['bot']}")

        user_input = st.text_input("Digite sua mensagem:", key="chat_input")
        if st.button("Enviar"):
            if user_input:
                bot_reply = call_gemini(user_input)
                st.session_state.chat_history.append({"user": user_input, "bot": bot_reply})
                st.experimental_rerun()
            else:
                st.warning("Digite algo antes de enviar.")

    # Aba 2 — Agenda
    elif st.session_state.active_tab == "agenda":
        st.markdown("### 📅 Sua Agenda Semanal")
        st.success("Aqui será exibido seu plano semanal de dieta e treino baseado na conversa.")
        st.markdown("_(em breve com integração dinâmica)_")

    # Aba 3 — Produtos
    elif st.session_state.active_tab == "produtos":
        st.markdown("### 🛒 Produtos Recomendados")
        st.markdown("Confira abaixo os produtos indicados para sua jornada de emagrecimento:")
        st.markdown("- [Suplemento Natural X](https://seulink.com)")
        st.markdown("- [Ebook Receitas Low Carb](https://seulink.com)")
        st.markdown("- [Chá Detox Turbo](https://seulink.com)")

# ---------- EXECUÇÃO ----------
if not st.session_state.logged_in:
    login_screen()
else:
    main_app()
