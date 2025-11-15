import google.generativeai as genai
import re
import json
from typing import Dict, Any

def configurar_gemini(chave_api: str):
    """Configura a chave da API Gemini para permitir chamadas à IA."""
    genai.configure(api_key=chave_api)


def pre_processar_texto(texto: str) -> str:
    """
    Faz a limpeza básica do texto:
    - Converte para minúsculas
    - Remove múltiplos espaços
    - Normaliza o conteúdo
    """
    texto = texto.lower()
    texto = re.sub(r"\s+", " ", texto)  # Remove espaços extras e quebras de linha
    return texto.strip()


def classificar_com_gemini(texto_limpo: str) -> Dict[str, Any]:
    """
    Envia o texto para o modelo Gemini e solicita:
      1. Classificação do email (Produtivo ou Improdutivo)
      2. Geração de uma resposta curta e profissional
    Retorna sempre um JSON.
    
    Se o Gemini falhar ou retornar um JSON inválido,
    automaticamente usa o fallback local.
    """

    # Prompt enviado ao modelo Gemini
    prompt = f"""
Você é um sistema de classificação de emails corporativos.

Classifique o email abaixo em UMA das categorias:
- Produtivo
- Improdutivo

Depois gere uma resposta automática curta e profissional.

Retorne SOMENTE um JSON no formato:

{{
  "categoria": "Produtivo ou Improdutivo",
  "resposta": "texto curto sugerido"
}}

Email:
\"\"\"{texto_limpo}\"\"\" 
"""

    try:
        # Cria o modelo Gemini Pro
        modelo = genai.GenerativeModel("gemini-pro")

        # Solicita a geração de conteúdo passando o prompt
        resposta_gemini = modelo.generate_content(prompt)

        # Texto bruto retornado pela IA
        texto_resposta = resposta_gemini.text.strip()

        # Tenta localizar um bloco JSON dentro da resposta do modelo
        correspondencia_json = re.search(r"\{.*\}", texto_resposta, re.DOTALL)
        
        if correspondencia_json:
            texto_json = correspondencia_json.group(0)
            return json.loads(texto_json)  # Converte o JSON para dict
        else:
            # Se o JSON não foi encontrado, força um erro para acionar o fallback
            raise json.JSONDecodeError("Nenhum JSON encontrado na resposta da IA", texto_resposta, 0)

    except Exception:
        # Se qualquer erro ocorrer (rede, chave, formato, etc.), usa o modo local
        return classificacao_alternativa_local(texto_limpo)


def classificacao_alternativa_local(texto_limpo: str) -> Dict[str, str]:
    """
    Classificação simples baseada em palavras-chave.
    Usada quando o Gemini falha.
    
    Se o texto contiver termos relacionados a tarefas ou problemas,
    classifica como Produtivo. Caso contrário, como Improdutivo.
    """

    palavras_chave_produtivas = [
        "suporte", "status", "atualização", "reunião",
        "pedido", "erro", "problema", "documento", "solicitação"
    ]

    # Verifica se alguma palavra-chave produtiva aparece no texto
    if any(palavra in texto_limpo for palavra in palavras_chave_produtivas):
        return {
            "categoria": "Produtivo",
            "resposta": "Obrigado pelo contato! Estamos analisando sua solicitação e retornamos em breve. Guilherme Andrade"
        }

    # Caso nenhuma palavra relevante seja encontrada
    return {
        "categoria": "Improdutivo",
        "resposta": "Obrigado pela mensagem! Caso precise de algo específico, estou à disposição. Atenciosamente, Guilherme Andrade"
    }
