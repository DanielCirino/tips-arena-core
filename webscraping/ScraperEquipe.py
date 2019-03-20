#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from webscraping.Scraper import Scraper
from utils.UtilBll import UtilBll


class ScraperEquipe(Scraper):

    def getListaEquipesEdicaoCompeticao(self, urlEdicao):
        try:
            CSS_LINKS_EQUIPE = "td.tp>a"
            documentoHtml = self.getHtmlFromUrl(
                self.URL_BASE + urlEdicao + "equipes/")
            linksEquipe = documentoHtml.select(CSS_LINKS_EQUIPE)

            listaEquipes = []

            for link in linksEquipe:
                listaEquipes.append(
                    {"nome": link.text, "url": link["href"] + "/", "seq": 0})

            return listaEquipes
        except Exception as e:
            print(e.args)
            return []

    def getDadosEquipe(self, urlEquipe):
        try:

            documentoHtml = self.getHtmlFromUrl(self.URL_BASE + urlEquipe)
            linksCabecalho = self.getDadosCabecalho(documentoHtml)

            paisEquipe = {"nome": linksCabecalho[1]["text"],
                          "url": linksCabecalho[1]["href"]}

            nomeEquipe = linksCabecalho[2]["text"]

            urlEscudoEquipe = documentoHtml.select(".team-logo")
            urlEscudoEquipe = urlEscudoEquipe[0]["style"].split("(")[1]
            urlEscudoEquipe = urlEscudoEquipe.replace(")", "")

            return {
                "nome": UtilBll().limparString(nomeEquipe),
                "pais": paisEquipe,
                "urlEscudo": urlEscudoEquipe,
                "url": urlEquipe
            }

        except Exception as e:
            print(e.args)
            return None
