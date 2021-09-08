# -*- coding: utf-8 -*-
from datetime import datetime
from tipsarena_core.utils import html_utils, string_utils, hash_utils
from tipsarena_core.services import log_service as log, auth_service
from tipsarena_core.extratores.flash_score import navegador_web
from tipsarena_core.models.item_extracao import ItemExtracao


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
    documentoHtml = html_utils.converterStringParaHtml(html)

    competicoes = documentoHtml.select(CSS_LISTA_COMPETICOES)

    for competicao in competicoes:
      url = competicao["href"]

      if url != "#":
        urlCompeticao = f"{navegador_web.URL_BASE}{url}"
        TIPO_EXTRACAO = "HTML_LISTA_EDICOES_COMPETICAO"
        id = auth_service.gerarIdentificadorUniversal()
        dataHoraExtracao = datetime.now()

        yield ItemExtracao(
          {
            "id": id,
            "url": f"{urlCompeticao}",
            "urlHash": hash_utils.gerarHash(urlCompeticao),
            "tipo": TIPO_EXTRACAO,
            "dataHora": dataHoraExtracao,
            "html": None,
            "nomeArquivo": None
          })


  except Exception as e:
    log.ERRO(f"Erro ao processar lista de competições do país [{urlCompeticao}]", e.args)
    return None


def processarHtmlEdicoesCompeticao(html: str):
  try:
    CSS_LISTA_EDICOES = "#tournament-page-archiv div.profileTable__row"
    documentoHtml = html_utils.converterStringParaHtml(html)

    metadados = documentoHtml.select_one("metadados").attrs
    urlCompeticao = metadados["url_competicao"]

    linksCompeticao = documentoHtml.select(CSS_LISTA_EDICOES)

    sequencial = 1
    for linha in linksCompeticao:
      links = linha.select(".leagueTable__seasonName a")
      if len(links) == 0: continue

      anoEdicao = links[0].text.split(" ")[-1]
      anoEdicao = anoEdicao.replace("/", "-")

      urlEdicao = f"{urlCompeticao[:-1]}-{anoEdicao}/"

      equipeVencedora = None

      if len(links) > 1:
        equipeVencedora = {
          "nome": links[1].text,
          "url": f"{navegador_web.URL_BASE}{links[1]['href']}"
        }

      yield {"url": urlEdicao,
             "anoEdicao": anoEdicao,
             "equipeVencedora": equipeVencedora,
             "emAndamento": equipeVencedora is None,
             "sequencial": sequencial}

      sequencial += 1

  except Exception as e:
    log.ERRO(f"Erro ao obter lista de edições da competição [{urlCompeticao}]", e.args)
    return None
