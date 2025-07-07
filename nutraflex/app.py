import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
import datetime
from PIL import Image

# Configuração da página
st.set_page_config(
    page_title="NutraFlex",
    page_icon="🏋️",
    layout="wide"
)

# Simulação de login (remova depois)
def simple_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        st.title("Bem-vindo ao NutraFlex")
        username = st.text_input("Nome de usuário")
        password = st.text_input("Senha", type="password")
        
        if st.button("Entrar"):
            if username and password:  # Verificação simples
                st.session_state.logged_in = True
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Por favor, preencha todos os campos")
        st.stop()

# Inicializar dados do usuário
def init_user_data():
    if "user_data" not in st.session_state:
        st.session_state.user_data = {
            "nome": "",
            "idade": "",
            "altura": "",
            "peso": "",
            "objetivo": "emagrecimento",
            "historico_chat": [],
            "agenda_exercicios": {},
            "plano_alimentar": {}
        }

# Configurar Gemini
def setup_gemini():
    if "model" not in st.session_state:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        st.session_state.model = genai.GenerativeModel('gemini-pro')

# Página de Perfil
def profile_page():
    st.title("👤 Seu Perfil")
    
    with st.form("perfil_form"):
        st.session_state.user_data["nome"] = st.text_input(
            "Nome Completo", 
            value=st.session_state.user_data["nome"]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.user_data["idade"] = st.number_input(
                "Idade", 
                min_value=12, max_value=100, 
                value=int(st.session_state.user_data["idade"]) if st.session_state.user_data["idade"] else 30
            )
        with col2:
            st.session_state.user_data["altura"] = st.number_input(
                "Altura (cm)", 
                min_value=100, max_value=250, 
                value=int(st.session_state.user_data["altura"]) if st.session_state.user_data["altura"] else 170
            )
        
        st.session_state.user_data["peso"] = st.number_input(
            "Peso (kg)", 
            min_value=30, max_value=300, 
            value=int(st.session_state.user_data["peso"]) if st.session_state.user_data["peso"] else 70
        )
        
        st.session_state.user_data["objetivo"] = st.selectbox(
            "Objetivo Principal",
            ["emagrecimento", "ganho de massa muscular", "manutenção", "melhora de condicionamento"],
            index=["emagrecimento", "ganho de massa muscular", "manutenção", "melhora de condicionamento"].index(
                st.session_state.user_data["objetivo"]
            ) if st.session_state.user_data["objetivo"] else 0
        )
        
        if st.form_submit_button("Salvar Perfil"):
            st.success("Perfil atualizado com sucesso!")

# Página do Personal
def personal_page():
    st.title("💬 Personal Virtual")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Olá! Sou seu Personal Virtual. Como posso te ajudar hoje?"}
        ]
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Digite sua mensagem..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    response = st.session_state.model.generate_content(
                        f"Você é um personal trainer/nutricionista. Dados do usuário: {st.session_state.user_data}. "
                        f"Responda de forma profissional e acolhedora sobre fitness e nutrição. "
                        f"Pergunta: {prompt}"
                    )
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error("Ocorreu um erro. Por favor, tente novamente.")

# Página de Agenda
def agenda_page():
    st.title("📅 Agenda de Exercícios")
    st.write("Sua programação semanal aparecerá aqui após conversar com o Personal.")
    
    if st.session_state.messages and len(st.session_state.messages) > 1:
        st.info("Interaja com o Personal Virtual para gerar sua agenda personalizada.")

# Página de Produtos
def produtos_page():
    st.title("🛍 Produtos Recomendados")
    st.write("Aqui estarão os produtos de afiliados para você.")
    
    # Exemplo de produto
    with st.expander("🥗 Shake Emagrecedor"):
        st.image("https://via.placeholder.com/300x200?text=Shake+NutraFlex", width=200)
        st.write("Shake proteico para auxílio no emagrecimento.")
        st.button("Comprar", key="shake_btn")

# App Principal
def main():
    simple_login()  # Remova quando implementar login real
    init_user_data()
    setup_gemini()
    
    with st.sidebar:
        st.image("assets/logo.png", width=150)
        st.markdown(f"### Olá, {st.session_state.user}!")
        
        selected = option_menu(
            menu_title="Menu",
            options=["Perfil", "Personal", "Agenda", "Produtos"],
            icons=["person", "chat", "calendar", "cart"],
            default_index=1,
            styles={
                "container": {"padding": "5px"},
                "icon": {"color": "#2e8b57", "font-size": "18px"},
                "nav-link": {"font-size": "16px", "text-align": "left"},
                "nav-link-selected": {"background-color": "#2e8b57"},
            }
        )
    
    if selected == "Perfil":
        profile_page()
    elif selected == "Personal":
        personal_page()
    elif selected == "Agenda":
        agenda_page()
    elif selected == "Produtos":
        produtos_page()

if __name__ == "__main__":
    main()