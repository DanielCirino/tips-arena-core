# -*- coding: utf-8 -*-
from datetime import datetime
from tipsarena_core.utils import html_utils, hash_utils, string_utils
from tipsarena_core.extratores.flash_score import navegador_web
from tipsarena_core.services import log_service as log, auth_service
from tipsarena_core.models.item_extracao import ItemExtracao


def processarHtmlListaPaises(html: str):
  try:
    CSS_ITEM_PAIS = "a[id^=lmenu_]"
    documentoHtml = html_utils.converterStringParaHtml(html)
    htmlPaises = documentoHtml.select(CSS_ITEM_PAIS)


    for pais in htmlPaises:
      url = pais.attrs["href"]

      if url != "#":
        urlPais = f"{navegador_web.URL_BASE}{url}"
        TIPO_EXTRACAO = "HTML_LISTA_COMPETICOES_PAIS"
        id = auth_service.gerarIdentificadorUniversal()
        dataHoraExtracao = datetime.now()

        yield ItemExtracao(
          {
            "id": id,
            "url": f"{urlPais}",
            "urlHash": hash_utils.gerarHash(urlPais),
            "tipo": TIPO_EXTRACAO,
            "dataHora": dataHoraExtracao,
            "html": None,
            "nomeArquivo": None
          })

  except Exception as e:
    log.ERRO("Não foi possível processar html lista de países.", e.args)
    return None
