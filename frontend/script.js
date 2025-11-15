document.addEventListener("DOMContentLoaded", () => {
  // URL da API FastAPI usada pelo frontend.

  // Para deploy no Vercel, esta é a rota a ser usada:
  // const API_URL = "/api/process"; // Para Vercel (deploy)

  // Para testes locais, a API roda no localhost:
  const API_URL = "http://localhost:8000/api/process";

  // Captura os elementos do formulário e áreas de exibição
  const formEmail = document.getElementById("formEmail");
  const inputFile = document.getElementById("arquivo");
  const inputTexto = document.getElementById("textoEmail");
  const respostaDiv = document.getElementById("resposta");
  const nomeArquivoSpan = document.getElementById("nome-arquivo-selecionado");

  /**
   * Quando o usuário seleciona um arquivo:
   * - Mostramos o nome do arquivo
   * - Limpamos o campo de texto para evitar envio duplicado
   */
  inputFile.addEventListener("change", () => {
    if (inputFile.files.length > 0) {
      nomeArquivoSpan.textContent = `Arquivo: ${inputFile.files[0].name}`;
      inputTexto.value = ""; // limpa o campo de texto
    } else {
      nomeArquivoSpan.textContent = ""; // se cancelado
    }
  });

  /**
   * Quando o usuário começa a digitar no campo de texto:
   * - Limpa o campo de arquivo para evitar conflito
   */
  inputTexto.addEventListener("input", () => {
    if (inputTexto.value.trim() !== "") {
      inputFile.value = null; // remove arquivo selecionado
      nomeArquivoSpan.textContent = "";
    }
  });

  /**
   * Lógica principal do formulário:
   * - Cria um FormData
   * - Envia arquivo ou texto, nunca os dois ao mesmo tempo
   * - Exibe mensagens de carregamento, erro e resposta formatada
   */
  formEmail.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData();

    // Decide se o envio será por arquivo ou texto
    if (inputFile.files.length > 0) {
      formData.append("file", inputFile.files[0]);
    } else if (inputTexto.value.trim() !== "") {
      formData.append("texto", inputTexto.value.trim());
    } else {
      // Nada foi enviado — mostra erro ao usuário
      respostaDiv.style.display = "block";
      respostaDiv.innerHTML = `<div class="erro">Envie um arquivo .txt/.pdf ou escreva um texto.</div>`;
      return;
    }

    // Mensagem de carregamento enquanto aguarda resposta da API
    respostaDiv.style.display = "block";
    respostaDiv.innerHTML = `<div class="loading">Processando, aguarde...</div>`;

    try {
      // Faz a requisição POST para a API FastAPI
      const response = await fetch(API_URL, {
        method: "POST",
        body: formData,
      });

      // Se a API retornar erro (400, 500 ou outros)
      if (!response.ok) {
        const errorData = await response.json();
        const mensagem =
          errorData.error || errorData.detail || "Erro ao processar o email.";
        throw new Error(mensagem);
      }

      // Converte o retorno JSON
      const resultado = await response.json();

      // Formata a resposta automática (mantém quebras de linha)
      const respostaFormatada = (resultado.resposta || "").replace(
        /\n/g,
        "<br>"
      );

      // O texto original é exibido como texto puro (textContent)
      const textoOriginalFormatado = resultado.texto_original || "";

      /**
       * Montei o HTML base da resposta:
       * - Texto enviado
       * - Categoria
       * - Resposta automática sugerida
       */
      respostaDiv.innerHTML = `
          <p><strong>Texto Enviado:</strong></p>
          <div class="texto-original-cliente"></div>
          
          <hr class="linha-divisoria"> 

          <p><strong>Categoria:</strong> ${resultado.categoria}</p>
          <p><strong>Resposta automática:</strong></p>
          <div class="resposta-sugerida">${respostaFormatada}</div>
      `;

      // Insere o texto original de forma segura
      respostaDiv.querySelector(".texto-original-cliente").textContent =
        textoOriginalFormatado;
    } catch (erro) {
      // Exibe erro ao usuário
      respostaDiv.innerHTML = `
          <div class="erro">
            Ocorreu um erro ao processar o email. Detalhes: ${erro.message}
          </div>
      `;
    }
  });
});
