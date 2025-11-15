from pydantic import BaseModel

class ResultadoSaida(BaseModel):
    """
    Define a estrutura de dados da resposta
    para o endpoint /api/process.
    """
    categoria: str
    resposta: str
    texto_original: str | None = None