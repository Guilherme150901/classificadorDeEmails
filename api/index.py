import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from io import BytesIO

# Carrega variáveis de ambiente, como a chave da API Gemini
load_dotenv()

# Importa o modelo Pydantic usado como resposta da API
from app.modelos import ResultadoSaida

# Funções internas usadas para processamento do texto e classificação
from app.processamento import (
    pre_processar_texto,           # Limpa e normaliza o texto
    classificar_com_gemini,        # Classificação usando o modelo Gemini
    classificacao_alternativa_local, # Fallback sem IA
    configurar_gemini              # Configura a chave da API Gemini
)

# Função para extrair texto de arquivos PDF
from app.util_arquivos import extrair_texto_de_pdf

# Instancia a aplicação FastAPI
app = FastAPI()

# Libera requisições de qualquer origem (CORS) — necessário para o frontend funcionar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configura a API do Gemini se a chave estiver disponível no ambiente
CHAVE_GEMINI = os.getenv("GEMINI_API_KEY")
if CHAVE_GEMINI:
    configurar_gemini(CHAVE_GEMINI)

# Endpoint simples para verificar se a API está funcionando
@app.get("/api/health")
def verificar_saude():
    """Endpoint de verificação de status."""
    return {"status": "ok"}

# Endpoint principal que processa texto ou arquivo enviado pelo usuário
@app.post("/api/process", response_model=ResultadoSaida)
async def processar_email(
    texto: str = Form(None),     # Texto enviado diretamente pelo form
    file: UploadFile = File(None)  # Arquivo enviado (PDF e TXT)
):
    """
    Processa um email (via texto ou arquivo) para classificar
    e sugerir uma resposta.
    """
    
    # Caso o usuário não envie texto, tenta processar o arquivo
    if not texto and file:
        try:
            conteudo_arquivo = await file.read()  # Lê o arquivo enviado
        except:
            return JSONResponse(
                {"error": "Erro ao ler arquivo"},
                status_code=400
            )

        nome_arquivo = file.filename.lower()

        if nome_arquivo.endswith(".pdf"):
            # Extrai texto do PDF
            texto = extrair_texto_de_pdf(BytesIO(conteudo_arquivo))
        else:
            # Assume que é um arquivo de texto comum
            texto = conteudo_arquivo.decode("utf-8", errors="ignore").strip()

    # Se nenhum conteúdo foi enviado
    if not texto:
        return JSONResponse(
            {"error": "Nenhum conteúdo enviado"},
            status_code=400
        )

    # Limpa e pré-processa o texto antes da classificação
    texto_limpo = pre_processar_texto(texto)

    try:
        # Realiza classificação usando a IA Gemini
        resultado = classificar_com_gemini(texto_limpo)
    except Exception as e:
        # Caso a IA falhe, usa o classificador local como fallback
        print(f"Erro na API Gemini: {e}. Usando fallback local.")
        resultado = classificacao_alternativa_local(texto_limpo)

    # Retorna o resultado padronizado pelo modelo Pydantic
    return ResultadoSaida(
        categoria=resultado.get("categoria"),
        resposta=resultado.get("resposta"),
        texto_original=texto
    )
