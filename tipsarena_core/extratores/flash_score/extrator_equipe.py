# -*- coding: utf-8 -*-

from tipsarena_core.extratores.flash_score import navegador_web
from tipsarena_core.utils import string_utils, html_utils, hash_utils
from tipsarena_core.utils.html_utils import DadosBrutos
from tipsarena_core.services import log_service as log


def extrairHtmlEquipesEdicaoCompeticao(urlEdicao: str):
  try:
    CSS_TABELA_CLASSIFICACAO = "#tournament-table-tabs-and-content"

    url = f"{navegador_web.URL_BASE}{urlEdicao}classificacao/"
    browser = navegador_web.obterNavegadorWeb()
    browser.get(url)

    tabelaClassificacao = navegador_web.obterElementoAposCarregamento(CSS_TABELA_CLASSIFICACAO)

    return DadosBrutos(hash_utils.gerarHash(urlEdicao),
                       "EQUIPES_EDICAO_COMPETICAO",
                       url,
                       string_utils.limparString(
                         tabelaClassificacao.get_attribute("innerHTML"))
                       )

  except Exception as e:
    log.ERRO(f"Não foi possível extrair html de equipes da edição da competição [{urlEdicao}]", e.args)
    return None


def extrairHtmlEquipe(urlEquipe):
  try:
    url = f"{navegador_web.URL_BASE}{urlEquipe}"
    documentoHtml = html_utils.obterHtml(url)

    return DadosBrutos(hash_utils.gerarHash(urlEquipe),
                       "EQUIPE",
                       url,
                       string_utils.limparString(str(documentoHtml)))


  except Exception as e:
    log.ERRO(f"Não foi possível extrair html da equipe [{urlEquipe}]", e.args)
    return None
