#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from webscraping.Scraper import Scraper


class ScraperEdicaoCompeticao(Scraper):

    def getListaEdicoesCompeticao(self, urlCompeticao):
        try:
            CSS_LISTA_EDICOES = "#tournament-page-archiv table tbody tr"
            listaEdicoes = []
            documentoHtml = self.getHtmlFromUrl(
                self.URL_BASE + urlCompeticao + "arquivo/")

            linksCompeticao = documentoHtml.select(CSS_LISTA_EDICOES)

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

    def getDadosEdicaoCompeticao(self, urlEdicao):
        try:
            documentoHtml = self.getHtmlFromUrl(self.URL_BASE + urlEdicao)

            linksCabecalho = self.getDadosCabecalho(documentoHtml)

            anoEdicao = linksCabecalho[3]["text"]
            urlEdicao = linksCabecalho[2]["href"][:-1] + \
                "-" + anoEdicao.replace("/", "-") + "/"

            competicao = {
                "nome": linksCabecalho[2]["text"],
                "pais": linksCabecalho[1]["text"],
                "url": linksCabecalho[2]["href"]
            }

            return {
                "competicao": competicao,
                "ano": anoEdicao,
                "total_partidas": 0,
                "total_partidas_finalizadas": 0,
                "status": "NAO_DEFINIDO",
                "url": urlEdicao
            }
        except Exception as e:
            print(e.args)
            return None
