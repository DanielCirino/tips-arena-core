# -*- coding: utf-8 -*-
from datetime import datetime
from tipsarena_core.extratores.flash_score import navegador_web
from tipsarena_core.services import log_service as log


def obterListaPaises():
  try:
    CSS_LISTA_PAISES = "a[id^=lmenu_]"

    browser = navegador_web.obterNavegadorWeb()
    browser.get(navegador_web.URL_BASE + "/futebol/")
    navegador_web.fecharPopupCookies()
    htmlListaPaises = navegador_web.obterElementoAposCarregamento("#category-left-menu")
    elementoListaMaisPaises = navegador_web.obterElementoAposCarregamento("[class^=itemMore_]")
    elementoListaMaisPaises.click()

    htmlPaises = htmlListaPaises.find_elements_by_css_selector(CSS_LISTA_PAISES)

    listaPaises = []

    sequencial = 1
    for urlPais in htmlPaises:
      url = urlPais.get_attribute("href").replace(navegador_web.URL_BASE, "")
      if url != "#":
        listaPaises.append({"url": url, "sequencial": sequencial})
        sequencial += 1

    return listaPaises
  except Exception as e:
    log.ERRO("Não foi possível extrair lista de países.", e.args)
    browser.save_screenshot(f"error_screenshot_{datetime.now().strftime('%Y%m%d')}.png")
    return []
  finally:
    navegador_web.finalizarNavegadorWeb()
