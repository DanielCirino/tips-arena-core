from tipsarena_core.utils import html_utils, string_utils
from tipsarena_core.services import log_service as log


def processarHtmlEstatisticas(html: str):
  CSS_LINHAS_ESTATISTICAS = "div[class^=statRow]"
  CSS_VALORES_ESTATISTICA = "div[class^=statCategory] div"
  estatisticasPartida = []

  try:
    htmlEstatisticas = html_utils.converterStringParaHtml(html)
    listaEstatisticas = htmlEstatisticas.select(CSS_LINHAS_ESTATISTICAS)

    for elemento in listaEstatisticas:
      camposEstatistica = elemento.select(CSS_VALORES_ESTATISTICA)

      descricao = string_utils.limparString(camposEstatistica[1].text)
      valorMandante = string_utils.limparString(camposEstatistica[0].text)
      valorVisitante = string_utils.limparString(camposEstatistica[2].text)

      estatisticasPartida.append({"descricao": descricao,
                                  "valorMandante": valorMandante,
                                  "valorVisitante": valorVisitante})

    return estatisticasPartida

  except Exception as e:
    log.ERRO("Não foi possível processar HTML estatísticas da partida.", e.args)
    return estatisticasPartida


def normalizarDescricaoEstatistica(descricao: str):
  novaDescricao = descricao
  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Goal Attempts":
    novaDescricao = "Tentativa de Gols"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Shots on Goal":
    novaDescricao = "Chutes a gol"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  else:
    log.ALERTA(f"Descricao estatística '{descricao}' nao mapeada.")

  return novaDescricao
