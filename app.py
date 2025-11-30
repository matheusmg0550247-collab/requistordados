import streamlit as st
import requests
import json

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Requisição de Dados", page_icon="📈")

# --- 2. ESTILO DARK PERSONALIZADO (CSS) ---
st.markdown("""
<style>
    /* Fundo PRETO e texto BRANCO para o app inteiro */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* Força a cor branca em títulos e textos diversos */
    h1, h2, h3, p, div, label, span {
        color: #FFFFFF !important;
    }
    
    /* Estilizando as caixas de entrada (Input) para não sumirem no preto */
    /* Fundo cinza escuro (#262730), Borda branca suave, Texto branco */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea {
        background-color: #262730; 
        color: #FFFFFF;
        border: 1px solid #4a4a4a;
    }
    
    /* Quando clica na caixa de texto (foco) */
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #FFFFFF;
    }

    /* Estilo do Botão: Fundo BRANCO com letras PRETAS para destaque total */
    div.stButton > button {
        background-color: #FFFFFF;
        color: #000000;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }
    /* Efeito ao passar o mouse no botão */
    div.stButton > button:hover {
        background-color: #DDDDDD; /* Um cinza claro */
        color: #000000;
        border: 1px solid #FFFFFF;
    }
    
    /* Ajuste da cor da seleção do Radio Button */
    div[role="radiogroup"] label {
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CABEÇALHO E IMAGEM ---
col1, col2 = st.columns([1, 3])

with col1:
    try:
        # Tenta carregar a imagem do Matheus
        st.image("Matheus.png", width=120)
    except:
        # Se não achar, mostra um emoji
        st.header("👤")

with col2:
    st.title("Central de Requisições")
    st.write("Responsável: Matheus")

st.markdown("---")

# --- 4. FORMULÁRIO ---
st.subheader("Dados do Solicitante")

nome = st.text_input("Nome Completo")
setor = st.text_input("Setor")

st.subheader("Tipo de Solicitação")

# --- SELEÇÃO COM A NOVA OPÇÃO "PRODUTIVIDADE" ---
tipo_solicitacao = st.radio(
    "Selecione a categoria:",
    options=["Controle de Acervo", "Produtividade", "Contrafé"], # Ordem atualizada
    horizontal=True
)

# Variável para guardar o número do processo (padrão é traço)
num_processo = "-"

# Lógica Condicional: Só mostra campo de processo se for "Contrafé"
if tipo_solicitacao == "Contrafé":
    num_processo = st.text_input("Digite o Número do Processo:", placeholder="Ex: 1.0000.24...")
    if not num_processo:
        st.warning("⚠️ Para Contrafé, é necessário informar o número.")

# Campo para detalhes extras
detalhes = st.text_area("Descreva sua solicitação", height=100, placeholder="Ex: Detalhes do relatório, período, dúvidas...")

st.markdown("<br>", unsafe_allow_html=True)

# --- 5. BOTÃO E ENVIO ---
if st.button("ENVIAR SOLICITAÇÃO"):
    
    # Validação de campos obrigatórios
    erro = False
    
    if not nome or not setor:
        st.error("❌ Por favor, preencha seu Nome e Setor.")
        erro = True
        
    if tipo_solicitacao == "Contrafé" and (not num_processo or num_processo == "-"):
        st.error("❌ O número do processo é obrigatório para solicitações de Contrafé.")
        erro = True
    
    # Se não houver erros, envia para o Google Chat
    if not erro:
        webhook_url = "https://chat.googleapis.com/v1/spaces/AAQAtWfirl8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=wNSRzU6KYdXa3U1l6y6ew1FVVtY746ep6c1j-WneE1k"
        
        # Ícones para cada tipo
        icone_tipo = "📂"
        if tipo_solicitacao == "Produtividade": icone_tipo = "🚀"
        if tipo_solicitacao == "Contrafé": icone_tipo = "⚖️"

        # Montagem da mensagem
        msg_final = (
            f"🚨 *NOVA REQUISIÇÃO RECEBIDA*\n"
            f"──────────────────────\n"
            f"👤 *Solicitante:* {nome}\n"
            f"🏢 *Setor:* {setor}\n"
            f"{icone_tipo} *Tipo:* {tipo_solicitacao}\n"
        )
        
        # Adiciona linha do processo apenas se existir
        if tipo_solicitacao == "Contrafé":
            msg_final += f"📄 *Processo:* {num_processo}\n"
            
        msg_final += f"📝 *Obs:* {detalhes}"

        # Preparando envio JSON
        payload = {"text": msg_final}
        headers = {"Content-Type": "application/json; charset=UTF-8"}
        
        try:
            r = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
            
            if r.status_code == 200:
                st.success("✅ Solicitação enviada com sucesso!")
                st.balloons()
            else:
                st.error(f"Erro ao enviar: {r.text}")
                
        except Exception as e:
            st.error(f"Erro de conexão: {e}")
