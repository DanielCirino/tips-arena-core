from tipsarena_core.utils import html_utils, hash_utils
from tipsarena_core.extratores.flash_score import navegador_web
from tipsarena_core.services import log_service as log


def processarHtmlListaPaises(html: str):
  try:
    CSS_ITEM_PAIS = "a[id^=lmenu_]"
    documentoHtml = html_utils.converterStringParaHtml(html)
    htmlPaises = documentoHtml.select(CSS_ITEM_PAIS)

    listaPaises = []
    sequencial = 1

    for urlPais in htmlPaises:
      url = urlPais.attrs["href"].replace(navegador_web.URL_BASE, "")

      if url != "#":
        listaPaises.append(
          {"url": url,
           "sequencial": sequencial
           })
        sequencial += 1
    return listaPaises
  except Exception as e:
    log.ERRO("Não foi possível processar html lista de países.", e.args)
    return None
