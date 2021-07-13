def teste_obter_navegador_web(navegadorWeb):
  browser = navegadorWeb.obterNavegadorWeb()
  browser.get("https://www.google.com.br")
  assert browser.title == "Google"
  # navegadorWeb.finalizarNavegadorWeb()


def teste_aguardar_carregamento_elemento(navegadorWeb):
  browser = navegadorWeb.obterNavegadorWeb()
  browser.get("https://www.flashscore.com.br")
  elemento = navegadorWeb.obterElementoAposCarregamento("#live-table")
  assert elemento is not None
  # navegadorWeb.finalizarNavegadorWeb()


def teste_aguardar_carregamento_pagina(navegadorWeb):
  browser = navegadorWeb.obterNavegadorWeb()
  browser.get("https://www.flashscore.com.br")
  navegadorWeb.aguardarCarregamentoPagina(".loadingOverlay")
  assert True
  # navegadorWeb.finalizarNavegadorWeb()

def teste_fechar_botao_cookies(navegadorWeb):
  navegadorWeb.fecharPopupCookies()
  assert True

def teste_finalizar_navegador_web(navegadorWeb):
  assert navegadorWeb.finalizarNavegadorWeb()
