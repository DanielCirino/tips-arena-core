# -*- coding: utf-8 -*-
import traceback
from enum import Enum
from datetime import datetime
import time

from utils.DateTimeHandler import DateTimeHandler
from utils.HashString import HashString
from webscraping.Scraper import Scraper
from webscraping.ScraperCompeticao import ScraperCompeticao
from models.Partida import Partida
from utils.UtilBll import UtilBll
from webscraping.ScraperEquipe import ScraperEquipe


class ScraperPartida(Scraper):
    def __init__(self):
        try:
            Scraper.__init__(self)
            self.utils = UtilBll()
            self.CASAS_DECIMAIS = 3
        except Exception as e:
            print(e.args[0])

    def obterListaIdsPartida(self):
        try:
            CSS_LINK_LISTAR_MAIS = ".link-more-games tbody tr td a "
            CSS_LOADING = "#preload"
            CSS_LINHAS_PARTIDA = "tr[id^=g_1_]"

            linkListarMais = self.webDriver.find_element_by_css_selector(
                CSS_LINK_LISTAR_MAIS)

            while linkListarMais.is_displayed():
                linkListarMais.click()
                self.aguardarCarregamentoPagina(CSS_LOADING)
                linkListarMais = self.webDriver.find_element_by_css_selector(
                    CSS_LINK_LISTAR_MAIS)

            linhasHtml = self.webDriver.find_elements_by_css_selector(
                CSS_LINHAS_PARTIDA)
            listaIdPartida = []

            for item in linhasHtml:
                id = item.get_attribute("id").split("_")[2]
                listaIdPartida.append({"url": "/jogo/" + id + "/", "seq": 0})

            return listaIdPartida

        except Exception as e:
            print(e.args)
            return []

    def getListaPartidasEdicaoCompeticao(self, urlEdicao):
        try:
            CSS_LOADING = "#preload"
            CSS_LINK_PARTIDAS_AGENDADAS = ".page-tabs>.ifmenu>.li2>span>a"

            if self.webDriver is None:
                self.setupWebDriver()

            urlPartidas = self.URL_BASE + urlEdicao + "resultados/"

            self.webDriver.get(urlPartidas)
            self.aguardarCarregamentoPagina(CSS_LOADING)

            listaPartidasFinalizadas = self.obterListaIdsPartida()

            linkPartidasAgendadas = self.webDriver.find_element_by_css_selector(
                CSS_LINK_PARTIDAS_AGENDADAS)
            linkPartidasAgendadas.click()
            self.aguardarCarregamentoPagina(CSS_LOADING)

            listaPartidasAgendadas = self.obterListaIdsPartida()

            return {"agendadas": listaPartidasFinalizadas,
                    "finalizadas": listaPartidasAgendadas}

        except Exception as e:
            print(e.args)
            return None

    def getListaPartidasDia(self):
        CSS_LOADING = ".loadingOverlay"
        CSS_LINK_YESTERDAY = "div.calendar__direction--yesterday"
        CSS_LINK_TOMORROW = "div.calendar__direction--tomorrow"
        CSS_LINK_EXPAND_LEAGUE = "div.event__info"
        CSS_LINHA_PARTIDA = "div[id^=g_1_]"

        try:
            if self.webDriver is None:
                self.setupWebDriver()

            self.webDriver.get(self.URL_BASE)

            listaPartidas = []
            cont_dia = -3

            while cont_dia < 0:
                cont_dia += 1
                self.aguardarCarregamentoPagina(CSS_LOADING)
                dia_anterior = self.webDriver.find_element_by_css_selector(
                    CSS_LINK_YESTERDAY)
                dia_anterior.click()
                self.aguardarCarregamentoPagina(CSS_LOADING)

            while cont_dia < 6:
                cont_dia += 1

                self.aguardarCarregamentoPagina(CSS_LOADING)

                links_competicao_oculta = self.webDriver.find_elements_by_css_selector(
                    CSS_LINK_EXPAND_LEAGUE)

                for link in links_competicao_oculta:
                    link.click()

                partidas = self.webDriver.find_elements_by_css_selector(
                    CSS_LINHA_PARTIDA)

                for partida in partidas:
                    id = partida.get_attribute("id").split("_")[2]
                    listaPartidas.append("/jogo/" + id + "/")

                proximo_dia = self.webDriver.find_element_by_css_selector(
                    CSS_LINK_TOMORROW)
                proximo_dia.click()
                self.aguardarCarregamentoPagina(CSS_LOADING)

            return listaPartidas

        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__))

            if self.webDriver:
                self.webDriver.save_screenshot("error_screenshot.png")

            return None

    def getDadosPartida(self, urlPartida, extrairTimeline=True, extrairOdds=True, extrairStats=True,
                        extrairUltimasPartidas=True):

        try:
            CSS_LOADING = "#preload-all"
            CSS_CABECALHO_PARTIDA = ".fleft"
            CSS_DADOS_MANDANTE = ".tname-home>div>div>a"
            CSS_DADOS_VISITANTE = ".tname-away>div>div>a"
            CSS_PLACAR_PARTIDA = ".scoreboard"
            CSS_DATA_PARTIDA = ".mstat-date"
            CSS_STATUS_PARTIDA = ".mstat"
            CSS_INFO_PARTIDA = ".info-bubble>span.text"

            partida = {
                "url": str.replace(urlPartida, self.URL_BASE, ""),
                "timeline": [],
                "estatisticas": [],
                "headToHead": {},
                "odds": {}
            }

            if self.webDriver is None:
                self.setupWebDriver()

            self.webDriver.get(self.URL_BASE + urlPartida)
            self.aguardarCarregamentoPagina(CSS_LOADING)

            competicao = {"url": ""}

            cabecalhoPartida = self.webDriver.find_element_by_css_selector(
                CSS_CABECALHO_PARTIDA)
            dadosMandante = self.webDriver.find_element_by_css_selector(
                CSS_DADOS_MANDANTE)
            dadosVisitante = self.webDriver.find_element_by_css_selector(
                CSS_DADOS_VISITANTE)
            placarPartida = self.webDriver.find_elements_by_css_selector(
                CSS_PLACAR_PARTIDA)

            dataPartida = self.webDriver.find_element_by_css_selector(
                CSS_DATA_PARTIDA).text
            partida["dataHora"] = datetime.strptime(
                dataPartida, "%d.%m.%Y %H:%M")
            partida["timezoneOffset"] = DateTimeHandler().local_time_offset(
                time.mktime(partida["dataHora"].timetuple()))

            statusPartida = self.webDriver.find_element_by_css_selector(
                CSS_STATUS_PARTIDA).text.split("-")
            partida["status"] = self.normalizarDescricaoStatus(
                statusPartida[0])

            if len(statusPartida) > 1:
                partida["minutos"] = statusPartida[1]
            else:
                partida["minutos"] = ""

            informacoesPartida = self.webDriver.find_elements_by_css_selector(
                CSS_INFO_PARTIDA)

            if len(informacoesPartida) == 1:
                partida["info"] = informacoesPartida[0].text

            faseCompeticao = cabecalhoPartida.text.split("-")
            partida["faseCompeticao"] = "-".join(faseCompeticao[1:])
            partida["faseCompeticao"] = self.utils.limparString(
                partida["faseCompeticao"])

            competicao["nome"] = cabecalhoPartida.text.split(":")[
                1].split(" - ")[0]

            urlCompeticao = self.getUrlFromOnClick(
                cabecalhoPartida.find_element_by_css_selector("span a").get_attribute("onclick"))

            urlEquipeMandante = dadosMandante.get_attribute("onclick").split("(")[1].split(")")[
                                    0].replace(
                "'", "") + "/"

            urlEquipeVisitante = dadosVisitante.get_attribute("onclick").split("(")[1].split(")")[
                                     0].replace(
                "'",
                "") + "/"

            competicao["url"] = urlCompeticao

            competicao = ScraperCompeticao().getDadosCompeticao(urlCompeticao)

            equipeMandante = ScraperEquipe().getDadosEquipe(urlEquipeMandante)
            equipeVisitante = ScraperEquipe().getDadosEquipe(urlEquipeVisitante)

            placarMandantePrimeiroTempo = self.webDriver.find_elements_by_css_selector(
                ".p1_home")
            placarMandanteSegundoTempo = self.webDriver.find_elements_by_css_selector(
                ".p2_home")
            placarMandanteProrrogacao = self.webDriver.find_elements_by_css_selector(
                ".p3_home")
            placarMandantePenalties = self.webDriver.find_elements_by_css_selector(
                ".p3_home")

            placarVisitantePrimeiroTempo = self.webDriver.find_elements_by_css_selector(
                ".p1_away")
            placarVisitanteSegundoTempo = self.webDriver.find_elements_by_css_selector(
                ".p2_away")
            placarVisitanteProrrogacao = self.webDriver.find_elements_by_css_selector(
                ".p3_away")
            placarVisitantePenalties = self.webDriver.find_elements_by_css_selector(
                ".p3_away")

            if len(placarPartida) == 0:
                placarPartida = ["", ""]
            elif len(placarPartida) == 2:
                placarPartida = [placarPartida[0].text, placarPartida[1].text]

            elif len(placarPartida) == 4:
                placarPartida = [placarPartida[2].text, placarPartida[3].text]

            if len(placarMandantePrimeiroTempo) > 0:
                placarMandantePrimeiroTempo = placarMandantePrimeiroTempo[0].text
            else:
                placarMandantePrimeiroTempo = ""

            if len(placarVisitantePrimeiroTempo) > 0:
                placarVisitantePrimeiroTempo = placarVisitantePrimeiroTempo[0].text
            else:
                placarVisitantePrimeiroTempo = ""

            if len(placarMandanteSegundoTempo) > 0:
                placarMandanteSegundoTempo = placarMandanteSegundoTempo[0].text
            else:
                placarMandanteSegundoTempo = ""

            if len(placarVisitanteSegundoTempo) > 0:
                placarVisitanteSegundoTempo = placarVisitanteSegundoTempo[0].text
            else:
                placarVisitanteSegundoTempo = ""

            if len(placarMandanteProrrogacao) > 0:
                placarMandanteProrrogacao = placarMandanteProrrogacao[0].text
            else:
                placarMandanteProrrogacao = ""

            if len(placarVisitanteProrrogacao) > 0:
                placar_visitante_prorrogacao = placarVisitanteProrrogacao[0].text
            else:
                placar_visitante_prorrogacao = ""

            if len(placarMandantePenalties) > 0:
                placarMandantePenalties = placarMandantePenalties[0].text
            else:
                placarMandantePenalties = ""

            if len(placarVisitantePenalties) > 0:
                placarVisitantePenalties = placarVisitantePenalties[0].text
            else:
                placarVisitantePenalties = ""

            partida["placarFinal"] = ":".join(placarPartida)
            partida["placarPrimeiroTempo"] = placarMandantePrimeiroTempo + \
                                             ":" + placarVisitantePrimeiroTempo
            partida["placarSegundoTempo"] = placarMandanteSegundoTempo + \
                                            ":" + placarVisitanteSegundoTempo
            partida["placarProrrogacao"] = placarMandanteProrrogacao + \
                                           ":" + placar_visitante_prorrogacao
            partida["placarPenalties"] = placarMandantePenalties + \
                                         ":" + placarVisitantePenalties

            partida["idEquipeMandante"] = HashString().encode(
                equipeMandante["url"])
            partida["idEquipeVisitante"] = HashString().encode(
                equipeVisitante["url"])

            partida["competicao"] = competicao
            partida["equipeMandante"] = equipeMandante
            partida["equipeVisitante"] = equipeVisitante

            partida["tags"] = [self.utils.limparString(competicao["nome"]),
                               self.utils.limparString(equipeMandante["nome"]),
                               self.utils.limparString(equipeVisitante["nome"])
                               ]

            linksInformacoesDisponiveis = self.webDriver.find_elements_by_css_selector(
                "a[id^=a-match-]")

            informacoesDiponiveis = self.verificarInformacoesDisponiveis(
                linksInformacoesDisponiveis)

            partida["timelineDisponivel"] = informacoesDiponiveis["timeline"]
            partida["estatisticasDisponiveis"] = informacoesDiponiveis["statistics"]
            partida["oddsDisponiveis"] = informacoesDiponiveis["odds-comparison"]
            partida["relatorioDisponivel"] = informacoesDiponiveis["commentary"]
            partida["lineupsDisponivel"] = informacoesDiponiveis["lineups"]
            partida["headToHeadDisponivel"] = informacoesDiponiveis["head-2-head"]
            partida["videosDisponiveis"] = informacoesDiponiveis["highlights"]
            partida["fotosDisponiveis"] = informacoesDiponiveis["photoreport"]
            partida["noticiasDisponiveis"] = informacoesDiponiveis["newsfeed"]

            if partida["timelineDisponivel"] and extrairTimeline:

                htmlTimeline = self.webDriver.find_elements_by_css_selector(
                    "#summary-content>div.detailMS")
                if len(htmlTimeline) > 0:
                    partida["timeline"] = self.getTimelinePartida(
                        htmlTimeline[0].get_attribute("innerHTML"))

            if partida["estatisticasDisponiveis"] and extrairStats:
                partida["estatisticas"] = self.getEstatisticasPartida()

            if partida["oddsDisponiveis"] and extrairOdds:
                partida["odds"] = self.getOddsPartida()

            if partida["headToHeadDisponivel"] and extrairUltimasPartidas:
                partida["headToHead"] = self.obterUltimasPartidasEquipes()

            return partida

        except Exception as e:
            print(str(e))
            return None

    def verificarInformacoesDisponiveis(self, htmlLinks):
        try:
            infos = {
                "timeline": False,
                "statistics": False,
                "lineups": False,
                "commentary": False,
                "odds-comparison": False,
                "head-2-head": False,
                "highlights": False,
                "photoreport": False,
                "newsfeed": False,

            }

            for link in htmlLinks:
                idLink = link.get_attribute("id").replace("a-match-", "")
                infos[idLink] = True

            return infos
        except Exception as e:
            print(e.args)
            return infos

    def getOddsPartida(self):
        try:
            bookmakers = {
                "resultado": {},
                "duplaChance": {},
                "drawNoBet": {},
                "oddEven": {},
                "btts": {},
                "underOver": [],
                "placarExato": []
            }
            mercadosDisponiveis = self.getMercadosApostaDisponiveis()

            for mercado in mercadosDisponiveis:
                link_mercado = self.webDriver.find_element_by_css_selector(
                    "#{}>span>a".format(mercado["id_link"]))
                link_mercado.click()
                odds = self.getOddsPorMercado(mercado)

                if mercado["tipo"] == self.TipoMercado.RESULTADO:
                    bookmakers["resultado"] = odds

                elif mercado["tipo"] == self.TipoMercado.DUPLA_CHANCE:
                    bookmakers["duplaChance"] = odds

                elif mercado["tipo"] == self.TipoMercado.DNB:
                    bookmakers["drawNoBet"] = odds

                elif mercado["tipo"] == self.TipoMercado.ODD_EVEN:
                    bookmakers["oddEven"] = odds

                elif mercado["tipo"] == self.TipoMercado.BTTS:
                    bookmakers["btts"] = odds

                elif mercado["tipo"] == self.TipoMercado.UNDER_OVER:
                    bookmakers["underOver"] = odds

                elif mercado["tipo"] == self.TipoMercado.PLACAR:
                    bookmakers["placarExato"] = odds

            return bookmakers

        except Exception as e:
            print(e.args)
            return bookmakers

    def getMercadosApostaDisponiveis(self):
        try:
            CSS_LINK_ODDS = "#a-match-odds-comparison"
            CSS_LISTA_ODDS = "#tab-match-odds-comparison>#odds-comparison-content>.odds-comparison-bookmark >ul.ifmenu>li"

            linkOdds = self.webDriver.find_element_by_css_selector(
                CSS_LINK_ODDS)
            linkOdds.click()

            self.aguardarCarregamentoPagina("#odds-comparison-preload")

            listaOdds = self.webDriver.find_elements_by_css_selector(
                CSS_LISTA_ODDS)
            listaBookmakers = []

            for odd in listaOdds:
                id_bookmark = odd.get_attribute("id")
                bookmark = {"id_link": id_bookmark,
                            "tipo": "",
                            "id_url": id_bookmark.replace("bookmark-", "") + "-odds"}

                if id_bookmark == 'bookmark-1x2':
                    bookmark["tipo"] = self.TipoMercado.RESULTADO
                elif id_bookmark == 'bookmark-under-over':
                    bookmark["tipo"] = self.TipoMercado.UNDER_OVER
                elif id_bookmark == 'bookmark-moneyline':
                    bookmark["tipo"] = self.TipoMercado.DNB
                # elif id_bookmark == 'bookmark-asian-handicap':
                #     print('')
                # elif id_bookmark == 'bookmark-european-handicap':
                #     print('')
                elif id_bookmark == 'bookmark-double-chance':
                    bookmark["tipo"] = self.TipoMercado.DUPLA_CHANCE
                # elif id_bookmark == 'bookmark-ht-ft':
                #     print('')
                elif id_bookmark == 'bookmark-correct-score':
                    bookmark["tipo"] = self.TipoMercado.PLACAR
                elif id_bookmark == 'bookmark-oddeven':
                    bookmark["tipo"] = self.TipoMercado.ODD_EVEN
                elif id_bookmark == 'bookmark-both-teams-to-score':
                    bookmark["tipo"] = self.TipoMercado.BTTS
                else:
                    pass

                listaBookmakers.append(bookmark)

            return listaBookmakers

        except Exception as e:
            print(e.args[0])
            return []

    def getOddsPorMercado(self, mercado):
        try:
            CSS_TABELA_ODDS_RESULTADO = "#block-1x2-ft>table>tbody>tr"
            CSS_TABELA_ODDS_UNDER_OVER = "#block-under-over-ft>table"
            CSS_TABELA_ODDS_DNB = "#block-moneyline-ft>table>tbody>tr"
            CSS_TABELA_ODDS_BTTS = "div#block-both-teams-to-score-ft>table>tbody>tr"
            CSS_TABELA_ODDS_PLACAR = "#block-correct-score-ft>table"
            CSS_TABELA_ODDS_ODD_EVEN = "#block-oddeven-ft>table>tbody>tr"
            CSS_TABELA_ODDS_DUPLA_CHANCE = "#block-double-chance-ft>table>tbody>tr"

            listaOdds = []

            if mercado["tipo"] == self.TipoMercado.RESULTADO:
                tabelaOdds = self.webDriver.find_elements_by_css_selector(
                    CSS_TABELA_ODDS_RESULTADO)
                listaOdds = self.getOddsResultado(tabelaOdds)

            if mercado["tipo"] == self.TipoMercado.UNDER_OVER:
                tabelaOdds = self.webDriver.find_elements_by_css_selector(
                    CSS_TABELA_ODDS_UNDER_OVER)

                for tabela in tabelaOdds:
                    qtd_gols = tabela.get_attribute("id").split("_")[-1]

                    if ".5" in qtd_gols:
                        odds = self.getOddsUnderOver(
                            tabela.find_elements_by_css_selector("tbody>tr"), qtd_gols)
                        listaOdds.append(odds)

            if mercado["tipo"] == self.TipoMercado.DNB:
                tabelaOdds = self.webDriver.find_elements_by_css_selector(
                    CSS_TABELA_ODDS_DNB)
                listaOdds = self.getOddsDrawNoBet(tabelaOdds)

            if mercado["tipo"] == self.TipoMercado.BTTS:
                tabelaOdds = self.webDriver.find_elements_by_css_selector(
                    CSS_TABELA_ODDS_BTTS)
                listaOdds = self.getOddsBtts(tabelaOdds)

            if mercado["tipo"] == self.TipoMercado.PLACAR:
                tabelaOdds = self.webDriver.find_elements_by_css_selector(
                    CSS_TABELA_ODDS_PLACAR)

                for tabela in tabelaOdds:
                    odds = self.getOddsPlacarExato(
                        tabela.find_elements_by_css_selector("tbody>tr"))
                    listaOdds.append(odds)

            if mercado["tipo"] == self.TipoMercado.ODD_EVEN:
                tabelaOdds = self.webDriver.find_elements_by_css_selector(
                    CSS_TABELA_ODDS_ODD_EVEN)
                listaOdds = self.getOddsImparPar(tabelaOdds)

            if mercado["tipo"] == self.TipoMercado.DUPLA_CHANCE:
                tabelaOdds = self.webDriver.find_elements_by_css_selector(
                    CSS_TABELA_ODDS_DUPLA_CHANCE)
                listaOdds = self.getOddsDuplaChance(tabelaOdds)

            return listaOdds

        except Exception as e:
            print(e.args[0])

    def getOddsResultado(self, bookmakers):

        quantidadeOdds = len(bookmakers)
        redutorQuantidadeMandante = 0
        redutorQuantidadeEmpate = 0
        redutorQuantidadeVisitante = 0

        valorOddsMandante = 0
        valorOddsEmpate = 0
        valorOddsVisitante = 0

        try:
            for linha in bookmakers:
                campos = linha.find_elements_by_css_selector("td>span")

                oddMandante = campos[0].text.replace("-", "0")
                oddEmpate = campos[1].text.replace("-", "0")
                oddVisitante = campos[2].text.replace("-", "0")

                if oddMandante == "0": redutorQuantidadeMandante += 1
                if oddEmpate == "0": redutorQuantidadeEmpate += 1
                if oddVisitante == "0": redutorQuantidadeVisitante += 1

                valorOddsMandante += float(oddMandante)
                valorOddsEmpate += float(oddEmpate)
                valorOddsVisitante += float(oddVisitante)

            return {
                "mandante": round(valorOddsMandante / (quantidadeOdds - redutorQuantidadeMandante),
                                  self.CASAS_DECIMAIS),
                "empate": round(valorOddsEmpate / (quantidadeOdds - redutorQuantidadeEmpate), self.CASAS_DECIMAIS),
                "visitante": round(valorOddsVisitante / (quantidadeOdds - redutorQuantidadeVisitante),
                                   self.CASAS_DECIMAIS)
            }

        except Exception as e:
            print(e.args[0])
            return {}

    def getOddsDrawNoBet(self, tabelaOdds):
        quantidadeOdds = len(tabelaOdds)
        redutorQuantidadeMandante = 0
        redutorQuantidadeVisitante = 0

        valorOddsMandante = 0
        valorOddsVisitante = 0

        try:

            for linha in tabelaOdds:
                campos = linha.find_elements_by_css_selector("td>span")

                oddMandante = campos[0].text.replace("-", "0")
                oddVisitante = campos[1].text.replace("-", "0")

                if oddMandante == "0": redutorQuantidadeMandante += 1
                if oddVisitante == "0": redutorQuantidadeVisitante += 1

                valorOddsMandante += float(oddMandante)
                valorOddsVisitante += float(oddVisitante)

            return {
                "mandante": round(valorOddsMandante / (quantidadeOdds - redutorQuantidadeMandante),
                                  self.CASAS_DECIMAIS),
                "visitante": round(valorOddsVisitante / (quantidadeOdds - redutorQuantidadeVisitante),
                                   self.CASAS_DECIMAIS)
            }

        except Exception as e:
            print(e.args[0])
            return {}

    def getOddsUnderOver(self, tabelaOdds, quantidadeGols):
        quantidadeOdds = len(tabelaOdds)
        redutorQuantidadeUnder = 0
        redutorQuantidadeOver = 0

        valorOddsOver = 0
        valorOddsUnder = 0

        try:
            for linha in tabelaOdds:
                campos = linha.find_elements_by_css_selector("td>span")

                oddOver = campos[0].text.replace("-", "0")
                oddUnder = campos[1].text.replace("-", "0")

                if oddOver == "0": redutorQuantidadeOver += 1
                if oddUnder == "0": redutorQuantidadeUnder += 1

                valorOddsOver += float(oddOver)
                valorOddsUnder += float(oddUnder)

            return {
                "totalGols": quantidadeGols,
                "under": round(valorOddsUnder / (quantidadeOdds - redutorQuantidadeUnder), self.CASAS_DECIMAIS),
                "over": round(valorOddsOver / (quantidadeOdds - redutorQuantidadeOver), self.CASAS_DECIMAIS)
            }

        except Exception as e:
            print(e.args[0])
            return {}

    def getOddsPlacarExato(self, tabelaOdds):
        quantidadeOdds = len(tabelaOdds)
        redutorQuantidadeOdds = 0

        valorOddsPlacar = 0

        try:
            for linha in tabelaOdds:
                campos = linha.find_elements_by_css_selector("td>span")
                placar = linha.find_element_by_css_selector(
                    "td.correct_score").text

                oddPlacar = campos[0].text.replace("-", "0")
                if oddPlacar == "0": redutorQuantidadeOdds += 1

                valorOddsPlacar += float(oddPlacar)

            placar = placar.split(":")

            return {
                "placarMandante": placar[0],
                "placarVisitante": placar[1],
                "valor": round(valorOddsPlacar / (quantidadeOdds - redutorQuantidadeOdds), self.CASAS_DECIMAIS)
            }
        except Exception as e:
            print(e.args[0])
            return {}

    def getOddsBtts(self, tabelaOdds):
        quantidadeOdds = len(tabelaOdds)
        redutorQuantidadeBtts = 0
        redutorQuantidadeNoBtts = 0

        valorOddsBtts = 0
        valorOddsNoBtts = 0

        try:

            for linha in tabelaOdds:
                campos = linha.find_elements_by_css_selector("td>span")

                oddBtts = campos[0].text.replace("-", "0")
                oddNoBtts = campos[1].text.replace("-", "0")

                if oddBtts == "0": redutorQuantidadeBtts += 1
                if oddNoBtts == "0": redutorQuantidadeNoBtts += 1

                valorOddsBtts += float(oddBtts)
                valorOddsNoBtts += float(oddNoBtts)

            return {
                "yes": round(valorOddsBtts / (quantidadeOdds - redutorQuantidadeBtts), self.CASAS_DECIMAIS),
                "no": round(valorOddsNoBtts / (quantidadeOdds - redutorQuantidadeNoBtts), self.CASAS_DECIMAIS)
            }

        except Exception as e:
            print(e.args[0])
            return {}

    def getOddsImparPar(self, tabelaOdds):
        quantidadeOdds = len(tabelaOdds)
        redutorQuantidadeImpar = 0
        redutorQuantidadePar = 0

        valorOddImpar = 0
        valorOddPar = 0

        try:
            for linha in tabelaOdds:
                campos = linha.find_elements_by_css_selector("td>span")

                oddImpar = campos[0].text.replace("-", "0")
                oddPar = campos[1].text.replace("-", "0")

                if oddImpar == "0": redutorQuantidadeImpar += 1
                if oddPar == "0": redutorQuantidadePar += 1

                valorOddImpar += float(oddImpar)
                valorOddPar += float(oddPar)

            return {
                "odd": round(valorOddImpar / (quantidadeOdds - redutorQuantidadeImpar), self.CASAS_DECIMAIS),
                "even": round(valorOddPar / (quantidadeOdds - redutorQuantidadePar), self.CASAS_DECIMAIS)
            }

        except Exception as e:
            print(e.args[0])
            return {}

    def getOddsDuplaChance(self, tabelaOdds):
        total_odds = len(tabelaOdds)
        redutorQuantidadeContraMandante = 0
        redutorQuantidadeContraEmpate = 0
        redutorQuantidadeContraVisitante = 0

        valorOddContraMandante = 0
        valorOddContraEmpate = 0
        valorOddContraVisitante = 0

        try:
            for linha in tabelaOdds:
                campos = linha.find_elements_by_css_selector("td>span")

                oddContraVisitante = campos[0].text.replace("-", "0")
                oddContraEmpate = campos[1].text.replace("-", "0")
                oddContraMandante = campos[2].text.replace("-", "0")

                if oddContraMandante == "0": redutorQuantidadeContraMandante += 1
                if oddContraEmpate == "0": redutorQuantidadeContraEmpate += 1
                if oddContraVisitante == "0": redutorQuantidadeContraVisitante += 1

                valorOddContraMandante += float(oddContraMandante)
                valorOddContraEmpate += float(oddContraEmpate)
                valorOddContraVisitante += float(oddContraVisitante)

            return {
                "contraVisitante": round(valorOddContraVisitante / (total_odds - redutorQuantidadeContraVisitante),
                                         self.CASAS_DECIMAIS),
                "contraMandante": round(valorOddContraMandante / (total_odds - redutorQuantidadeContraEmpate),
                                        self.CASAS_DECIMAIS),
                "contraEmpate": round(valorOddContraEmpate / (total_odds - redutorQuantidadeContraEmpate),
                                      self.CASAS_DECIMAIS)
            }

        except Exception as e:
            print(e.args[0])
            return {}

    def getTimelinePartida(self, htmlEventos):
        listaEventos = []

        dadosHtml = self.converterStringParaHtml(htmlEventos)

        try:

            htmlEventos = dadosHtml.select(".detailMS__incidentRow")

            contadorEventos = 1

            for html in htmlEventos:
                eventoPartida = {"seq": contadorEventos,
                                 "tipo": "",
                                 "equipe": "",
                                 "minutos": "",
                                 "participante_01": "",
                                 "participante_02": ""
                                 }

                classeCss = html.attrs["class"][1]

                if classeCss != "--empty":
                    if classeCss == "incidentRow--away":
                        eventoPartida["equipe"] = "V"
                    elif classeCss == "incidentRow--home":
                        eventoPartida["equipe"] = "M"

                    eventoPartida["tipo"] = \
                        html.select(".icon-box span")[0].attrs["class"][1]
                    eventoPartida["minutos"] = html.select(
                        ".time-box,.time-box-wide")[0].getText()

                    participanteUm = {"nome": "", "url": ""}
                    participanteDois = {"nome": "", "url": ""}

                    htmlParticipantes = html.select(
                        ".participant-name a,.substitution-in-name a,.substitution-out-name a")

                    if len(htmlParticipantes) >= 1:
                        participanteUm["nome"] = self.utils.limparString(
                            htmlParticipantes[0].getText())

                        participanteUm["url"] = self.getUrlFromOnClick(
                            htmlParticipantes[0].attrs["onclick"])

                    if len(htmlParticipantes) == 2:
                        participanteDois["nome"] = self.utils.limparString(
                            htmlParticipantes[1].getText())

                        participanteDois["url"] = self.getUrlFromOnClick(
                            htmlParticipantes[1].attrs["onclick"])

                    eventoPartida["participante_01"] = participanteUm
                    eventoPartida["participante_02"] = participanteDois

                    eventoPartida["tipo"] = self.normalizarDescricaoEvento(
                        eventoPartida["tipo"])

                    listaEventos.append(eventoPartida)
                    contadorEventos += 1

            return listaEventos

        except Exception as e:
            print(e.args)
            return listaEventos

    def getEstatisticasPartida(self):
        try:
            linkEstatisticas = self.webDriver.find_element_by_css_selector(
                "#a-match-statistics")
            linkEstatisticas.click()

            self.aguardarCarregamentoPagina("#statistics-preload")

            estatisticasPartida = []
            html_stats = self.webDriver.find_elements_by_css_selector(
                "#tab-statistics-0-statistic>.statRow")

            for html in html_stats:
                estatistica = {"desc": "",
                               "valor_mandante": "", "valor_visitante": ""}

                camposEstatistica = html.find_elements_by_css_selector(
                    ".statTextGroup>.statText")

                estatistica["desc"] = self.utils.limparString(
                    camposEstatistica[1].text)
                estatistica["valor_mandante"] = self.utils.limparString(
                    camposEstatistica[0].text)
                estatistica["valor_visitante"] = self.utils.limparString(
                    camposEstatistica[2].text)

                estatisticasPartida.append(estatistica)

            return estatisticasPartida

        except Exception as e:
            print(e.args)
            return estatisticasPartida

    def obterUltimasPartidasEquipes(self):
        ultimasPartidas = {
            "mandante": [],
            "visitante": [],
            "confrontosDiretos": []
        }

        try:
            CSS_LINK_HEAD_2_HEAD = "#a-match-head-2-head"
            CSS_LOADING = "#head-2-head-preload"

            CSS_TABLE_PARTIDAS_MANDANTE = "table.h2h_home"
            CSS_TABLE_PARTIDAS_VISITANTE = "table.h2h_away"
            CSS_TABLE_PARTIDAS_DIRETOS = "table.h2h_mutual"

            linkHeadToHead = self.webDriver.find_element_by_css_selector(CSS_LINK_HEAD_2_HEAD)
            linkHeadToHead.click()

            self.aguardarCarregamentoPagina(CSS_LOADING)

            html = self.webDriver.find_element_by_css_selector("#tab-h2h-overall").get_attribute("innerHTML")

            # html = '<div class="h2h-wrapper"><table class="head_to_head h2h_home"><colgroup><col width="1%"><col width="1%"><col width="48%"><col width="48%"><col width="1%"><col width="1%"></colgroup><thead><tr><td colspan="6" class="h-part last">Últimos jogos: SAN LORENZO</td></tr></thead><tbody><tr class="odd highlight" onclick="detail_open("g_0_ILKvTGtG", null, "", "", "2019", false)"><td><span class="date">19.04.19</span></td><td class="flag_td " title="Copa de la Superliga (Argentina), "><span class="flag fl_22"></span>COS</td><td class="name"><span>Huracan</span></td><td class="name highTeam"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>0 : 1</strong><br>(0 : 0)</span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate/Vitória" class="form-bg-last form-wo"><span></span></a></span></td></tr><tr class="even highlight" onclick="detail_open("g_0_61Z4GwcA", null, "", "", "2019", false)"><td><span class="date">14.04.19</span></td><td class="flag_td " title="Copa de la Superliga (Argentina), "><span class="flag fl_22"></span>COS</td><td class="name highTeam"><span>San Lorenzo</span></td><td class="name"><span>Huracan</span></td><td class=""><span class="score"><strong>0 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="odd highlight" onclick="detail_open("g_0_vsl52EUH", null, "", "", "2019", false)"><td><span class="date">09.04.19</span></td><td class="flag_td " title="Copa Libertadores (América do Sul), "><span class="flag fl_3"></span>LIB</td><td class="name highTeam"><span><strong>San Lorenzo</strong></span></td><td class="name"><span>Melgar</span></td><td class=""><span class="score"><strong>2 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight" onclick="detail_open("g_0_f7yUGGNP", null, "", "", "2018-2019", false)"><td><span class="date">05.04.19</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name"><span>San Martin Tucuman</span></td><td class="name highTeam"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>0 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="odd highlight" onclick="detail_open("g_0_v1v4jkG9", null, "", "", "2019", false)"><td><span class="date">02.04.19</span></td><td class="flag_td " title="Copa Libertadores (América do Sul), "><span class="flag fl_3"></span>LIB</td><td class="name highTeam"><span><strong>San Lorenzo</strong></span></td><td class="name"><span>Palmeiras</span></td><td class=""><span class="score"><strong>1 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_x8M636m9", null, "", "", "2018-2019", false)"><td><span class="date">30.03.19</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name highTeam"><span>San Lorenzo</span></td><td class="name"><span>Gimnasia L.P.</span></td><td class=""><span class="score"><strong>1 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_I73bhRMH", null, "", "", "2018-2019", false)"><td><span class="date">23.03.19</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name"><span>Colon</span></td><td class="name highTeam"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>1 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_2DdS6Kx4", null, "", "", "2018-2019", false)"><td><span class="date">17.03.19</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name"><span>Rosario</span></td><td class="name highTeam"><span><strong>San Lorenzo</strong></span></td><td class=""><span class="score"><strong>0 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_pvu0iV03", null, "", "", "2019", false)"><td><span class="date">13.03.19</span></td><td class="flag_td " title="Copa Libertadores (América do Sul), "><span class="flag fl_3"></span>LIB</td><td class="name highTeam"><span><strong>San Lorenzo</strong></span></td><td class="name"><span>Junior</span></td><td class=""><span class="score"><strong>1 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_K831qQvt", null, "", "", "2018-2019", false)"><td><span class="date">09.03.19</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name"><span><strong>Boca Juniors</strong></span></td><td class="name highTeam"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>3 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_IRad4z05", null, "", "", "2019", false)"><td><span class="date">05.03.19</span></td><td class="flag_td " title="Copa Libertadores (América do Sul), "><span class="flag fl_3"></span>LIB</td><td class="name"><span>Melgar</span></td><td class="name highTeam"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>0 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_rBjVtXIs", null, "", "", "2018-2019", false)"><td><span class="date">01.03.19</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name highTeam"><span>San Lorenzo</span></td><td class="name"><span><strong>Argentinos Jrs</strong></span></td><td class=""><span class="score"><strong>2 : 3</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_MuxwCCJ7", null, "", "", "2018-2019", false)"><td><span class="date">23.02.19</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name"><span>Belgrano</span></td><td class="name highTeam"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>0 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_hn5m1e5k", null, "", "", "2018-2019", false)"><td><span class="date">16.02.19</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name highTeam"><span>San Lorenzo</span></td><td class="name"><span>Newells Old Boys</span></td><td class=""><span class="score"><strong>1 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_K09KtUN5", null, "", "", "2018-2019", false)"><td><span class="date">02.02.19</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name highTeam"><span>San Lorenzo</span></td><td class="name"><span>Independiente</span></td><td class=""><span class="score"><strong>0 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_8UJu1GgE", null, "", "", "2018-2019", false)"><td><span class="date">25.01.19</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name"><span><strong>Defensa y Justicia</strong></span></td><td class="name highTeam"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>1 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_6kTELmz5", null, "", "", "2018-2019", false)"><td><span class="date">20.01.19</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name highTeam"><span>San Lorenzo</span></td><td class="name"><span>Huracan</span></td><td class=""><span class="score"><strong>0 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_0n5c1Pmc", null, "", "", "2018-2019", false)"><td><span class="date">08.12.18</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name highTeam"><span>San Lorenzo</span></td><td class="name"><span>Estudiantes</span></td><td class=""><span class="score"><strong>1 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_nN3mzmkb", null, "", "", "2018-2019", false)"><td><span class="date">02.12.18</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name"><span>Aldosivi</span></td><td class="name highTeam"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>2 : 2</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_lIWyQm90", null, "", "", "2018-2019", false)"><td><span class="date">18.11.18</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name highTeam"><span>San Lorenzo</span></td><td class="name"><span><strong>Atl. Tucuman</strong></span></td><td class=""><span class="score"><strong>0 : 2</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_EypC5yp7", null, "", "", "2018-2019", false)"><td><span class="date">12.11.18</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name"><span>Velez Sarsfield</span></td><td class="name highTeam"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>0 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_6c1Vhb01", null, "", "", "2018-2019", false)"><td><span class="date">04.11.18</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name highTeam"><span>San Lorenzo</span></td><td class="name"><span><strong>Talleres Córdoba</strong></span></td><td class=""><span class="score"><strong>0 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_WzJuNaJi", null, "", "", "2018", false)"><td><span class="date">31.10.18</span></td><td class="flag_td " title="Copa Argentina (Argentina), "><span class="flag fl_22"></span>COP</td><td class="name highTeam"><span>San Lorenzo</span></td><td class="name"><span>Temperley</span></td><td class=""><span class="score"><strong>1 : 2</strong><br>(1 : 1)</span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate/Derrota" class="form-bg-last form-lo"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_dbGiioPd", null, "", "", "2018-2019", false)"><td><span class="date">28.10.18</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name"><span><strong>Racing Club</strong></span></td><td class="name highTeam"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>2 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_6gJQxnA3", null, "", "", "2018-2019", false)"><td><span class="date">22.10.18</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name highTeam"><span><strong>San Lorenzo</strong></span></td><td class="name"><span>San Martin S.J.</span></td><td class=""><span class="score"><strong>2 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_QHxufSNt", null, "", "", "2018-2019", false)"><td><span class="date">07.10.18</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name"><span><strong>Banfield</strong></span></td><td class="name highTeam"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>2 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_8pGCsH1n", null, "", "", "2018", false)"><td><span class="date">03.10.18</span></td><td class="flag_td " title="Copa Argentina (Argentina), "><span class="flag fl_22"></span>COP</td><td class="name"><span>Estudiantes</span></td><td class="name highTeam"><span><strong>San Lorenzo</strong></span></td><td class=""><span class="score"><strong>1 : 3</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_xCxiIKTJ", null, "", "", "2018", false)"><td><span class="date">25.09.18</span></td><td class="flag_td " title="Copa Sul-Americana (América do Sul), "><span class="flag fl_3"></span>SUL</td><td class="name"><span><strong>Nacional</strong></span></td><td class="name highTeam"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>2 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_zkFQJCnR", null, "", "", "2018-2019", false)"><td><span class="date">21.09.18</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name highTeam"><span><strong>San Lorenzo</strong></span></td><td class="name"><span>Patronato</span></td><td class=""><span class="score"><strong>3 : 2</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_p4xF1DQr", null, "", "", "2018-2019", false)"><td><span class="date">16.09.18</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name"><span><strong>Godoy Cruz</strong></span></td><td class="name highTeam"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>1 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_GdvMlmic", null, "", "", "2018", false)"><td><span class="date">07.09.18</span></td><td class="flag_td " title="Copa Argentina (Argentina), "><span class="flag fl_22"></span>COP</td><td class="name highTeam"><span>San Lorenzo</span></td><td class="name"><span>Colon</span></td><td class=""><span class="score"><strong>3 : 2</strong><br>(2 : 2)</span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate/Vitória" class="form-bg-last form-wo"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_KtFZjNCN", null, "", "", "2018-2019", false)"><td><span class="date">01.09.18</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name highTeam"><span>San Lorenzo</span></td><td class="name"><span>River Plate</span></td><td class=""><span class="score"><strong>1 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_h88Dc7Tu", null, "", "", "2018-2019", false)"><td><span class="date">27.08.18</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name"><span>Union Santa Fe</span></td><td class="name highTeam"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>1 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_z7b8gyiJ", null, "", "", "2018", false)"><td><span class="date">22.08.18</span></td><td class="flag_td " title="Copa Sul-Americana (América do Sul), "><span class="flag fl_3"></span>SUL</td><td class="name highTeam"><span><strong>San Lorenzo</strong></span></td><td class="name"><span>Nacional</span></td><td class=""><span class="score"><strong>3 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_fa1ESnU5", null, "", "", "2018-2019", false)"><td><span class="date">19.08.18</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name highTeam"><span>San Lorenzo</span></td><td class="name"><span>Lanus</span></td><td class=""><span class="score"><strong>2 : 2</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_xYiVHJ5a", null, "", "", "2018", false)"><td><span class="date">15.08.18</span></td><td class="flag_td " title="Copa Sul-Americana (América do Sul), "><span class="flag fl_3"></span>SUL</td><td class="name"><span><strong>Deportes Temuco</strong></span></td><td class="name highTeam"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>1 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_Gj7QTy9r", null, "", "", "2018-2019", false)"><td><span class="date">10.08.18</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name"><span>Tigre</span></td><td class="name highTeam"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>2 : 2</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_GtdNlLyD", null, "", "", "2018", false)"><td><span class="date">26.07.18</span></td><td class="flag_td " title="Copa Sul-Americana (América do Sul), "><span class="flag fl_3"></span>SUL</td><td class="name highTeam"><span><strong>San Lorenzo</strong></span></td><td class="name"><span>Deportes Temuco</span></td><td class=""><span class="score"><strong>3 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_nBLdUPDh", null, "", "", "2018", false)"><td><span class="date">16.07.18</span></td><td class="flag_td " title="Copa Argentina (Argentina), "><span class="flag fl_22"></span>COP</td><td class="name highTeam"><span><strong>San Lorenzo</strong></span></td><td class="name"><span>Racing Cordoba</span></td><td class=""><span class="score"><strong>1 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_6kZzbvyi", null, "", "", "2018", false)"><td><span class="date">11.07.18</span></td><td class="flag_td " title="Amistoso Interclubes (Mundo), "><span class="flag fl_8"></span>AMS</td><td class="name"><span><strong>Chapecoense</strong></span></td><td class="name highTeam"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>2 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_rNA1AKZ9", null, "", "", "2017-2018", false)"><td><span class="date">14.05.18</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name"><span><strong>River Plate</strong></span></td><td class="name highTeam"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>2 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_bVxRFYVH", null, "", "", "2018", false)"><td><span class="date">08.05.18</span></td><td class="flag_td " title="Copa Sul-Americana (América do Sul), "><span class="flag fl_3"></span>SUL</td><td class="name"><span>Atlético-MG</span></td><td class="name highTeam"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>0 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_je8eelU5", null, "", "", "2017-2018", false)"><td><span class="date">04.05.18</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name highTeam"><span><strong>San Lorenzo</strong></span></td><td class="name"><span>Belgrano</span></td><td class=""><span class="score"><strong>2 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_bw5ZkghQ", null, "", "", "2017-2018", false)"><td><span class="date">29.04.18</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name"><span>Patronato</span></td><td class="name highTeam"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>0 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_MHo7XPK1", null, "", "", "2017-2018", false)"><td><span class="date">21.04.18</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name highTeam"><span><strong>San Lorenzo</strong></span></td><td class="name"><span>Chacarita Juniors</span></td><td class=""><span class="score"><strong>1 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_Us9WsJxh", null, "", "", "2017-2018", false)"><td><span class="date">16.04.18</span></td><td class="flag_td " title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name"><span>Velez Sarsfield</span></td><td class="name highTeam"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>2 : 2</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_vmighvYg", null, "", "", "2018", false)"><td><span class="date">11.04.18</span></td><td class="flag_td " title="Copa Sul-Americana (América do Sul), "><span class="flag fl_3"></span>SUL</td><td class="name highTeam"><span><strong>San Lorenzo</strong></span></td><td class="name"><span>Atlético-MG</span></td><td class=""><span class="score"><strong>1 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_xlMpKFpo", null, "", "", "2017-2018", false)"><td class="lastR"><span class="date">08.04.18</span></td><td class="flag_td  lastR" title="Superliga (Argentina), "><span class="flag fl_22"></span>SUP</td><td class="name highTeam lastR"><span>San Lorenzo</span></td><td class="name lastR"><span><strong>Godoy Cruz</strong></span></td><td class="lastR"><span class="score"><strong>0 : 5</strong></span></td><td class="winLose lastR"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="hid"><td colspan="6" class="last lastR"><a class="show_more" onclick="glib_show_hidden("tab-h2h-overall","h2h_home",5); return false" href="#">Mostrar mais jogos <span class="arrow"></span></a></td></tr></tbody></table></div><div class="h2h-wrapper"><table class="head_to_head h2h_away"><colgroup><col width="1%"><col width="1%"><col width="48%"><col width="48%"><col width="1%"><col width="1%"></colgroup><thead><tr><td colspan="6" class="h-part last">Últimos jogos: MELGAR</td></tr></thead><tbody><tr class="odd highlight" onclick="detail_open("g_0_EuO2VY67", null, "", "", "2019", false)"><td><span class="date">20.04.19</span></td><td class="flag_td " title="Liga 1 (Peru), "><span class="flag fl_152"></span>L1</td><td class="name highTeam"><span><strong>Melgar</strong></span></td><td class="name"><span>Alianza Huanuco</span></td><td class=""><span class="score"><strong>2 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight" onclick="detail_open("g_0_fuHjYzNl", null, "", "", "2019", false)"><td><span class="date">14.04.19</span></td><td class="flag_td " title="Liga 1 (Peru), "><span class="flag fl_152"></span>L1</td><td class="name"><span>Union Comercio</span></td><td class="name highTeam"><span>Melgar</span></td><td class=""><span class="score"><strong>1 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="odd highlight" onclick="detail_open("g_0_vsl52EUH", null, "", "", "2019", false)"><td><span class="date">09.04.19</span></td><td class="flag_td " title="Copa Libertadores (América do Sul), "><span class="flag fl_3"></span>LIB</td><td class="name"><span><strong>San Lorenzo</strong></span></td><td class="name highTeam"><span>Melgar</span></td><td class=""><span class="score"><strong>2 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="even highlight" onclick="detail_open("g_0_d2YXdarh", null, "", "", "2019", false)"><td><span class="date">05.04.19</span></td><td class="flag_td " title="Liga 1 (Peru), "><span class="flag fl_152"></span>L1</td><td class="name"><span>Carlos Mannucci</span></td><td class="name highTeam"><span><strong>Melgar</strong></span></td><td class=""><span class="score"><strong>0 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="odd highlight" onclick="detail_open("g_0_0lbP796c", null, "", "", "2019", false)"><td><span class="date">02.04.19</span></td><td class="flag_td " title="Copa Libertadores (América do Sul), "><span class="flag fl_3"></span>LIB</td><td class="name highTeam"><span><strong>Melgar</strong></span></td><td class="name"><span>Junior</span></td><td class=""><span class="score"><strong>1 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_vR17tvbB", null, "", "", "2019", false)"><td><span class="date">30.03.19</span></td><td class="flag_td " title="Liga 1 (Peru), "><span class="flag fl_152"></span>L1</td><td class="name highTeam"><span><strong>Melgar</strong></span></td><td class="name"><span>U. San Martin</span></td><td class=""><span class="score"><strong>3 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_hGQxRbbO", null, "", "", "2019", false)"><td><span class="date">23.03.19</span></td><td class="flag_td " title="Liga 1 (Peru), "><span class="flag fl_152"></span>L1</td><td class="name"><span><strong>Molinos El Pirata</strong></span></td><td class="name highTeam"><span>Melgar</span></td><td class=""><span class="score"><strong>2 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_OtG066Gs", null, "", "", "2019", false)"><td><span class="date">20.03.19</span></td><td class="flag_td " title="Liga 1 (Peru), "><span class="flag fl_152"></span>L1</td><td class="name highTeam"><span>Melgar</span></td><td class="name"><span>Cajamarca</span></td><td class=""><span class="score"><strong>1 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_pj1aDuUO", null, "", "", "2019", false)"><td><span class="date">17.03.19</span></td><td class="flag_td " title="Liga 1 (Peru), "><span class="flag fl_152"></span>L1</td><td class="name highTeam"><span><strong>Melgar</strong></span></td><td class="name"><span>Universitario</span></td><td class=""><span class="score"><strong>2 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_0jk13fFB", null, "", "", "2019", false)"><td><span class="date">12.03.19</span></td><td class="flag_td " title="Copa Libertadores (América do Sul), "><span class="flag fl_3"></span>LIB</td><td class="name"><span><strong>Palmeiras</strong></span></td><td class="name highTeam"><span>Melgar</span></td><td class=""><span class="score"><strong>3 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_d8gsJq0m", null, "", "", "2019", false)"><td><span class="date">09.03.19</span></td><td class="flag_td " title="Liga 1 (Peru), "><span class="flag fl_152"></span>L1</td><td class="name"><span><strong>Garcilaso</strong></span></td><td class="name highTeam"><span>Melgar</span></td><td class=""><span class="score"><strong>1 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_IRad4z05", null, "", "", "2019", false)"><td><span class="date">05.03.19</span></td><td class="flag_td " title="Copa Libertadores (América do Sul), "><span class="flag fl_3"></span>LIB</td><td class="name highTeam"><span>Melgar</span></td><td class="name"><span>San Lorenzo</span></td><td class=""><span class="score"><strong>0 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_4lop22LH", null, "", "", "2019", false)"><td><span class="date">26.02.19</span></td><td class="flag_td " title="Copa Libertadores (América do Sul), "><span class="flag fl_3"></span>LIB</td><td class="name"><span><strong>Caracas</strong></span></td><td class="name highTeam"><span>Melgar</span></td><td class=""><span class="score"><strong>2 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_OEusDHXd", null, "", "", "2019", false)"><td><span class="date">23.02.19</span></td><td class="flag_td " title="Liga 1 (Peru), "><span class="flag fl_152"></span>L1</td><td class="name"><span>Ayacucho</span></td><td class="name highTeam"><span>Melgar</span></td><td class=""><span class="score"><strong>1 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_hWYY44ya", null, "", "", "2019", false)"><td><span class="date">19.02.19</span></td><td class="flag_td " title="Copa Libertadores (América do Sul), "><span class="flag fl_3"></span>LIB</td><td class="name highTeam"><span><strong>Melgar</strong></span></td><td class="name"><span>Caracas</span></td><td class=""><span class="score"><strong>2 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_dSHJeG2M", null, "", "", "2019", false)"><td><span class="date">17.02.19</span></td><td class="flag_td " title="Liga 1 (Peru), "><span class="flag fl_152"></span>L1</td><td class="name highTeam"><span>Melgar</span></td><td class="name"><span><strong>Dep. Municipal</strong></span></td><td class=""><span class="score"><strong>0 : 3</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_Q9nNjwge", null, "", "", "2019", false)"><td><span class="date">13.02.19</span></td><td class="flag_td " title="Copa Libertadores (América do Sul), "><span class="flag fl_3"></span>LIB</td><td class="name"><span>U. De Chile</span></td><td class="name highTeam"><span>Melgar</span></td><td class=""><span class="score"><strong>0 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_C2jnkQHj", null, "", "", "2019", false)"><td><span class="date">05.02.19</span></td><td class="flag_td " title="Copa Libertadores (América do Sul), "><span class="flag fl_3"></span>LIB</td><td class="name highTeam"><span><strong>Melgar</strong></span></td><td class="name"><span>U. De Chile</span></td><td class=""><span class="score"><strong>1 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_nNsbo7Ag", null, "", "", "2018", false)"><td><span class="date">06.12.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name highTeam"><span>Melgar</span></td><td class="name"><span>A. Lima</span></td><td class=""><span class="score"><strong>2 : 3</strong><br>(2 : 2)</span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate/Derrota" class="form-bg-last form-lo"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_4bhgnmem", null, "", "", "2018", false)"><td><span class="date">02.12.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name"><span>A. Lima</span></td><td class="name highTeam"><span>Melgar</span></td><td class=""><span class="score"><strong>3 : 3</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_h8KTUYyU", null, "", "", "2018", false)"><td><span class="date">25.11.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name"><span>U. San Martin</span></td><td class="name highTeam"><span>Melgar</span></td><td class=""><span class="score"><strong>1 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_AP2wKHNB", null, "", "", "2018", false)"><td><span class="date">11.11.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name highTeam"><span>Melgar</span></td><td class="name"><span><strong>AD Cantolao</strong></span></td><td class=""><span class="score"><strong>0 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_dnUUNaOn", null, "", "", "2018", false)"><td><span class="date">08.11.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name"><span><strong>Cajamarca</strong></span></td><td class="name highTeam"><span>Melgar</span></td><td class=""><span class="score"><strong>3 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_zZAS5R21", null, "", "", "2018", false)"><td><span class="date">05.11.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name highTeam"><span><strong>Melgar</strong></span></td><td class="name"><span>Union Comercio</span></td><td class=""><span class="score"><strong>1 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_6gNF8TIr", null, "", "", "2018", false)"><td><span class="date">01.11.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name highTeam"><span><strong>Melgar</strong></span></td><td class="name"><span>Comerciantes Unidos</span></td><td class=""><span class="score"><strong>2 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_l4XoglJe", null, "", "", "2018", false)"><td><span class="date">28.10.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name"><span>Garcilaso</span></td><td class="name highTeam"><span>Melgar</span></td><td class=""><span class="score"><strong>2 : 2</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_dpHWmgsG", null, "", "", "2018", false)"><td><span class="date">25.10.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name highTeam"><span><strong>Melgar</strong></span></td><td class="name"><span>Dep. Municipal</span></td><td class=""><span class="score"><strong>1 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_lKDOkFC3", null, "", "", "2018", false)"><td><span class="date">21.10.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name"><span>A. Lima</span></td><td class="name highTeam"><span><strong>Melgar</strong></span></td><td class=""><span class="score"><strong>0 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_W2gLlEAC", null, "", "", "2018", false)"><td><span class="date">03.10.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name highTeam"><span><strong>Melgar</strong></span></td><td class="name"><span>Sporting Cristal</span></td><td class=""><span class="score"><strong>2 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_hCfHkfe6", null, "", "", "2018", false)"><td><span class="date">29.09.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name"><span><strong>Sport Boys</strong></span></td><td class="name highTeam"><span>Melgar</span></td><td class=""><span class="score"><strong>1 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_rsyZxHB0", null, "", "", "2018", false)"><td><span class="date">26.09.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name highTeam"><span><strong>Melgar</strong></span></td><td class="name"><span>Sport Rosario</span></td><td class=""><span class="score"><strong>2 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_KrWgnLlE", null, "", "", "2018", false)"><td><span class="date">22.09.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name"><span>Binacional</span></td><td class="name highTeam"><span><strong>Melgar</strong></span></td><td class=""><span class="score"><strong>0 : 4</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_x61GY1KE", null, "", "", "2018", false)"><td><span class="date">15.09.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name highTeam"><span><strong>Melgar</strong></span></td><td class="name"><span>Huancayo</span></td><td class=""><span class="score"><strong>3 : 2</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_0KznJMKR", null, "", "", "2018", false)"><td><span class="date">11.09.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name"><span>Ayacucho</span></td><td class="name highTeam"><span>Melgar</span></td><td class=""><span class="score"><strong>0 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_0dhkMXUi", null, "", "", "2018", false)"><td><span class="date">01.09.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name highTeam"><span><strong>Melgar</strong></span></td><td class="name"><span>Universitario</span></td><td class=""><span class="score"><strong>2 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_4Ksu4jFN", null, "", "", "2018", false)"><td><span class="date">25.08.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name highTeam"><span><strong>Melgar</strong></span></td><td class="name"><span>U. San Martin</span></td><td class=""><span class="score"><strong>3 : 2</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_MyQlgZ05", null, "", "", "2018", false)"><td><span class="date">19.08.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name"><span>AD Cantolao</span></td><td class="name highTeam"><span>Melgar</span></td><td class=""><span class="score"><strong>1 : 1</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_hdYXdH1t", null, "", "", "2018", false)"><td><span class="date">16.08.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name highTeam"><span>Melgar</span></td><td class="name"><span>Cajamarca</span></td><td class=""><span class="score"><strong>3 : 3</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_fmRYRd26", null, "", "", "2018", false)"><td><span class="date">13.08.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name"><span>Union Comercio</span></td><td class="name highTeam"><span>Melgar</span></td><td class=""><span class="score"><strong>0 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_KUYLUbIm", null, "", "", "2018", false)"><td><span class="date">05.08.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name"><span>Comerciantes Unidos</span></td><td class="name highTeam"><span>Melgar</span></td><td class=""><span class="score"><strong>2 : 2</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_KAEdS5dk", null, "", "", "2018", false)"><td><span class="date">01.08.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name highTeam"><span><strong>Melgar</strong></span></td><td class="name"><span>Garcilaso</span></td><td class=""><span class="score"><strong>1 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_vF9ww2gA", null, "", "", "2018", false)"><td><span class="date">29.07.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name"><span><strong>Dep. Municipal</strong></span></td><td class="name highTeam"><span>Melgar</span></td><td class=""><span class="score"><strong>4 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_IaLUvOOc", null, "", "", "2018", false)"><td><span class="date">25.07.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name highTeam"><span><strong>Melgar</strong></span></td><td class="name"><span>A. Lima</span></td><td class=""><span class="score"><strong>2 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Vitória" class="form-bg-last form-w"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_61PQAqAH", null, "", "", "2018", false)"><td><span class="date">22.07.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name"><span><strong>Sporting Cristal</strong></span></td><td class="name highTeam"><span>Melgar</span></td><td class=""><span class="score"><strong>2 : 0</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="odd highlight hidden" onclick="detail_open("g_0_Qk8TBPfB", null, "", "", "2018", false)"><td><span class="date">10.06.18</span></td><td class="flag_td " title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name highTeam"><span>Melgar</span></td><td class="name"><span>Sport Boys</span></td><td class=""><span class="score"><strong>2 : 2</strong></span></td><td class="winLose"><span class="winLoseIcon"><a title="Empate" class="form-bg-last form-d"><span></span></a></span></td></tr><tr class="even highlight hidden" onclick="detail_open("g_0_I7goCYlf", null, "", "", "2018", false)"><td class="lastR"><span class="date">06.06.18</span></td><td class="flag_td  lastR" title="Primeira Divisão (Peru), "><span class="flag fl_152"></span>L1</td><td class="name lastR"><span><strong>Sport Rosario</strong></span></td><td class="name highTeam lastR"><span>Melgar</span></td><td class="lastR"><span class="score"><strong>2 : 1</strong></span></td><td class="winLose lastR"><span class="winLoseIcon"><a title="Derrota" class="form-bg-last form-l"><span></span></a></span></td></tr><tr class="hid"><td colspan="6" class="last lastR"><a class="show_more" onclick="glib_show_hidden("tab-h2h-overall","h2h_away",5); return false" href="#">Mostrar mais jogos <span class="arrow"></span></a></td></tr></tbody></table></div><div class="h2h-wrapper"><table class="head_to_head h2h_mutual"><colgroup><col width="1%"><col width="1%"><col width="48%"><col width="48%"><col width="2%"></colgroup><thead><tr><td colspan="6" class="h-part last">Confrontos diretos: SAN LORENZO - MELGAR</td></tr></thead><tbody><tr class="odd highlight" onclick="detail_open("g_0_vsl52EUH", null, "", "", "2019", false)"><td><span class="date">09.04.19</span></td><td class="flag_td " title="Copa Libertadores (América do Sul), "><span class="flag fl_3"></span>LIB</td><td class="name"><span><strong>San Lorenzo</strong></span></td><td class="name"><span>Melgar</span></td><td class="last"><span class="score"><strong>2 : 0</strong></span></td></tr><tr class="even highlight" onclick="detail_open("g_0_IRad4z05", null, "", "", "2019", false)"><td><span class="date">05.03.19</span></td><td class="flag_td " title="Copa Libertadores (América do Sul), "><span class="flag fl_3"></span>LIB</td><td class="name"><span>Melgar</span></td><td class="name"><span>San Lorenzo</span></td><td class="last"><span class="score"><strong>0 : 0</strong></span></td></tr></tbody></table></div>'
            dadosHtml = self.converterStringParaHtml(html)

            linhasTabelaPartidasMandante = dadosHtml.select(CSS_TABLE_PARTIDAS_MANDANTE + " tbody tr.highlight")
            linhasTabelaPartidasVisitante = dadosHtml.select(CSS_TABLE_PARTIDAS_VISITANTE + " tbody tr.highlight")
            linhasTabelaPartidasDiretas = dadosHtml.select(CSS_TABLE_PARTIDAS_DIRETOS + " tbody tr.highlight")

            ultimasPartidas["mandante"] = self.processarTabelaPartidasEquipe(linhasTabelaPartidasMandante)
            ultimasPartidas["visitante"] = self.processarTabelaPartidasEquipe(linhasTabelaPartidasVisitante)
            ultimasPartidas["confrontosDiretos"] = self.processarTabelaPartidasEquipe(linhasTabelaPartidasDiretas)

            return ultimasPartidas


        except Exception as e:
            print(e.args)
            return ultimasPartidas

    def processarTabelaPartidasEquipe(self, linhasTabela):
        try:
            listaPartidas = []

            for linha in linhasTabela:

                atributoOnClick = linha.attrs["onclick"]
                idPartida = atributoOnClick.split("'")[1].replace("g_0_", "")

                camposTabela = linha.select("td")

                urlPartida = "/jogo/{}/".format(idPartida)
                dataPartida = camposTabela[0].select("span")[0].text
                competicao = camposTabela[1].attrs["title"]
                equipeMandante = camposTabela[2].select("span")[0].text
                equipeVisitante = camposTabela[3].select("span")[0].text
                placar = camposTabela[4].select("span.score")[0].text

                resultado = ""
                if len(camposTabela) == 6:
                    resultado = camposTabela[5].select("span a")[0].attrs["title"]

                partidaEmCasa = len(camposTabela[2].attrs["class"]) > 1

                partida = {"idPartida": HashString().encode(urlPartida),
                           "urlPartida": urlPartida,
                           "data": datetime.strptime(dataPartida, "%d.%m.%y"),
                           "competicao": competicao,
                           "mandante": equipeMandante,
                           "visitante": equipeVisitante,
                           "casaFora": "CASA" if partidaEmCasa else "FORA",
                           "placar": placar.replace("(", "|").replace(")", ""),
                           "resultado": str.upper(resultado)
                           }

                listaPartidas.append(partida)

            return listaPartidas
        except Exception as e:
            print(e.args[0])
            return []

    def normalizarDescricaoStatus(self, status: str):

        if status == "":
            statusPartida = Partida.Status.AGENDADO.name

        elif status.find("1º tempo") != -1:
            statusPartida = Partida.Status.PRIMEIRO_TEMPO.name

        elif status.find("2º tempo") != -1:
            statusPartida = Partida.Status.SEGUNDO_TEMPO.name

        elif status == "Adiado":
            statusPartida = Partida.Status.ADIADO.name

        elif status == "Após Pênaltis":
            statusPartida = Partida.Status.FINALIZADO.name

        elif status == "Após Prorrogação":
            statusPartida = Partida.Status.FINALIZADO.name

        elif status == "Intervalo":
            statusPartida = Partida.Status.INTERVALO.name

        elif status == "Atribuído":
            statusPartida = Partida.Status.RESULTADO_NAO_DISPONIVEL.name

        elif status == "Abandonado":
            statusPartida = Partida.Status.ABANDONADO.name

        elif status == "Cancelado":
            statusPartida = Partida.Status.CANCELADO.name

        elif status == "SRF - Só resultado final.":
            statusPartida = Partida.Status.RESULTADO_NAO_DISPONIVEL.name

        elif status == "SRF ":
            statusPartida = Partida.Status.RESULTADO_NAO_DISPONIVEL.name

        elif status == "Encerrado":
            statusPartida = Partida.Status.FINALIZADO.name

        elif status == "Walkover":
            statusPartida = Partida.Status.W_O.name

        elif status.find("Walkover") != -1:
            statusPartida = Partida.Status.W_O.name
        else:
            print(" Status não mapeado:" + status)

            statusPartida = status

        return statusPartida

    def normalizarDescricaoEvento(self, desc: str):

        if desc == "y-card":
            desc = "CARTAO_AMARELO"

        elif desc == "soccer-ball":
            desc = "GOL"

        elif desc == "substitution-in":
            desc = "SUBSTITUICAO"

        elif desc == "yr-card":
            desc = "CARTAO_AMARELO_VERMELHO"

        elif desc == "soccer-ball-own":
            desc = "GOL_CONTRA"

        elif desc == "Penalty goal":
            desc = "GOL_PENALTY"

        elif desc == "r-card":
            desc = "CARTAO_VERMELHO"

        elif desc == "Penalty save":
            desc = "PENALTY_MARCADO"

        elif desc == "penalty-missed":
            desc = "PENALTY_PERDIDO"
        else:
            print(desc)

        return desc

    class TipoMercado(Enum):
        RESULTADO = "1x2-odds"""
        DNB = "home-away"
        UNDER_OVER = "acima-abaixo"
        PLACAR = "correct-score"
        BTTS = "ambos-marcam"
        ODD_EVEN = "odd-even"
        DUPLA_CHANCE = "double-chance"

    class Mercado(Enum):
        RESULTADO = 1
        UNDER = 2
        OVER = 3
        DNB = 4
        PLACAR = 5
        BTTS_YES = 6
        BTTS_NO = 7
        ODD = 8
        EVEN = 9
        CONTRA_MANDANTE = 10
        CONTRA_EMPATE = 11
        CONTRA_VISITANTE = 12
