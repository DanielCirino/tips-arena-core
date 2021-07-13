# -*- coding: utf-8 -*-

from tipsarena_core.extratores.flash_score import navegador_web
from tipsarena_core.utils import string_utils as strUtil, html_utils, hash_utils
from tipsarena_core.utils.html_utils import DadosBrutos
from tipsarena_core.services import log_service as log


def extrairHtmlCompeticoesPais(urlPais):
  try:
    url = f"{navegador_web.URL_BASE}{urlPais}"
    documentoHtml = html_utils.obterHtml(url)


    return DadosBrutos(hash_utils.gerarHash(urlPais),
                               "COMPETICOES_PAIS",
                               navegador_web.URL_BASE + urlPais,
                               strUtil.limparString(str(documentoHtml)))

  except Exception as e:
    log.ERRO(f"Erro ao obter lista de competições do país [{urlPais}]", e.args)
    return None


def extrairHtmlCompeticao(urlCompeticao):
  try:
    documentoHtml = html_utils.obterHtml(navegador_web.URL_BASE + urlCompeticao)

    return DadosBrutos(hash_utils.gerarHash(urlCompeticao),
                          "COMPETICAO",
                          navegador_web.URL_BASE + urlCompeticao,
                          strUtil.limparString(str(documentoHtml)))

  except Exception as e:
    log.ERRO(f"Erro ao extrair html da competição [{urlCompeticao}]", e.args)
    return None


def extrairHtmlEdicoesCompeticao(urlCompeticao):
  try:
    urlEdicoes = f"{navegador_web.URL_BASE}{urlCompeticao}/arquivo"
    documentoHtml = html_utils.obterHtml(urlEdicoes)

    return DadosBrutos(hash_utils.gerarHash(urlCompeticao),
                                 "EDICOES_COMPETICAO",
                                 urlEdicoes,
                                 strUtil.limparString(str(documentoHtml)))


  except Exception as e:
    log.ERRO(f"Erro ao extrair html de edições da competição [{urlCompeticao}]", e.args)
    return None

