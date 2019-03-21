#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import json
import time
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class Scraper:
    def __init__(self):
        try:
            self.URL_BASE = "https://www.resultados.com"
            self.webDriver = None
            self.pathToDriver = os.environ.get("TA_PATH_TO_WEBDRIVER")

            if self.pathToDriver is None:
                print("Variável de ambiente TA_PATH_TO_WEBDRIVER precisa ser criada.")
                exit(0)
        except Exception as e:
            print(e.args[0])

    def finalizarWebDriver(self):
        try:
            if self.webDriver is not None:
                self.webDriver.delete_all_cookies()
                self.webDriver.execute_script("localStorage.clear();")
                self.webDriver.quit()
                return True
        except Exception as e:
            print(str(e))
            return False

    def setupWebDriver(self):
        try:
            if self.webDriver is None:
                options = Options()
                options.add_argument("--headless")
                caps = webdriver.DesiredCapabilities.FIREFOX
                caps["binary"] = "/usr/bin/firefox"

                self.webDriver = webdriver.Firefox(capabilities=caps,
                                                   executable_path=self.pathToDriver,
                                                   firefox_options=options)
                # self.webDriver = webdriver.Remote(
                #     command_executor='http://127.0.0.1:4444/wd/hub',
                #     desired_capabilities=caps)

        except Exception as e:
            print("Erro ao iniciar webdriver - " +
                  e.args[0] + " - " + self.pathToDriver)
            print(e.args[0])

    def aguardarCarregamentoPagina(self, cssSelector):
        try:
            carregando = self.webDriver.find_element_by_css_selector(
                cssSelector)
            tempoEspera = 0.0

            while carregando.is_displayed():
                time.sleep(0.5)
                tempoEspera += 0.5

                carregando = self.webDriver.find_element_by_css_selector(
                    cssSelector)

                if tempoEspera >= 10:
                    # print("[Erro][Esperou mais de 10 segundos, time out...]")
                    self.webDriver.save_screenshot("erro_loading.png")
                    return None
            # print("Demorou:" + tempo_espera)

        except Exception as e:
            print(str(e))
            return None

    def getHtmlFromUrl(self, url):
        try:
            page = requests.get(url)
            documento_html = BeautifulSoup(page.content, "html.parser")
            page.close()
            return documento_html
        except Exception as e:
            print(e.args)
            return None

    def converterStringParaHtml(self, string):
        try:
            dados_html = BeautifulSoup(string, "html.parser")
            return dados_html
        except Exception as e:
            print(e.args)
            return None

    def getDadosCabecalho(self, html):
        try:
            CSS_LINKS_CABECALHO = "h2.tournament a"
            CSS_TEXTO_CABECALHO = ".breadcrumb__text"
            time.sleep(10)
            cabecalhoCompeticao = html.select(CSS_LINKS_CABECALHO)
            linksCabecalho = []

            for item in cabecalhoCompeticao:
                linksCabecalho.append(
                    {"text": item.text, "href": item.attrs["href"]})

            textoCabecalho = html.select(CSS_TEXTO_CABECALHO)

            if len(textoCabecalho) > 0:
                linksCabecalho.append(
                    {"text": textoCabecalho[0].text, "href": "#"})

            return linksCabecalho
        except Exception as e:
            print(e.args)
            return None

    def getUrlFromOnClick(self, onclick):
        try:
            url = onclick.split("(")[1].split(")")[0].replace("'", "")

            return url
        except Exception as e:
            return ""
