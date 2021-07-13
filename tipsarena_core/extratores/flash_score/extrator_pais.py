# -*- coding: utf-8 -*-
from datetime import datetime
from tipsarena_core.extratores.flash_score import navegador_web
from tipsarena_core.services import log_service as log
from tipsarena_core.utils import html_utils, hash_utils, string_utils
from tipsarena_core.utils.html_utils import DadosBrutos

def extrairHtmlPaises():
  try:
    CSS_LISTA_PAISES = "#category-left-menu"
    CSS_LISTAR_MAIS_PAISES = "[class^=itemMore_]"
    url = f"{navegador_web.URL_BASE}/futebol"
    browser = navegador_web.obterNavegadorWeb()
    browser.get(url)
    navegador_web.fecharPopupCookies()

    elementoListaMaisPaises = navegador_web.obterElementoAposCarregamento(CSS_LISTAR_MAIS_PAISES)
    elementoListaMaisPaises.click()

    htmlListaPaises = navegador_web.obterElementoAposCarregamento(CSS_LISTA_PAISES)

    return DadosBrutos(hash_utils.gerarHash(url),
                       "PAISES",
                       url,
                       string_utils.limparString(
                         htmlListaPaises.get_attribute("innerHTML"))
                       )

  except Exception as e:
    log.ERRO("Não foi possível extrair lista de países.", e.args)
    browser.save_screenshot(f"error_screenshot_{datetime.now().strftime('%Y%m%d')}.png")
    return None
  finally:
    navegador_web.finalizarNavegadorWeb()
