# -*- coding: utf-8 -*-

from tipsarena_core.extratores import navegador_web
from tipsarena_core.utils import html_utils, logUtils as log
from tipsarena_core.services import log_service as log


def obterListaEdicoesCompeticao(urlCompeticao):
  try:
    CSS_LISTA_EDICOES = "#tournament-page-archiv div.profileTable__row"
    listaEdicoes = []
    documentoHtml = html_utils.obterHtml(
      navegador_web.URL_BASE + urlCompeticao + "arquivo/")

    linksCompeticao = documentoHtml.select(CSS_LISTA_EDICOES)

    sequencial = 1
    for linha in linksCompeticao:
      links = linha.select(".leagueTable__seasonName a")
      if len(links) == 0: continue

      anoCompeticao = links[0].text.split(" ")[-1]
      anoCompeticao = anoCompeticao.replace("/", "-")
      urlEdicao = urlCompeticao[:-1] + "-" + anoCompeticao + "/"

      equipeVencedora = {"nome": "", "url": ""}

      if len(links) > 1:
        equipeVencedora = {
          "nome": links[1].text, "url": links[1]["href"]}

      listaEdicoes.append(
        {"url": urlEdicao, "equipeVencedora": equipeVencedora, "sequencial": sequencial})
      sequencial += 1

    return listaEdicoes
  except Exception as e:
    log.ERRO(f"Não foi possível extrair edições da competição {urlCompeticao}.", e.args)
    return None


def obterEdicaoMaisRecenteCompeticao(urlCompeticao):
  try:
    edicoes = obterListaEdicoesCompeticao(urlCompeticao)
    if len(edicoes) > 0:
      return edicoes[0]
  except Exception as e:
    log.ERRO(f"Não foi possível obter edição mais recente da competição {urlCompeticao}.", e.args)
    return None


def obterDadosEdicaoCompeticao(urlEdicao: str):
  try:
    CSS_NOME_COMPETICAO = "div.teamHeader__name"
    CSS_LINKS_CABECALHO = "h2.breadcrumb a"
    CSS_ANO_EDICAO = "div.teamHeader__text"

    documentoHtml = html_utils.obterHtml(navegador_web.URL_BASE + urlEdicao)
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
      "url": urlEdicao.replace("-" + anoEdicao, "")
    }

    if urlEdicao.find(anoEdicao) < 0:
      urlEdicao = urlEdicao[:-1] + "-" + anoEdicao + "/"

    return {
      "competicao": competicao,
      "ano": anoEdicao,
      "total_partidas": 0,
      "total_partidas_finalizadas": 0,
      "status": "NAO_DEFINIDO",
      "url": urlEdicao
    }
  except Exception as e:
    log.ERRO(f"Não foi possível obter dados da edição da competição {urlEdicao}.", e.args)
    return None
