def teste_obter_navegador_web(navegadorWeb):
  navegadorWeb.navegar("https://www.google.com.br")
  assert browser.title == "Google"


def teste_aguardar_carregamento_elemento(navegadorWeb):
  navegadorWeb.navegar("https://www.flashscore.com.br")
  elemento = navegadorWeb.obterElementoAposCarregamento("#live-table")
  assert elemento is not None


def teste_aguardar_carregamento_pagina(navegadorWeb):
  navegadorWeb.navegar("https://www.flashscore.com.br")
  navegadorWeb.aguardarCarregamentoPagina(".loadingOverlay")
  assert True
  # navegadorWeb.finalizarNavegadorWeb()


def teste_fechar_botao_cookies(navegadorWeb):
  navegadorWeb.navegar("https://www.flashscore.com.br")
  navegadorWeb.fecharPopupCookies()
  assert True


def teste_finalizar_navegador_web(navegadorWeb):
  assert navegadorWeb.finalizarNavegadorWeb()
