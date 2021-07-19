# -*- coding: utf-8 -*-

from tipsarena_core.extratores.flash_score import navegador_web
from tipsarena_core.utils import html_utils, logUtils as log, hash_utils,string_utils as strUtil

from tipsarena_core.services import log_service as log


def extrairHtmlEdicaoCompeticao(urlEdicao: str):
  try:
    url = f"{navegador_web.URL_BASE}{urlEdicao}"
    documentoHtml = html_utils.obterHtml(url)

    return DadosExtracao(hash_utils.gerarHash(urlEdicao),
                       "EDICAO_COMPETICAO",
                         url,
                         strUtil.limparString(str(documentoHtml)))

    
  except Exception as e:
    log.ERRO(f"Não foi possível obter html da edição da competição {urlEdicao}.", e.args)
    return None
