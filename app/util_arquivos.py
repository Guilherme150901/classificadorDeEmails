import PyPDF2
from io import BytesIO

def extrair_texto_de_pdf(bytes_do_arquivo: BytesIO) -> str:
    """
    Lê um arquivo PDF em bytes (enviado pelo usuário)
    e retorna o texto extraído.
    """
    try:
        # Abre o PDF usando o conteúdo em bytes
        leitor = PyPDF2.PdfReader(bytes_do_arquivo)
        texto_extraido = ""

        # Percorre todas as páginas do PDF e extrai o texto
        for pagina in leitor.pages:
            texto_extraido += pagina.extract_text() or ""  # Garantia caso a página não tenha texto extraível

        # Retorna o texto já limpo de espaços extras no início e fim
        return texto_extraido.strip()

    except Exception as e:
        # Caso ocorra qualquer erro na leitura do PDF
        print(f"Erro ao ler PDF: {e}")
        return ""