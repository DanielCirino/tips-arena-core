from tipsarena_core.services import log_service as log
from tipsarena_core.utils import html_utils,string_utils


def processarHtmlEquipesCompeticao(html: str):
  try:
    CSS_LISTA_EQUIPES = "[class^=rowCellParticipantImage]"
    tabelaClassificacao = html_utils.converterStringParaHtml(html)
    htmlListaEquipes = tabelaClassificacao.select(CSS_LISTA_EQUIPES)

    listaEquipes = []
    sequencial = 1

    for html in htmlListaEquipes:
      htmlEscudo = html.select("img")[0]
      listaEquipes.append(
        {"nome": htmlEscudo.attrs["alt"],
         "url": html.attrs["href"],
         "urlEscudo": htmlEscudo.attrs["src"],
         "sequencial": sequencial}
      )
      sequencial += 1

    return listaEquipes
  except Exception as e:
    log.ERRO("Não foi possível processar html lista de equipes da edição competição [{}]", e.args)
    return None

def processarHtmlEquipe(html:str):
  try:
    CSS_NOME_EQUIPE = ".teamHeader__name"
    CSS_ESCUDO_EQUIPE = ".teamHeader__logo"

    documentoHtml = html_utils.converterStringParaHtml(html)
    linksCabecalho = html_utils.obterDadosCabecalho(documentoHtml)

    paisEquipe = {"nome": linksCabecalho[1]["text"],
                  "url": linksCabecalho[1]["href"]}

    nomeEquipe = documentoHtml.select_one(CSS_NOME_EQUIPE).text

    urlEscudoEquipe = documentoHtml.select(CSS_ESCUDO_EQUIPE)
    urlEscudoEquipe = urlEscudoEquipe[0]["style"].split("(")
    urlEscudoEquipe = urlEscudoEquipe[1].replace(")", "")

    return {
      "nome": string_utils.limparString(nomeEquipe),
      "pais": paisEquipe,
      "urlEscudo": urlEscudoEquipe,
      "url": ""
    }

  except Exception as e:
    log.ERRO("Não foi possível processar o html  da equipe [{}]", e.args)
    return None