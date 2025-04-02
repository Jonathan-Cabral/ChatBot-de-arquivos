import tempfile
import os
from time import sleep
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from loaders import *


TIPOS_ARQUIVOS_VALIDOS = [ 
    'Site', 'YouTube', 'PDF', 'CSV', 'TXT'
]
CONFIG_MODELOS = {'Groq' : {'modelos': ['gemma2-9b-it', 'llama-3.3-70b-versatile', 'deepseek-r1-distill-llama-70b'], 'chat': ChatGroq},
                  'DeepSeek': {'modelos': ['deepseek-r1:7b'], 'chat': ChatOllama }, #PARA MODELOS BAIXADOS LOCALMENTE COM OLLAMA
                  'OpenAi': {'modelos': ['gpt-4o-mini', 'gpt-4o'], 'chat': ChatOpenAI}}

MEMORIA = ConversationBufferMemory()

FILE_ICONS = {
    'PDF': "📄",
    'TXT': "📝",
    'CSV': "📊",
    'Site': "🌐",
    'YouTube': "▶️"
}

ICONS_IA = {
    "OpenAi": "🟢", 
    "Groq": "🟣",
    "DeepSeek": "🔵"
}

def aplicar_estilos():

    st.markdown("""
    <style>
    /* Universal text colors for better visibility */
    .st-emotion-cache-1gulkj5 h1,
    .st-emotion-cache-1gulkj5 h2,
    .st-emotion-cache-1gulkj5 h3,
    .st-emotion-cache-1gulkj5 h4,
    .st-emotion-cache-1gulkj5 p,
    .st-emotion-cache-1gulkj5 li,
    .st-emotion-cache-1gulkj5 span,
    .st-emotion-cache-1gulkj5 div,
    .st-emotion-cache-uf99v8 h1,
    .st-emotion-cache-uf99v8 h2,
    .st-emotion-cache-uf99v8 h3,
    .st-emotion-cache-uf99v8 h4,
    .st-emotion-cache-uf99v8 p,
    .st-emotion-cache-uf99v8 li,
    .st-emotion-cache-uf99v8 span,
    .st-emotion-cache-uf99v8 div {
        color: currentColor !important;
    }
    
    /* Cross-compatibility for cards */
    .card {
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        border-radius: 10px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Ensure dark mode cards have proper background */
    [data-theme="dark"] .card {
        background-color: rgba(80, 80, 80, 0.2) !important;
    }
    
    /* Ensure light mode cards have proper background */
    [data-theme="light"] .card {
        background-color: rgba(255, 255, 255, 0.8) !important;
    }
    
    /* File indicator styling */
    .file-indicator {
        display: inline-block !important;
        padding: 5px 15px !important;
        background-color: #4287f5 !important;
        color: white !important;
        border-radius: 20px !important;
        font-size: 14px !important;
        margin-bottom: 20px !important;
    }
    
    /* File preview styling with contrast for both themes */
    .file-preview {
        padding: 10px !important;
        border-radius: 8px !important;
        margin-top: 10px !important;
        border: 1px solid rgba(128, 128, 128, 0.3) !important;
    }
    
    /* Ensure dark mode file previews have proper background */
    [data-theme="dark"] .file-preview {
        background-color: rgba(80, 80, 80, 0.2) !important;
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Ensure light mode file previews have proper background */
    [data-theme="light"] .file-preview {
        background-color: rgba(240, 240, 240, 0.8) !important;
        color: rgba(0, 0, 0, 0.8) !important;
    }
    
    /* Cross-compatible button styling */
    .custom-button {
        background-color: #4287f5 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        width: 100% !important;
    }
    
    .custom-button:hover {
        background-color: #05c46b !important;
    }
    
    /* Provider badge styling */
    .provider-badge {
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        border-radius: 8px !important;
        border: 1px solid rgba(128, 128, 128, 0.3) !important;
        padding: 10px !important;
        margin: 10px 0 !important;
    }
    
    /* Ensure dark mode provider badges have proper background */
    [data-theme="dark"] .provider-badge {
        background-color: rgba(80, 80, 80, 0.2) !important;
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Ensure light mode provider badges have proper background */
    [data-theme="light"] .provider-badge {
        background-color: rgba(240, 240, 240, 0.8) !important;
        color: rgba(0, 0, 0, 0.8) !important;
    }
    
    /* Empty chat styling */
    .empty-chat {
        text-align: center !important;
        padding: 60px 0 !important;
        color: rgba(128, 128, 128, 0.7) !important;
    }
    
    /* Welcome card styling */
    .welcome-card {
        text-align: center !important;
        padding: 40px 20px !important;
        border-radius: 10px !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        margin-bottom: 20px !important;
    }
    
    /* Ensure dark mode welcome cards have proper background */
    [data-theme="dark"] .welcome-card {
        background-color: rgba(80, 80, 80, 0.2) !important;
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Ensure light mode welcome cards have proper background */
    [data-theme="light"] .welcome-card {
        background-color: rgba(240, 240, 240, 0.8) !important;
        color: rgba(0, 0, 0, 0.8) !important;
    }
    
    /* Override Streamlit's chat message styling for better visibility */
    .st-emotion-cache-13y2inf.exg6vvm15 {
        color: currentColor !important;
    }
    
    /* Ensure sidebar elements are visible */
    .st-emotion-cache-16txtl3 h1,
    .st-emotion-cache-16txtl3 h2,
    .st-emotion-cache-16txtl3 h3,
    .st-emotion-cache-16txtl3 h4,
    .st-emotion-cache-16txtl3 p,
    .st-emotion-cache-16txtl3 span,
    .st-emotion-cache-16txtl3 div,
    .st-emotion-cache-16txtl3 label,
    .st-emotion-cache-16txtl3 .stRadio label,
    .st-emotion-cache-16txtl3 .stCheckbox label,
    .st-emotion-cache-16txtl3 .stSelectbox label,
    .st-emotion-cache-183lzff label {
        color: currentColor !important;
    }
    
    /* Force visibility for all text elements */
    div, p, h1, h2, h3, h4, h5, h6, span, label {
        color: currentColor !important;
    }
    
    /* Ensure headers are visible */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* Use a compatible strategy for chat messages */
    .stChatMessage {
        border-radius: 8px !important;
        margin-bottom: 10px !important;
        padding: 5px !important;
    }
    
    /* Override specific streamlit element classes to ensure visibility */
    .st-emotion-cache-q8sbsg p,
    .st-emotion-cache-q8sbsg span,
    .st-emotion-cache-q8sbsg div,
    .st-emotion-cache-1v0mbdj p,
    .st-emotion-cache-1v0mbdj span,
    .st-emotion-cache-1v0mbdj div {
        color: currentColor !important;
    }
    </style>
    """, unsafe_allow_html=True)

def carrega_arquivo(tipo_arquivo, arquivo):
    with st.spinner(f'Carregando arquivo {tipo_arquivo}...'):
        if tipo_arquivo == 'Site':
            documento = carrega_site(arquivo)
            
        if tipo_arquivo == 'YouTube':
            documento = carrega_youtube(arquivo)
            
        if tipo_arquivo == 'PDF':
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
                temp.write(arquivo.read())
                nome_temp = temp.name     
            documento = carrega_pdf(nome_temp)
            
        if tipo_arquivo == 'CSV':
            with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
                temp.write(arquivo.read())
                nome_temp = temp.name     
            documento = carrega_csv(nome_temp)
            
        if tipo_arquivo == 'TXT':
            with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp:
                temp.write(arquivo.read())
                nome_temp = temp.name     
            documento = carrega_txt(nome_temp)  
            
    return documento

def carrega_modelo(provedor, modelo, api_key, tipo_arquivo, arquivo):
 
    documento = carrega_arquivo(tipo_arquivo, arquivo)  
        
    system_message = '''Você é um assistente amigável que utiliza arquivos do usuario como base de conhecimento.
Você possui acesso às seguintes informações vindas 
de um documento {}: 

####
{}
####

Utilize as informações fornecidas para basear as suas respostas.

Sempre que houver $ na sua saída, substita por S.

Se a informação do documento for algo como "Just a moment...Enable JavaScript and cookies to continue" 
sugira ao usuário carregar novamente o Assistente!'''.format(tipo_arquivo, documento)

    template = ChatPromptTemplate.from_messages([
        ('system', system_message),
        ('placeholder', '{chat_history}'),
        ('user', '{input}')
    ])
    print(system_message)
      
    chat = CONFIG_MODELOS[provedor]['chat'](model=modelo, api_key=api_key)
    chain = template | chat
    st.session_state['chain'] = chain
    st.session_state['document_type'] = tipo_arquivo

    st.success(f"✅ Assistente carregado com sucesso usando modelo {modelo}!")

def show_file_preview(file_name, file_type):
    icon = FILE_ICONS.get(file_type, "📄")
    
    st.markdown(f"""
    <div class="file-preview">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 24px;">{icon}</span>
            <span>{file_name}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_welcome_screen():
    st.markdown("""
    <div class="welcome-card">
        <h2>👋 Bem-vindo ao Assistente de Arquivos IA!</h2>
        <p>Este assistente permite que você converse com seus arquivos usando IA.</p>
        <p>Para começar, carregue um arquivo e um modelo IA no painel lateral.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h3>📌 Dicas para usar o assistente:</h3>
        <p>1. Selecione o tipo de arquivo ou site que deseja carregar</p>
        <p>2. Escolha um provedor e modelo de IA e adicione sua API</p>
        <p>3. Faça perguntas específicas sobre o conteúdo do seu arquivo</p>
        <p>4. O assistente fornecerá respostas baseadas no arquivo carregado</p>
    </div>
    """, unsafe_allow_html=True)

def pagina_chat():
    aplicar_estilos()
    
    st.markdown('<div style="display: flex; align-items: center; margin-bottom: 20px;"><span style="font-size: 28px; margin-right: 10px;">🤖</span><h1>Assistente de Arquivos IA</h1></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <p>Este assistente permite que você converse com seus arquivos. Carregue um arquivo e um modelo de IA para começar.</p>
    </div>
    """, unsafe_allow_html=True)
    
    chain = st.session_state.get('chain')
    if chain is None:
        show_welcome_screen()
        st.stop()

    document_type = st.session_state.get('document_type', '')
    if document_type:
        st.markdown(f"""
        <div class="file-indicator">
            {FILE_ICONS.get(document_type, "📄")} Arquivo {document_type} carregado
        </div>
        """, unsafe_allow_html=True)

    chat_container = st.container()
    
    with chat_container:
        memoria = st.session_state.get('memoria', MEMORIA)

        if not memoria.buffer_as_messages:
            st.markdown("""
            <div class="empty-chat">
                <p>Nenhuma mensagem ainda. Comece a conversar!</p>
            </div>
            """, unsafe_allow_html=True)

        for mensagem in memoria.buffer_as_messages:
            chat = st.chat_message(mensagem.type)
            chat.markdown(mensagem.content)
    
    # Chat input
    input_usuario = st.chat_input('Pergunte sobre seu arquivo...')
    
    if input_usuario:
        memoria.chat_memory.add_user_message(input_usuario)
        chat = st.chat_message('human')
        chat.markdown(input_usuario)
        
        chat = st.chat_message('ai')
        with st.spinner('Pensando...'):
            resposta = chat.write_stream(chain.stream({'input': input_usuario, 'chat_history': memoria.buffer_as_messages})) 
        memoria.chat_memory.add_ai_message(resposta)
        
        st.session_state['memoria'] = memoria

def sidebar():
    st.sidebar.markdown("<h2>Configurações</h2>", unsafe_allow_html=True)
    tab1, tab2 = st.sidebar.tabs(["📄 Arquivo", "🤖 Modelo"])
    
    with tab1:
        st.markdown("<h3>Selecione seu arquivo</h3>", unsafe_allow_html=True)
        
        tipo_arquivo = st.selectbox('Tipo de arquivo', TIPOS_ARQUIVOS_VALIDOS)

        if tipo_arquivo == 'Site':
            arquivo = st.text_input('URL do Site', placeholder="https://exemplo.com")
            if arquivo:
                show_file_preview(arquivo, tipo_arquivo)
                
        elif tipo_arquivo == 'YouTube':
            arquivo = st.text_input('URL do Vídeo', placeholder="https://youtube.com/watch?v=...")
            if arquivo:
                show_file_preview(arquivo, tipo_arquivo)
                
        elif tipo_arquivo == 'PDF':
            arquivo = st.file_uploader('Upload de arquivo PDF', type=['pdf'])
            if arquivo:
                show_file_preview(arquivo.name, tipo_arquivo)
                
        elif tipo_arquivo == 'TXT':
            arquivo = st.file_uploader('Upload de arquivo TXT', type=['txt'])
            if arquivo:
                show_file_preview(arquivo.name, tipo_arquivo)
                
        elif tipo_arquivo == 'CSV':
            arquivo = st.file_uploader('Upload de arquivo CSV', type=['csv'])
            if arquivo:
                show_file_preview(arquivo.name, tipo_arquivo)
    
    with tab2:
        st.markdown("<h3>Configuração do modelo</h3>", unsafe_allow_html=True)
        
        provedor = st.selectbox('Selecione o provedor', CONFIG_MODELOS.keys())

        st.markdown(f"""
        <div class="provider-badge">
            <span style="font-size: 24px;">{ICONS_IA.get(provedor, "🤖")}</span>
            <div>
                <div style="font-weight: bold;">{provedor}</div>
                <div style="opacity: 0.7;">Provedor de IA</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        modelo = st.selectbox('Selecione o modelo', CONFIG_MODELOS[provedor]['modelos'])
        
        # API Key input
        api_key = st.text_input(
            f'API Key ({provedor})', 
            value=st.session_state.get(f'api_key_{provedor}', ''),
            type="password",
            help=f"Insira sua chave de API para {provedor}"
        )

        st.session_state[f'api_key_{provedor}'] = api_key

    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button('🚀 Carregar Assistente', use_container_width=True):
            if 'arquivo' not in locals() or not arquivo:
                st.sidebar.error("Por favor, selecione um arquivo")
            elif not api_key:
                st.sidebar.error("API key é necessária")
            else:
                with st.spinner("Carregando modelo..."):
                    carrega_modelo(provedor, modelo, api_key, tipo_arquivo, arquivo)
    
    with col2:
        if st.button('🗑️ Limpar Histórico', use_container_width=True):
            st.session_state['memoria'] = MEMORIA
            st.sidebar.success("Histórico de conversa apagado!")

def main():

    st.set_page_config(
        page_title="Assistente de Arquivos IA",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    with st.sidebar:
        sidebar()
    
    pagina_chat()

if __name__ == '__main__':
    main()