import streamlit as st
import requests
import json

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Requisição de Dados", page_icon="📊")

# --- TÍTULO E IMAGEM ---
st.title("Requisição de dados")

# Tenta carregar a imagem localmente ou do GitHub
# DICA: Quando subir no GitHub, o Streamlit Cloud lê o arquivo se estiver na mesma pasta.
try:
    # Substitua 'Matheus.png' pela extensão correta (.jpg, .jpeg) se for diferente
    st.image("Matheus.png", caption="Responsável: Matheus", width=200) 
except:
    st.warning("Imagem 'Matheus.png' não encontrada. Verifique o nome do arquivo no GitHub.")

st.markdown("---")

# --- FORMULÁRIO DE REQUISIÇÃO ---
with st.form("form_requisicao"):
    st.write("Preencha os dados abaixo para abrir um chamado:")
    
    nome = st.text_input("Seu Nome")
    setor = st.text_input("Seu Setor")
    detalhes = st.text_area("O que você precisa?", placeholder="Ex: Preciso da planilha de vendas consolidada de 2024...")
    
    # Botão de envio
    enviar = st.form_submit_button("Enviar Solicitação")

    # --- LÓGICA DE ENVIO ---
    if enviar:
        if not nome or not setor:
            st.error("Por favor, preencha o Nome e o Setor.")
        else:
            # URL do Webhook (Google Chat)
            webhook_url = "https://chat.googleapis.com/v1/spaces/AAQAtWfirl8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=wNSRzU6KYdXa3U1l6y6ew1FVVtY746ep6c1j-WneE1k"
            
            # Formata a mensagem para o Google Chat
            mensagem_chat = (
                f"🚨 *NOVA REQUISIÇÃO DE DADOS*\n\n"
                f"👤 *Solicitante:* {nome}\n"
                f"🏢 *Setor:* {setor}\n"
                f"📝 *Pedido:* {detalhes}"
            )
            
            payload = {"text": mensagem_chat}
            headers = {"Content-Type": "application/json; charset=UTF-8"}

            try:
                response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
                
                if response.status_code == 200:
                    st.success("✅ Solicitação enviada com sucesso para o Google Chat!")
                else:
                    st.error(f"Erro ao enviar: {response.text}")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")
