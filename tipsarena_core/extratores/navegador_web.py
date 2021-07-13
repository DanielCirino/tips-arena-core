# -*- coding: utf-8 -*-

import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tipsarena_core.services import log_service as log

URL_BASE = "https://www.flashscore.com.br"
PATH_TO_WEBDRIVER = os.getenv("TA_PATH_TO_WEBDRIVER")
navegadorWeb = None

CSS_BOTAO_ACEITAR_COOKIES = "#onetrust-accept-btn-handler"


def obterNavegadorWeb():
  try:
    global navegadorWeb

    if PATH_TO_WEBDRIVER is None:
      log.ERRO("Variável de ambiente TA_PATH_TO_WEBDRIVER precisa ser criada.", "")
      exit(1)

    if navegadorWeb is None:
      # Ensure mobile-friendly view for parsing
      useragent = "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36"

      # Firefox
      profile = webdriver.FirefoxProfile()
      profile.set_preference("general.useragent.override", useragent)
      options = webdriver.FirefoxOptions()
      options.set_preference("dom.webnotifications.serviceworker.enabled", False)
      options.set_preference("dom.webnotifications.enabled", False)
      options.add_argument('--headless')

      # opcoes = Options()
      # opcoes.add_argument("--headless")
      # caps = webdriver.DesiredCapabilities.FIREFOX
      # caps["binary"] = PATH_TO_WEBDRIVER

      navegadorWeb = webdriver.Firefox(executable_path=PATH_TO_WEBDRIVER,
                                       firefox_profile=profile, options=options)

    return navegadorWeb

  except Exception as e:
    log.ERRO(f"Não foi possível iniciar o navegador WEB no caminho {PATH_TO_WEBDRIVER}.",
             e.args)
    return None


def obterElementoAposCarregamento(cssElemento, tempoEspera=10):
  try:
    espera = WebDriverWait(navegadorWeb, tempoEspera)
    elemento = espera.until(EC.presence_of_element_located((By.CSS_SELECTOR, cssElemento)))
    return elemento
  except Exception as e:
    log.ERRO(f"Não foi possível localizar o elemento '{cssElemento}'", e.args)
    return None


def aguardarCarregamentoPagina(cssIndicadorCarregamento, tempoEspera=10):
  espera = WebDriverWait(navegadorWeb, tempoEspera)
  espera.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, cssIndicadorCarregamento)))


def clicarElemento(elemento, tempoEspera=10):
  espera = WebDriverWait(navegadorWeb, tempoEspera)
  espera.until(EC.element_to_be_clickable(elemento)).click()


def fecharPopupCookies():
  try:
    botaoAceitarCookies = obterElementoAposCarregamento(CSS_BOTAO_ACEITAR_COOKIES)
    if botaoAceitarCookies is not None:
      if botaoAceitarCookies.is_displayed(): botaoAceitarCookies.click()
  except Exception as e:
    log.ERRO(f"Não foi possível fechar pop up de cookies '{CSS_BOTAO_ACEITAR_COOKIES}'", e.args)


# def aguardarCarregamentoPaginaOld(cssSelector):
#   try:
#     carregando = navegadorWeb.find_element_by_css_selector(
#       cssSelector)
#     tempoEspera = 0.0
#
#     while carregando.is_displayed():
#       time.sleep(0.5)
#       tempoEspera += 0.5
#
#       carregando = navegadorWeb.find_element_by_css_selector(
#         cssSelector)
#
#       if tempoEspera >= 10:
#         log.ALERTA(f"Esperou mais de 10 segundos, time out...]")
#         navegadorWeb.save_screenshot("prints/erro_loading.png")
#
#   except Exception as e:
#     log.ERRO(f"Não foi possível aguardar o carregamento da página.['{cssSelector}']", e.args)


def finalizarNavegadorWeb():
  try:
    if navegadorWeb is not None:
      navegadorWeb.delete_all_cookies()
      navegadorWeb.execute_script("localStorage.clear();")
      navegadorWeb.quit()
      return True
  except Exception as e:
    log.ERRO(f"Não foi possível finalizar navegador web.['{navegadorWeb}']", e.args)
    return False
