from tipsarena_core.utils import html_utils, string_utils
from tipsarena_core.services import log_service as log


def processarHtmlEstatisticas(html: str):
  estatisticasPartida = []
  try:
    CSS_LINHAS_ESTATISTICAS = "div[class^=statRow]"
    CSS_VALORES_ESTATISTICA = "div[class^=statCategory] div"
    htmlEstatisticas = html_utils.converterStringParaHtml(html)

    listaEstatisticas = htmlEstatisticas.select(CSS_LINHAS_ESTATISTICAS)

    for html in listaEstatisticas:
      estatistica = {"desc": "",
                     "valor_mandante": "",
                     "valor_visitante": ""}

      camposEstatistica = html.find_elements_by_css_selector(CSS_VALORES_ESTATISTICA)

      estatistica["desc"] = string_utils.limparString(
        camposEstatistica[1].text)
      estatistica["valor_mandante"] = string_utils.limparString(
        camposEstatistica[0].text)
      estatistica["valor_visitante"] = string_utils.limparString(
        camposEstatistica[2].text)

      estatisticasPartida.append(estatistica)

    return estatisticasPartida

  except Exception as e:
    log.ERRO("Não foi possível obter estatísticas da partida.", e.args)
    return estatisticasPartida
