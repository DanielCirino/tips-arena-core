# -*- coding: utf-8 -*-
from datetime import datetime
from tipsarena_core.extratores.flash_score.navegador_web import URL_BASE
from tipsarena_core.utils import html_utils, logUtils as log, hash_utils, string_utils
from tipsarena_core.models.item_extracao import ItemExtracao
from tipsarena_core.services import log_service as log, auth_service
from tipsarena_core.extratores.flash_score import extrator_partida


def extrairHtmlPartidasFinalizadasEdicaoCompeticao(urlEdicao):
  try:
    urlPartidas = f"{urlEdicao}resultados/"
    return extrator_partida.extrairHtmlPartidas(urlPartidas)
  except Exception as e:
    log.ERRO(f"Não foi possível extrair HTML lista de IDS de partidas da edição da competicão {urlEdicao}.", e.args)
    return None


def extrairHtmlPartidasAgendadasEdicaoCompeticao(urlEdicao: str):
  try:
    urlPartidas = f"{urlEdicao}calendario/"
    return extrator_partida.extrairHtmlPartidas(urlPartidas)

  except Exception as e:
    log.ERRO(f"Não foi possível extrair HTML lista de IDS de partidas da edição da competicão {urlEdicao}.", e.args)
    return None


def extrairHtmlEdicaoCompeticao(urlEdicao: str):
  try:
    documentoHtml = html_utils.obterHtml(urlEdicao)

    TIPO_EXTRACAO = "EDICAO_COMPETICAO"
    urlHash = hash_utils.gerarHash(urlEdicao)
    id = auth_service.gerarIdentificadorUniversal()
    dataHoraExtracao = datetime.now()

    htmlFinal = html_utils.incluirMetadadosHtml(str(documentoHtml), urlEdicao, urlHash, TIPO_EXTRACAO)

    return ItemExtracao(
      {
        "id": id,
        "url": urlEdicao,
        "urlHash": urlHash,
        "tipo": TIPO_EXTRACAO,
        "dataHora": dataHoraExtracao,
        "html": string_utils.limparString(str(htmlFinal)),
        "nomeArquivo": f"{id.lower()}.html"
      })

  except Exception as e:
    log.ERRO(f"Não foi possível obter html da edição da competição {urlEdicao}.", e.args)
    return None
