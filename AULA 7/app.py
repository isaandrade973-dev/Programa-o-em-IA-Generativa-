import streamlit as st

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Classificador de Chamados",
    page_icon="🏷️",
    layout="centered"
)

st.title("🏷️ Classificador Automático de Chamados")
st.write("Digite a mensagem do cliente para direcioná-la ao setor correto.")

# ==========================================
# 2. DICIONÁRIOS DE PALAVRAS-CHAVE
# ==========================================
PALAVRAS_TECNICO = [
    "erro", "bug", "sistema", "login", "senha", "acesso", 
    "lentidao", "lento", "trava", "travando", "tela", "app", 
    "aplicativo", "carrega", "desconecta", "servidor"
]

PALAVRAS_FINANCEIRO = [
    "fatura", "boleto", "pagamento", "paguei", "cobrança", 
    "cobrança", "valor", "preço", "reembolso", "estorno", 
    "desconto", "nota fiscal", "pix", "cartao", "cartão", "vencimento"
]

# ==========================================
# 3. FUNÇÃO DE CLASSIFICAÇÃO
# ==========================================
def classificar_mensagem(mensagem):
    # Padroniza o texto para letras minúsculas
    texto = mensagem.lower()
    
    # Conta a quantidade de termos encontrados de cada setor
    termos_tecnico = [p for p in PALAVRAS_TECNICO if p in texto]
    termos_financeiro = [p for p in PALAVRAS_FINANCEIRO if p in texto]
    
    score_tecnico = len(termos_tecnico)
    score_financeiro = len(termos_financeiro)
    
    # Regras condicionais para determinar o setor
    if score_tecnico > score_financeiro:
        setor = "Suporte Técnico"
    elif score_financeiro > score_tecnico:
        setor = "Financeiro"
    elif score_tecnico > 0 and score_tecnico == score_financeiro:
        setor = "Atendimento Geral (Empate)"
    else:
        setor = "Atendimento Geral (Não identificado)"
        
    return setor, termos_tecnico, termos_financeiro

# ==========================================
# 4. INTERFACE DO USUÁRIO
# ==========================================
# Mensagem de exemplo pré-carregada
exemplo = "Não consigo fazer o login no sistema e o app fica travando na tela inicial."

mensagem_input = st.text_area(
    "Insira a mensagem do cliente:",
    value=exemplo,
    height=120
)

if st.button("Classificar Mensagem", type="primary"):
    if not mensagem_input.strip():
        st.warning("Por favor, digite uma mensagem para classificar.")
    else:
        setor, termos_tec, termos_fin = classificar_mensagem(mensagem_input)
        
        st.markdown("---")
        st.subheader("Resultado do Direcionamento:")
        
        # Exibição do setor com destaque visual
        if setor == "Suporte Técnico":
            st.success(f"🛠️ **Setor Destino:** {setor}")
        elif setor == "Financeiro":
            st.info(f"💳 **Setor Destino:** {setor}")
        else:
            st.warning(f"🎧 **Setor Destino:** {setor}")
            
        # Detalhes das palavras-chave encontradas
        st.markdown("### Detalhes da Análise:")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Termos de Suporte Técnico:**")
            if termos_tec:
                for t in termos_tec:
                    st.write(f"- `{t}`")
            else:
                st.write("*Nenhum termo encontrado*")
                
        with col2:
            st.write("**Termos do Financeiro:**")
            if termos_fin:
                for f in termos_fin:
                    st.write(f"- `{f}`")
            else:
                st.write("*Nenhum termo encontrado*")

# Painel lateral explicativo
with st.sidebar:
    st.header("💡 Regras de Classificação")
    st.markdown("""
    - **Suporte Técnico:** Acionado se houver mais palavras associadas a falhas, acessos ou uso da plataforma.
    - **Financeiro:** Acionado se houver mais palavras ligadas a boletos, pagamentos e cobranças.
    - **Atendimento Geral:** Acionado se houver empate ou se nenhum termo conhecido for identificado.
    """)