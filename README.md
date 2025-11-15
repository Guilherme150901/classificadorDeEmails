# 📧 Classificador de Emails com IA

## Descrição

Aplicação web que classifica emails em **Produtivo** ou **Improdutivo** e sugere uma **resposta automática**. Permite enviar **texto manual** ou **arquivos `.txt`/`.pdf`**.

---

## Funcionalidades Principais

- Envio de email via **texto ou arquivo**.
- Classificação automática:
  - **Produtivo:** exige ação ou resposta
  - **Improdutivo:** não exige ação imediata
- Resposta automática sugerida com base na categoria.
- Exibição do **texto original**, **categoria** e **resposta** na interface.
- Feedback visual:
  - Loading enquanto processa
  - Mensagens de erro se necessário

---

## Tecnologias Utilizadas

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (FastAPI), PyPDF2, python-dotenv
- **IA:** API Google Gemini (via `google.generativeai`)
- **Fallback:** Lógica local baseada em palavras-chave caso a API falhe.

---

## Como Usar (Teste Local)

Para executar o projeto localmente, você precisará de dois terminais.

1.  **Configurar a Chave da API (Arquivo .env):**
    Na **raiz** do projeto (na mesma pasta que o `requirements.txt`), crie um arquivo chamado `.env` e adicione sua chave do Gemini:

    ```
    GEMINI_API_KEY=SUA_CHAVE_API_AQUI
    ```

2.  **(Opcional) Instalar Dependências:**
    Se ainda não o fez, crie um ambiente virtual e instale as bibliotecas:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Executar o Backend (Terminal 1):**
    Na pasta raiz (com seu ambiente virtual ativo), execute o servidor FastAPI:

    ```bash
    uvicorn api.index:app --reload --port 8000
    ```

4.  **Executar o Frontend (Terminal 2):**
    Abra um _novo terminal_, navegue até a pasta `frontend` e inicie um servidor HTTP simples:

    ```bash
    cd frontend
    python -m http.server 5500
    ```

5.  **Abrir a interface web:**
    Abra seu navegador e acesse `http://localhost:5500`.

6.  **No formulário:**

    - Inserir o texto do email diretamente ou
    - Selecionar um arquivo `.txt` ou `.pdf`.

7.  **Clicar em Processar.**

8.  **A interface exibirá:**
    - O Texto Enviado (extraído do arquivo ou campo).
    - A Categoria do email (Produtivo/Improdutivo).
    - A Resposta automática sugerida.

---

## Autor

**Guilherme Andrade**

Atividade realizada para o processo seletivo da AutoU.
_Contato: gui15092001@gmail.com_
