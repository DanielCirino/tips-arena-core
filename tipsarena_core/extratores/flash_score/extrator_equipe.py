# -*- coding: utf-8 -*-
from datetime import datetime
from tipsarena_core.extratores.flash_score import navegador_web
from tipsarena_core.utils import string_utils, html_utils, hash_utils
from tipsarena_core.models.item_extracao import ItemExtracao
from tipsarena_core.services import log_service as log, auth_service


def extrairHtmlEquipesEdicaoCompeticao(urlEdicao: str, metadados={}):
  try:
    CSS_TABELA_CLASSIFICACAO = "#tournament-table-tabs-and-content"

    urlEquipes = f"{urlEdicao}classificacao/"
    navegador_web.navegar(urlEquipes)

    navegador_web.obterElementoAposCarregamento(CSS_TABELA_CLASSIFICACAO)
    html = navegador_web.obterElementoAposCarregamento("body")

    TIPO_EXTRACAO = "EQUIPES_EDICAO_COMPETICAO"
    urlHash = hash_utils.gerarHash(urlEquipes)
    id = auth_service.gerarIdentificadorUniversal()
    dataHoraExtracao = datetime.now()

    metadados.update({
      "url_equipes": urlEquipes,
      "url_equipes_hash": urlHash,
    })

    htmlFinal = html_utils.incluirMetadadosHtml(html.get_attribute('outerHTML'), metadados)

    return ItemExtracao(
      {
        "id": id,
        "url": urlEdicao,
        "urlHash": urlHash,
        "tipo": TIPO_EXTRACAO,
        "dataHora": dataHoraExtracao,
        "html": string_utils.limparString(str(htmlFinal)),
        "nomeArquivo": f"eqp-edc{urlHash.lower()}.html"
      })

  except Exception as e:
    log.ERRO(f"Não foi possível extrair html de equipes da edição da competição [{urlEdicao}]", e.args)
    return None


def extrairHtmlEquipe(urlEquipe: str, metadados={}):
  try:
    documentoHtml = html_utils.obterHtml(urlEquipe)

    TIPO_EXTRACAO = "EQUIPE"
    urlHash = hash_utils.gerarHash(urlEquipe)
    id = auth_service.gerarIdentificadorUniversal()
    dataHoraExtracao = datetime.now()

    metadados.update({
      "url_equipe": urlEquipe,
      "url_equipe_hash": urlHash
    })

    htmlFinal = html_utils.incluirMetadadosHtml(str(documentoHtml), metadados)

    return ItemExtracao(
      {
        "id": id,
        "url": urlEquipe,
        "urlHash": urlHash,
        "tipo": TIPO_EXTRACAO,
        "dataHora": dataHoraExtracao,
        "html": string_utils.limparString(str(htmlFinal)),
        "nomeArquivo": f"{id.lower()}.html"
      })


  except Exception as e:
    log.ERRO(f"Não foi possível extrair html da equipe [{urlEquipe}]", e.args)
    return None
