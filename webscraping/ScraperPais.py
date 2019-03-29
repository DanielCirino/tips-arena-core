
# -*- coding: utf-8 -*-

from webscraping.Scraper import Scraper


class ScraperPais(Scraper):

    def getListaPaises(self):
        try:
            CSS_LISTA_PAISES = "ul.country-list.tournament-menu>li[id^=lmenu_]>a"
            documento_html = self.getHtmlFromUrl(self.URL_BASE + "/futebol/")
            paises = documento_html.select(CSS_LISTA_PAISES)
            listaPaises = []

            for urlPais in paises:
                url = urlPais["href"]
                if url != "#":
                    listaPaises.append({"url": url, "seq": 0})

            return listaPaises
        except Exception as e:
            print(e.args)
            return []
