import streamlit as st
import requests
import json

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Requisição de Dados", page_icon="tjmg-icon")

# --- 2. ESTILO PRETO E BRANCO (CSS) ---
# Isso força o visual clean: Fundo Branco, Texto Preto, Botão Preto.
st.markdown("""
<style>
    /* Fundo branco e texto preto */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }
    /* Entradas de texto com borda preta */
    .stTextInput > div > div > input {
        color: #000000;
        border-color: #000000;
    }
    /* Botão Preto com texto Branco */
    div.stButton > button {
        background-color: #000000;
        color: #FFFFFF;
        border: 1px solid #000000;
        border-radius: 5px;
    }
    div.stButton > button:hover {
        background-color: #333333;
        color: #FFFFFF;
        border-color: #333333;
    }
    /* Títulos em preto */
    h1, h2, h3 {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CABEÇALHO E IMAGEM ---
col1, col2 = st.columns([1, 3])

with col1:
    try:
        # Certifique-se de que a imagem Matheus.png está no GitHub
        st.image("Matheus.png", width=130)
    except:
        st.warning("Sem img")

with col2:
    st.title("Central de Requisições")
    st.write("Responsável: Matheus")

st.markdown("---")

# --- 4. FORMULÁRIO DE DADOS ---
# Usamos st.container para agrupar, mas sem st.form para permitir
# que o campo "Número do Processo" apareça instantaneamente.

st.subheader("Dados do Solicitante")
nome = st.text_input("Nome Completo")
setor = st.text_input("Setor")

st.subheader("Tipo de Solicitação")

# --- AQUI ESTÁ A LÓGICA PEDIDA ---
tipo_solicitacao = st.radio(
    "Selecione a categoria:",
    options=["Controle de Acervo", "Contrafé"],
    horizontal=True # Deixa as opções lado a lado
)

num_processo = "N/A" # Valor padrão

# Se escolher Contrafé, abre a caixa para digitar o processo
if tipo_solicitacao == "Contrafé":
    num_processo = st.text_input("Digite o Número do Processo:", placeholder="Ex: 1.0000.24...")
    if not num_processo:
        st.info("⚠️ Por favor, informe o número do processo para Contrafé.")

# Campo de mensagem adicional
detalhes = st.text_area("Observações Adicionais", height=100)

st.markdown("<br>", unsafe_allow_html=True)

# --- 5. BOTÃO DE ENVIO ---
if st.button("ENVIAR SOLICITAÇÃO"):
    
    # Validação simples
    erro = False
    if not nome or not setor:
        st.error("Preencha Nome e Setor.")
        erro = True
    if tipo_solicitacao == "Contrafé" and (not num_processo or num_processo == "N/A"):
        st.error("Para Contrafé, o número do processo é obrigatório.")
        erro = True
        
    if not erro:
        # URL do seu Webhook
        webhook_url = "https://chat.googleapis.com/v1/spaces/AAQAtWfirl8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=wNSRzU6KYdXa3U1l6y6ew1FVVtY746ep6c1j-WneE1k"
        
        # Monta a mensagem bonita para o Google Chat
        msg_final = (
            f"🚨 *NOVA REQUISIÇÃO RECEBIDA*\n"
            f"──────────────────────\n"
            f"👤 *Nome:* {nome}\n"
            f"🏢 *Setor:* {setor}\n"
            f"📂 *Tipo:* {tipo_solicitacao}\n"
        )
        
        # Adiciona o processo se for Contrafé
        if tipo_solicitacao == "Contrafé":
            msg_final += f"⚖️ *Processo:* {num_processo}\n"
            
        msg_final += f"📝 *Obs:* {detalhes}"

        # Envia
        payload = {"text": msg_final}
        headers = {"Content-Type": "application/json; charset=UTF-8"}
        
        try:
            r = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
            if r.status_code == 200:
                st.success("✅ Solicitação enviada com sucesso!")
                st.balloons() # Efeito visual legal
            else:
                st.error(f"Erro no envio: {r.text}")
        except Exception as e:
            st.error(f"Erro de conexão: {e}")
