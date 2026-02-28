import streamlit as st
import pandas as pd

# Configurações iniciais da página
st.set_page_config(
    page_title="Gerenciador de Identidade Visual IA",
    page_icon="🎨",
    layout="wide"
)

# Inicialização do "Banco de Dados" na sessão
if 'clientes' not in st.session_state:
    st.session_state.clientes = {}

# Função para criar o prompt baseado na identidade
def construir_prompt(nome, tema, cores, publico, estilo, total_refs):
    prompt = f"""
    [SYSTEM INSTRUCTION: VISUAL IDENTITY REPLICATION]
    CLIENTE: {nome}
    TEMA DA CAMPANHA: {tema}
    
    DIRETRIZES VISUAIS OBRIGATÓRIAS:
    - PALETA DE CORES: {cores} (Prevalência de tons pastéis e suaves).
    - ESTILO DE LUZ: High-key, iluminação natural, brilhante, sem sombras duras.
    - COMPOSIÇÃO: Minimalista, clean, com foco central no sujeito. 
    - AMBIENTE: {estilo} (Desfocado/Bokeh ao fundo para profundidade).
    - PÚBLICO: {publico}.
    
    DETALHES ADICIONAIS:
    - Manter a estética de "Cuidado com gostinho de brincadeira".
    - Integrar elementos lúdicos (como medalhas, brinquedos ou ícones amigáveis).
    - Tipografia sugerida: Sans Serif arredondada e moderna.
    - Baseado em análise de {total_refs} imagens de referência para consistência de layout.
    
    FORMATO: Fotorealista, 8k, estilo publicitário profissional.
    """
    return prompt

# --- INTERFACE LATERAL (ADMINISTRAÇÃO) ---
with st.sidebar:
    st.header("⚙️ Painel de Admin")
    st.subheader("Cadastrar Novo Cliente")
    
    with st.form("cadastro_cliente"):
        nome_cliente = st.text_input("Nome da Marca/Clínica")
        cores_base = st.text_input("Cores da Identidade", placeholder="Ex: Verde Menta, Rosa Pastel")
        publico_alvo = st.selectbox("Público-alvo", ["Infantil", "Adulto", "Estético/Premium", "Geral"])
        estilo_fundo = st.text_input("Ambiente de Fundo", value="Consultório moderno e acolhedor")
        
        # Upload de múltiplas referências para maior assertividade
        arquivos = st.file_uploader("Subir Imagens de Referência", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
        
        btn_salvar = st.form_submit_button("Salvar Perfil de Admin")
        
        if btn_salvar and nome_cliente:
            st.session_state.clientes[nome_cliente] = {
                "nome": nome_cliente,
                "cores": cores_base,
                "publico": publico_alvo,
                "estilo": estilo_fundo,
                "refs": len(arquivos) if arquivos else 0
            }
            st.success(f"Perfil de '{nome_cliente}' ativado!")

# --- ÁREA PRINCIPAL ---
st.title("🎨 Gerador de Temas por Identidade Visual")
st.markdown("Use este sistema para criar prompts de novas campanhas mantendo o padrão visual de cada cliente.")

if not st.session_state.clientes:
    st.info("👈 Por favor, cadastre um cliente no painel lateral para começar.")
else:
    # Seleção do Perfil
    col_sel, col_info = st.columns([1, 1])
    with col_sel:
        selecionado = st.selectbox("Selecione o Cliente Administrado:", list(st.session_state.clientes.keys()))
    
    cliente = st.session_state.clientes[selecionado]
    
    with col_info:
        st.caption(f"**Identidade Ativa:** {cliente['cores']} | **Referências:** {cliente['refs']} fotos.")

    st.divider()

    # Gerador de Novo Tema
    col_input, col_output = st.columns(2)

    with col_input:
        st.subheader("Novo Conteúdo")
        novo_tema = st.text_input("Qual o tema do novo post?", placeholder="Ex: Importância do Fio Dental")
        detalhes_extras = st.text_area("Observações para esta imagem específica", placeholder="Ex: Mostrar uma criança rindo com um fio dental colorido...")
        
        if st.button("✨ Gerar Prompt para Identidade"):
            if novo_tema:
                prompt_gerado = construir_prompt(
                    cliente['nome'], 
                    novo_tema, 
                    cliente['cores'], 
                    cliente['publico'], 
                    cliente['estilo'],
                    cliente['refs']
                )
                st.session_state.prompt_atual = prompt_gerado
            else:
                st.error("Por favor, digite um tema.")

    with col_output:
        st.subheader("Prompt para IA (Copy/Paste)")
        if 'prompt_atual' in st.session_state:
            st.code(st.session_state.prompt_atual, language="text")
            st.info("💡 Copie o código acima e cole no Midjourney, DALL-E ou Leonardo.ai")
        else:
            st.light("O prompt aparecerá aqui após você clicar em gerar.")

# Tabela de Gestão
with st.expander("📊 Visualizar Clientes Cadastrados"):
    if st.session_state.clientes:
        df = pd.DataFrame.from_dict(st.session_state.clientes, orient='index')
        st.table(df)