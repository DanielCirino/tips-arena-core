# -*- coding: utf-8 -*-
from datetime import datetime
from tipsarena_core.extratores.flash_score import navegador_web
from tipsarena_core.utils import string_utils, html_utils, hash_utils
from tipsarena_core.models.item_extracao import ItemExtracao
from tipsarena_core.services import log_service as log, auth_service


def extrairHtmlCompeticoesPais(urlPais: str):
  try:
    TIPO_EXTRACAO = "HTML_LISTA_COMPETICOES_PAIS"
    html = html_utils.obterHtml(urlPais)

    id = auth_service.gerarIdentificadorUniversal()
    dataHoraExtracao = datetime.now()

    urlHash = hash_utils.gerarHash(urlPais)
    htmlFinal = html_utils.incluirMetadadosHtml(str(html), urlPais, urlHash, TIPO_EXTRACAO)

    return ItemExtracao(
      {
        "id": id,
        "url": urlPais,
        "urlHash": urlHash,
        "tipo": TIPO_EXTRACAO,
        "dataHora": dataHoraExtracao,
        "html": string_utils.limparString(str(htmlFinal)),
        "nomeArquivo": f"{id.lower()}.html"
      })

  except Exception as e:
    log.ERRO(f"Erro ao obter lista de competições do país [{urlPais}]", e.args)
    return None


def extrairHtmlCompeticao(urlCompeticao: str):
  try:
    TIPO_EXTRACAO = "HTML_COMPETICAO"
    html = html_utils.obterHtml(navegador_web.URL_BASE + urlCompeticao)

    id = auth_service.gerarIdentificadorUniversal()
    dataHoraExtracao = datetime.now()

    urlHash = hash_utils.gerarHash(urlCompeticao)
    htmlFinal = html_utils.incluirMetadadosHtml(str(html), urlCompeticao, urlHash, TIPO_EXTRACAO)

    return ItemExtracao(
      {
        "id": id,
        "url": urlCompeticao,
        "urlHash": urlHash,
        "tipo": TIPO_EXTRACAO,
        "dataHora": dataHoraExtracao,
        "html": string_utils.limparString(str(htmlFinal)),
        "nomeArquivo": f"{id.lower()}.html"
      })

  except Exception as e:
    log.ERRO(f"Erro ao extrair html da competição [{urlCompeticao}]", e.args)
    return None


def extrairHtmlEdicoesCompeticao(urlCompeticao: str):
  try:
    TIPO_EXTRACAO = "HTML_LISTA_EDICOES_COMPETICAO"
    urlEdicoes = f"{urlCompeticao}arquivo"
    html = html_utils.obterHtml(urlEdicoes)

    id = auth_service.gerarIdentificadorUniversal()
    dataHoraExtracao = datetime.now()

    urlHash = hash_utils.gerarHash(urlCompeticao)
    htmlFinal = html_utils.incluirMetadadosHtml(str(html), urlCompeticao, urlHash, TIPO_EXTRACAO)

    return ItemExtracao(
      {
        "id": id,
        "url": urlEdicoes,
        "urlHash": urlHash,
        "tipo": TIPO_EXTRACAO,
        "dataHora": dataHoraExtracao,
        "html": string_utils.limparString(
          str(htmlFinal)),
        "nomeArquivo": f"{id.lower()}.html"
      })


  except Exception as e:
    log.ERRO(f"Erro ao extrair html de edições da competição [{urlCompeticao}]", e.args)
    return None
