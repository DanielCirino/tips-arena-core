# -*- coding: utf-8 -*-

from tipsarena_core.extratores import navegador_web
from tipsarena_core.utils import string_utils as strUtil, html_utils
from tipsarena_core.services import log_service as log


def obterListaCompeticoesPais(urlPais):
  try:
    CSS_LISTA_COMPETICOES = "ul.selected-country-list>li>a"
    listaCompeticoes = []
    documentoHtml = html_utils.obterHtml(navegador_web.URL_BASE + urlPais)

    competicoes = documentoHtml.select(CSS_LISTA_COMPETICOES)
    sequencial = 1
    for competicao in competicoes:
      urlCompet = competicao["href"]
      if urlCompet != "#":
        listaCompeticoes.append({"url": urlCompet, "sequencial": sequencial})
        sequencial += 1

    return listaCompeticoes
  except Exception as e:
    log.ERRO(f"Erro ao obter lista de competições do país [{urlPais}]", e.args)
    return None


def obterDadosCompeticao(urlCompeticao):
  try:
    documentoHtml = html_utils.obterHtml(navegador_web.URL_BASE + urlCompeticao)
    linksCabecalho = html_utils.obterDadosCabecalho(documentoHtml)

    paisCompeticao = {"url": linksCabecalho[1]["href"],
                      "nome": linksCabecalho[1]["text"]}

    anoEdicao = documentoHtml.select(".teamHeader__text")[0].text
    urlCompeticao = urlCompeticao[:-1] + "-" + anoEdicao.replace("/", "-") + "/"

    nomeCompeticao = documentoHtml.select(".teamHeader__name")[0].text
    logoCompeticao = documentoHtml.select(".teamHeader__logo")
    logoCompeticao = logoCompeticao[0]["style"].split("(")[1]
    logoCompeticao = logoCompeticao.replace(")", "")
    logoCompeticao = logoCompeticao.replace("\\", "")
    logoCompeticao = logoCompeticao.replace("'", "")

    return {
      "nome": strUtil.limparString(nomeCompeticao),
      "pais": paisCompeticao,
      "urlLogo": logoCompeticao,
      "url": urlCompeticao,
      "anoEdicao": anoEdicao,
      "totalPartidas": 0,
      "totalPartidasFinalizadas": 0,
      "status": "NAO_DEFINIDO",
      "equipeCampea": None
    }

  except Exception as e:
    log.ERRO(f"Erro ao extrair dados da competição [{urlCompeticao}]", e.args)
    return None


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
    log.ERRO(f"Erro ao obter lista de edições da competição [{urlCompeticao}]", e.args)
    return None


def obterEdicaoMaisRecenteCompeticao(urlCompeticao):
  try:
    edicoes = obterListaEdicoesCompeticao(urlCompeticao)
    return edicoes[0]
  except Exception as e:
    log.ERRO(f"Erro ao obter edição mais recente da competição [{urlCompeticao}]", e.args)
    return None
