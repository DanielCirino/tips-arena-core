#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from webscraping.Scraper import Scraper
from utils.UtilBll import UtilBll


class ScraperCompeticao(Scraper):

    def getListaCompeicoesPais(self, urlPais):
        try:
            CSS_LISTA_COMPETICOES = "ul.selected-country-list>li>a"
            listaCompeticoes = []
            documentoHtml = self.getHtmlFromUrl(self.URL_BASE + urlPais)

            competicoes = documentoHtml.select(CSS_LISTA_COMPETICOES)

            for competicao in competicoes:
                urlCompet = competicao["href"]
                if urlCompet != "#":
                    listaCompeticoes.append({"url": urlCompet, "seq": 0})

            return listaCompeticoes
        except Exception as e:
            print(e.args)
            return None

    def getDadosCompeticao(self, urlCompeticao):
        try:

            documentoHtml = self.getHtmlFromUrl(self.URL_BASE + urlCompeticao)
            linksCabecalho = self.getDadosCabecalho(documentoHtml)

            paisCompeticao = {"url": linksCabecalho[1]["href"],
                              "nome": linksCabecalho[1]["text"]}

            anoEdicao = linksCabecalho[3]["text"]
            urlCompeticao = linksCabecalho[2]["href"][:-
                                                      1] + "-" + anoEdicao.replace("/", "-") + "/"

            nomeCompeticao = UtilBll().limparString(linksCabecalho[2]["text"])
            logoCompeticao = documentoHtml.select(".tournament-logo")
            logoCompeticao = logoCompeticao[0]["style"].split("(")[1]
            logoCompeticao = logoCompeticao.replace(")", "")

            return {
                "nome": nomeCompeticao,
                "pais": paisCompeticao,
                "urlLogo": logoCompeticao,
                "url": urlCompeticao,
                "anoEdicao": anoEdicao,
                "totalPartidas": 0,
                "totalPartidasFinalizadas": 0,
                "status": "NAO_DEFINIDO",
                "equipeCampea": None
            }

        except Exception as e:
            print(e.args)
            return None

    def getListaEdicoesCompeticao(self, urlCompeticao):
        try:
            CSS_LINHAS_EDICAO = "#tournament-page-archiv table tbody tr"
            listaEdicoes = []
            documentoHtml = self.getHtmlFromUrl(
                self.URL_BASE + urlCompeticao + "arquivo/")

            linksCompeticao = documentoHtml.select(CSS_LINHAS_EDICAO)

            sequencia = 1
            for linha in linksCompeticao:
                links = linha.select(" td a")
                anoCompeticao = links[0].text.split(" ")[-1]
                anoCompeticao = anoCompeticao.replace("/", "-")
                urlEdicao = urlCompeticao[:-1] + "-" + anoCompeticao + "/"

                equipeVencedora = {"nome": "", "url": ""}

                if len(links) > 1:
                    equipeVencedora = {
                        "nome": links[1].text, "url": links[1]["href"]}

                listaEdicoes.append(
                    {"url": urlEdicao, "equipeVencedora": equipeVencedora, "seq": sequencia})
                sequencia += 1

            return listaEdicoes
        except Exception as e:
            print(e.args)
            return None

    def getEdicaoMaisRecenteCompeticao(self, urlCompeticao):
        try:
            edicoes = self.getListaEdicoesCompeticao(urlCompeticao)
            if len(edicoes) > 0:
                return edicoes[0]
        except Exception as e:
            print(e.args)
            return None
