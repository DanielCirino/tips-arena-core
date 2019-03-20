#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from webscraping.Scraper import Scraper


class ScraperPais(Scraper):

    def getListaPaises(self):
        try:
            CSS_LISTA_PAISES = "ul.country-list.tournament-menu>li[id^=lmenu_]>a"
            documento_html = self.getHtmlFromUrl(self.URL_BASE + "/futebol/")
            paises = documento_html.select(CSS_LISTA_PAISES)
            lista_paises = []

            for url_pais in paises:
                url = url_pais["href"]
                if url != "#":
                    lista_paises.append({"url": url, "seq": 0})

            return lista_paises
        except Exception as e:
            print(e.args)
            return []
