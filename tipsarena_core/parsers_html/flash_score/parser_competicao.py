from tipsarena_core.utils import html_utils, string_utils
from tipsarena_core.services import log_service as log


def processarHtmlCompeticao(html: str):
  try:
    documentoHtml = html_utils.converterStringParaHtml(html)
    linksCabecalho = html_utils.obterDadosCabecalho(documentoHtml)

    paisCompeticao = {"url": linksCabecalho[1]["href"],
                      "nome": linksCabecalho[1]["text"]}

    anoEdicao = documentoHtml.select(".teamHeader__text")[0].text
    # urlCompeticao = urlCompeticao[:-1] + "-" + anoEdicao.replace("/", "-") + "/"

    nomeCompeticao = documentoHtml.select(".teamHeader__name")[0].text
    logoCompeticao = documentoHtml.select(".teamHeader__logo")
    logoCompeticao = logoCompeticao[0]["style"].split("(")[1]
    logoCompeticao = logoCompeticao.replace(")", "")
    logoCompeticao = logoCompeticao.replace("\\", "")
    logoCompeticao = logoCompeticao.replace("'", "")

    return {
      "nome": string_utils.limparString(nomeCompeticao),
      "pais": paisCompeticao,
      "urlLogo": logoCompeticao,
      "url": "",
      "anoEdicao": anoEdicao,
      "totalPartidas": 0,
      "totalPartidasFinalizadas": 0,
      "status": "NAO_DEFINIDO",
      "equipeCampea": None
    }

  except Exception as e:
    log.ERRO("Erro ao extrair dados da competição [{}]", e.args)
    return None


def processarHtmlCompeticoesPais(html: str):
  try:
    CSS_LISTA_COMPETICOES = "ul.selected-country-list>li>a"
    listaCompeticoes = []
    documentoHtml = html_utils.converterStringParaHtml(html)

    competicoes = documentoHtml.select(CSS_LISTA_COMPETICOES)
    sequencial = 1
    for competicao in competicoes:
      urlCompet = competicao["href"]
      if urlCompet != "#":
        listaCompeticoes.append({"url": urlCompet, "sequencial": sequencial})
        sequencial += 1

    return listaCompeticoes
  except Exception as e:
    log.ERRO("Erro ao processar lista de competições do país [{}]", e.args)
    return None


def processarHtmlEdicoesCompeticao(html: str):
  try:
    CSS_LISTA_EDICOES = "#tournament-page-archiv div.profileTable__row"
    listaEdicoes = []
    documentoHtml = html_utils.converterStringParaHtml(html)

    linksCompeticao = documentoHtml.select(CSS_LISTA_EDICOES)

    sequencial = 1
    for linha in linksCompeticao:
      links = linha.select(".leagueTable__seasonName a")
      if len(links) == 0: continue

      anoCompeticao = links[0].text.split(" ")[-1]
      anoCompeticao = anoCompeticao.replace("/", "-")
      # urlEdicao = urlCompeticao[:-1] + "-" + anoCompeticao + "/"

      equipeVencedora = {"nome": "", "url": ""}

      if len(links) > 1:
        equipeVencedora = {
          "nome": links[1].text, "url": links[1]["href"]}

      listaEdicoes.append(
        {"url": "",
         "anoEdicao": anoCompeticao,
         "equipeVencedora": equipeVencedora,
         "sequencial": sequencial})
      sequencial += 1

    return listaEdicoes
  except Exception as e:
    log.ERRO("Erro ao obter lista de edições da competição [{}]", e.args)
    return None
