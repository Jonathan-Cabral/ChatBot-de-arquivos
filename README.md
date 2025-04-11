# 🤖 Assistente de Arquivos IA

O Assistente de Arquivos IA é uma aplicação Streamlit que permite conversar com seus arquivos usando inteligência artificial. A aplicação suporta diversos formatos de arquivos e modelos de IA para criar uma experiência interativa de perguntas e respostas baseada no conteúdo dos seus documentos.

## ✨ Funcionalidades

- **Suporte a múltiplos formatos**: PDF, TXT, CSV, sites web e vídeos do YouTube
- **Integração com várias APIs de IA**
- **Interface de chat intuitiva**: Faça perguntas sobre o conteúdo dos seus arquivos
- **Personalização de modelos**: Escolha entre diversos modelos de IA disponíveis
- **Design responsivo**: Compatível com modo claro e escuro

## 🚀 Como usar

1. **Instale as dependências**:
   ```
   pip install -r requirements.txt
   ```

2. **Execute a aplicação**:
   ```
   streamlit run app.py
   ```

3. **Carregue um arquivo**:
   - Selecione o tipo de arquivo (PDF, TXT, CSV, Site ou YouTube)
   - Faça upload do arquivo ou forneça a URL

4. **Configure o modelo de IA**:
   - Escolha o provedor 
   - Selecione o modelo específico
   - Insira sua chave de API

5. **Comece a conversar**:
   - Clique em "Carregar Assistente"
   - Faça perguntas sobre o conteúdo do arquivo

## 📝 Suporte a arquivos

- **📄 PDF**: Documentos, relatórios, artigos
- **📝 TXT**: Arquivos de texto simples
- **📊 CSV**: Dados tabulares
- **🌐 Site**: Conteúdo de páginas web
- **▶️ YouTube**: Transcrições de vídeos

## 🤖 Modelos suportados

### OpenAI
- gpt-4o-mini
- gpt-4o

### Groq
- gemma2-9b-it
- llama-3.3-70b-versatile
- deepseek-r1-distill-llama-70b

### DeepSeek (via Ollama)
- deepseek-r1:7b

## Você pode adicionar mais modelos conforme desejar

## 🔧 Estrutura do projeto

```
.
├── app.py               # Arquivo principal da aplicação
├── loaders.py           # Funções para carregar diferentes tipos de arquivos
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação
```

## 🔒 Segurança

As chaves de API são armazenadas apenas na sessão atual e não são persistidas. É recomendado não compartilhar sua aplicação em execução com outros usuários para evitar o vazamento de suas chaves de API.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.
