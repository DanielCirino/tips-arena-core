from tipsarena_core.utils import html_utils
from tipsarena_core.services import log_service as log

def processarHtmlEdicaoCompeticao(html:str):
  try:
    CSS_NOME_COMPETICAO = "div.teamHeader__name"
    CSS_LINKS_CABECALHO = "h2.breadcrumb a"
    CSS_ANO_EDICAO = "div.teamHeader__text"

    documentoHtml = html_utils.converterStringParaHtml(html)
    linksCabecalho = documentoHtml.select(CSS_LINKS_CABECALHO)
    divNomeCompeticao = documentoHtml.select(CSS_NOME_COMPETICAO)
    divAnoEdicao = documentoHtml.select(CSS_ANO_EDICAO)

    if len(divNomeCompeticao) > 0:
      nomeCometicao = divNomeCompeticao[0].text

    if len(linksCabecalho) > 1:
      paisCompeticao = linksCabecalho[1].text

    if len(divAnoEdicao) > 0:
      anoEdicao = divAnoEdicao[0].text.replace("/", "-")

    competicao = {
      "nome": nomeCometicao.strip(),
      "pais": paisCompeticao.strip(),
      "url": ""
    }

    return {
      "competicao": competicao,
      "ano": anoEdicao,
      "total_partidas": 0,
      "total_partidas_finalizadas": 0,
      "status": "NAO_DEFINIDO",
      "url": ""
    }
  except Exception as e:
    log.ERRO("Não foi possível processar html da edição da competição {}.", e.args)
    return None