
import streamlit as st
import requests
import json

# CONFIGURAÇÃO
st.set_page_config(page_title="NutraFlex", layout="wide")

# Sessão
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Banco de usuários simples (em produção use um banco de verdade)
users_db = {
    "teste@gmail.com": {"password": "123456"}
}

# Função para chamar a API da Gemini
def call_gemini(prompt, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={AIzaSyA80-lpm2_GCi_Wdm7B-mcgzETFeSrszbw}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Erro: {response.status_code}\n{response.text}"

# LOGIN
def login_screen():
    st.title("NutraFlex 🔐")
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if email in users_db and users_db[email]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.email = email
        else:
            st.error("Credenciais inválidas")

# TELA PRINCIPAL
def main_app():
    st.sidebar.title("NutraFlex")
    menu = st.sidebar.radio("Menu", ["Personal Particular", "Agenda Semanal", "Produtos"])

    st.sidebar.markdown("---")
    api_key = st.sidebar.text_input("API Key do Gemini", type="password")

    if menu == "Personal Particular":
        st.title("🧠 Personal Particular")
        st.write("Converse com seu coach de emagrecimento baseado em IA.")
        prompt = st.text_area("Digite sua dúvida ou objetivo:")
        if st.button("Enviar"):
            if api_key and prompt:
                resposta = call_gemini(prompt, api_key)
                st.success("Resposta:")
                st.write(resposta)
            else:
                st.warning("Digite a API Key e uma pergunta.")

    elif menu == "Agenda Semanal":
        st.title("📅 Sua Agenda Semanal")
        st.info("Aqui será exibido seu plano semanal de treino e alimentação. Em breve.")

    elif menu == "Produtos":
        st.title("🛒 Produtos Recomendados")
        st.markdown("Confira abaixo os produtos recomendados para seu objetivo:")
        st.write("- [Suplemento X](https://seulink.com)")
        st.write("- [Ebook de Receitas Fit](https://seulink.com)")
        st.write("- [Treinamento Emagreça Já](https://seulink.com)")

# RENDERIZAÇÃO
if not st.session_state.logged_in:
    login_screen()
else:
    main_app()
