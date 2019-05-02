# -*- coding: utf-8 -*-

from threading import Thread
import time
from datetime import datetime, timedelta
from enum import Enum

from core.CompeticaoCore import CompeticaoCore
from core.EquipeCore import EquipeCore
from core.PartidaCore import PartidaCore
from core.ScrapWorkCore import ScrapWorkCore
from models.Competicao import Competicao
from models.Partida import Partida
from models.ScrapWork import ScrapWork
from utils.DateTimeHandler import DateTimeHandler
from utils.HashString import HashString
from webscraping.ScraperCompeticao import ScraperCompeticao
from webscraping.ScraperEquipe import ScraperEquipe
from webscraping.ScraperPais import ScraperPais
from webscraping.ScraperPartida import ScraperPartida
from extratores.Motor import Motor


class MotorExtracao(Motor):
    def __init__(self, acaoMotor=-1, idThread=-1, totalThreads=-1, listaProcessamento=[]):

        super(MotorExtracao, self).__init__(acaoMotor, idThread, totalThreads, listaProcessamento)
        Thread.__init__(self)

    def salvarScrap(self, url, prioridade: int, tipo: str, status: str, idPai=0):
        try:
            scrapWorkCore = ScrapWorkCore()
            objectId = HashString().encode(url)
            scrap = scrapWorkCore.getScrapWorkById(objectId)

            scrap.url = url
            scrap.tipo = tipo
            scrap.idPai = idPai
            scrap.status = status
            scrap.prioridadeExtracao = prioridade

            ret = scrapWorkCore.salvarScrapWork(scrap)
            if ret:
                return True
            else:
                return False
        except Exception as e:
            return False

    def salvarListaScraping(self, listaUrls, status, tipo, idPai):
        contadorSucesso = 0
        contadorErro = 0
        try:
            for item in listaUrls:
                resultado = self.salvarScrap(
                    item["url"], item["seq"], tipo, status, idPai)

                if resultado:
                    contadorSucesso += 1
                else:
                    contadorErro += 1

        except Exception as e:
            print(e.args)

        return {"totalRegistros": len(listaUrls), "totalSucesso": contadorSucesso, "totalErro": contadorErro}

    def scrapListaPaises(self):
        try:
            horaInicio = datetime.now()
            paises = ScraperPais().getListaPaises()

            resultado = self.salvarListaScraping(paises,
                                                 ScrapWork.Status.SCRAPING_COMPETICOES.name,
                                                 ScrapWork.Tipo.PAIS.name, "")

            horaFim = datetime.now()

            return {
                "horaInicio": horaInicio,
                "horaFim": horaFim,
                "acaoMotor": self.acaoMotor,
                "totalItens": len(paises),
                "resultado": resultado,
                "idThread": self.idThread,
                "totalThread": self.totalThreads
            }
        except Exception as e:
            print(e.args)
            return None

    def scrapListaCompeticoesPais(self, scrapPais: ScrapWork):
        try:
            scrapWorkCore = ScrapWorkCore()

            horaInicio = datetime.now()
            competicoes = ScraperCompeticao().getListaCompeicoesPais(scrapPais.url)

            scrapPais.target = len(competicoes)
            scrapPais.status = ScrapWork.Status.PROCESSANDO.name
            scrapWorkCore.salvarScrapWork(scrapPais)

            resultado = self.salvarListaScraping(competicoes,
                                                 ScrapWork.Status.SCRAPING_EDICOES_COMPETICAO.name,
                                                 ScrapWork.Tipo.COMPETICAO.name, scrapPais._id)

            scrapPais.status = ScrapWork.Status.OK.name
            scrapWorkCore.salvarScrapWork(scrapPais)

            horaFim = datetime.now()

            return {
                "horaInicio": horaInicio,
                "horaFim": horaFim,
                "acaoMotor": self.acaoMotor,
                "totalItens": len(competicoes),
                "resultado": resultado,
                "idThread": self.idThread,
                "totalThread": self.totalThreads
            }

        except Exception as e:
            print(e.args)
            scrapPais.status = ScrapWork.Status.ERRO.name
            scrapWorkCore.salvarScrapWork(scrapPais)

            return None

    def scrapListaEquipesCompeticao(self, scrapCompeticao: ScrapWork):
        scrapWorkCore = ScrapWorkCore()
        try:

            horaInicio = datetime.now()
            equipes = ScraperEquipe().getListaEquipesEdicaoCompeticao(scrapCompeticao.url)

            scrapCompeticao.target = len(equipes)
            scrapCompeticao.status = ScrapWork.Status.PROCESSANDO.name
            scrapWorkCore.salvarScrapWork(scrapCompeticao)

            ret = self.salvarListaScraping(equipes,
                                           ScrapWork.Status.AGUARDANDO_SCRAPING.name,
                                           ScrapWork.Tipo.EQUIPE.name, scrapCompeticao._id)

            scrapCompeticao.status = ScrapWork.Status.SCRAPING_PARTIDAS.name
            scrapWorkCore.salvarScrapWork(scrapCompeticao)

            horaFim = datetime.now()

            return {
                "horaInicio": horaInicio,
                "horaFim": horaFim,
                "acaoMotor": self.acaoMotor,
                "totalItens": len(equipes),
                "resultado": ret,
                "idThread": self.idThread,
                "totalThread": self.totalThreads
            }

        except Exception as e:
            print(e.args)
            scrapCompeticao.status = ScrapWork.Status.ERRO.name
            scrapWorkCore.salvarScrapWork(scrapCompeticao)

            return None

    def scrapListaPartidasCompeticao(self, scrapCompeticao: ScrapWork):
        scrapWorkCore = ScrapWorkCore()
        try:
            horaInicio = datetime.now()
            partidas = self.extrator.getListaPartidasEdicaoCompeticao(
                scrapCompeticao.url)
            totalPartidas = len(partidas["agendadas"]) + \
                            len(partidas["finalizadas"])

            scrapCompeticao.target = totalPartidas
            scrapCompeticao.status = ScrapWork.Status.PROCESSANDO.name
            scrapWorkCore.salvarScrapWork(scrapCompeticao)

            ret = self.salvarListaScraping(partidas["agendadas"] + partidas["finalizadas"],
                                           ScrapWork.Status.AGUARDANDO_SCRAPING.name,
                                           ScrapWork.Tipo.PARTIDA.name, scrapCompeticao._id)

            scrapCompeticao.status = ScrapWork.Status.AGUARDANDO_SCRAPING.name
            scrapWorkCore.salvarScrapWork(scrapCompeticao)

            horaFim = datetime.now()

            return {
                "horaInicio": horaInicio,
                "horaFim": horaFim,
                "acaoMotor": self.acaoMotor,
                "totalItens": totalPartidas,
                "resultado": ret,
                "idThread": self.idThread,
                "totalThread": self.totalThreads
            }

        except Exception as e:
            print(e.args)
            scrapCompeticao.status = ScrapWork.Status.ERRO.name
            scrapWorkCore.salvarScrapWork(scrapCompeticao)

            return None

    def salvarCompeticao(self, scrapCompeticao: ScrapWork):
        scrapWorkCore = ScrapWorkCore()
        try:
            competicaoCore = CompeticaoCore()
            dadosCompeticao = ScraperCompeticao().getDadosCompeticao(scrapCompeticao.url)
            objectId = HashString().encode(scrapCompeticao.url)

            competicao = competicaoCore.getCompeticaoPorId(objectId)
            dadosCompeticao["_id"] = competicao._id
            dadosCompeticao["dataCadastro"] = competicao.dataCadastro

            competicao = Competicao(dadosCompeticao)

            resultado = competicaoCore.salvarCompeticao(competicao)

            if resultado:
                scrapCompeticao.status = ScrapWork.Status.OK.name
            else:
                scrapCompeticao.status = ScrapWork.Status.ERRO.name

            scrapWorkCore.salvarScrapWork(scrapCompeticao)

            return resultado
        except Exception as e:
            print(e.args)
            scrapCompeticao.status = ScrapWork.Status.ERRO.name
            scrapWorkCore.salvarScrapWork(scrapCompeticao)
            return False

    def salvarEquipe(self, scrapEquipe: ScrapWork):
        scrapWorkCore = ScrapWorkCore()
        try:
            equipeCore = EquipeCore()
            dadosEquipe = ScraperEquipe().getDadosEquipe(scrapEquipe.url)
            objectId = HashString().encode(scrapEquipe.url)

            equipe = equipeCore.getEquipePorId(objectId)
            dadosEquipe["_id"] = equipe._id
            dadosEquipe["dataCadastro"] = equipe.dataCadastro

            equipe = Competicao(dadosEquipe)

            resultado = equipeCore.salvarEquipe(equipe)

            if resultado:
                scrapEquipe.status = ScrapWork.Status.OK.name
            else:
                scrapEquipe.status = ScrapWork.Status.ERRO.name

            scrapWorkCore.salvarScrapWork(scrapEquipe)

            return resultado
        except Exception as e:
            print(e.args)
            scrapEquipe.status = ScrapWork.Status.ERRO.name
            scrapWorkCore.salvarScrapWork(scrapEquipe)
            return False

    def salvarPartida(self, scrapPartida: ScrapWork):
        scrapWorkCore = ScrapWorkCore()
        try:
            partidaCore = PartidaCore()
            dadosPartida = self.extrator.getDadosPartida(scrapPartida.url)
            objectId = HashString().encode(scrapPartida.url)

            partida = partidaCore.getPartidaPorId(objectId)
            dadosPartida["_id"] = partida._id
            dadosPartida["edicaoCompeticao"]["url"] = scrapPartida.url

            dadosPartida["dataCadastro"] = partida.dataCadastro

            partida = Partida(dadosPartida)
            partida.idEdicaoCompeticao = scrapPartida.idPai

            resultado = partidaCore.salvarPartida(partida)

            if resultado:
                scrapPartida.status = ScrapWork.Status.OK.name
            else:
                scrapPartida.status = ScrapWork.Status.ERRO.name

            scrapWorkCore.salvarScrapWork(scrapPartida)

            return resultado
        except Exception as e:
            print(e.args)
            scrapPartida.status = ScrapWork.Status.ERRO.name
            scrapWorkCore.salvarScrapWork(scrapPartida)
            return False

    def salvarPartidaDoDia(self, urlPartida):
        try:
            partidaCore = PartidaCore()
            hashString = HashString()

            partidaCadastrada = partidaCore.getPartidaPorId(hashString.encode(urlPartida))

            if partidaCadastrada.url == urlPartida: return True

            motorExtracao = MotorExtracao()

            dadosPartida = self.extrator.getDadosPartida(urlPartida)

            urlPais = dadosPartida["competicao"]["pais"]["url"]
            idPais = hashString.encode(urlPais)

            urlCompeticao = dadosPartida["competicao"]["url"]
            idCompeticao = hashString.encode(urlCompeticao)

            dadosPartida["idCompeticao"] = idCompeticao
            motorExtracao.salvarScrap(urlPais, 1, ScrapWork.Tipo.PAIS.name,
                                      ScrapWork.Status.SCRAPING_COMPETICOES.name)

            motorExtracao.salvarScrap(urlCompeticao, 1, ScrapWork.Tipo.COMPETICAO.name,
                                      ScrapWork.Status.SCRAPING_EDICOES_COMPETICAO.name, idPais)

            motorExtracao.salvarScrap(dadosPartida["equipeMandante"]["url"], 1, ScrapWork.Tipo.EQUIPE.name,
                                      ScrapWork.Status.AGUARDANDO_SCRAPING.name, idCompeticao)

            motorExtracao.salvarScrap(dadosPartida["equipeVisitante"]["url"], 1, ScrapWork.Tipo.EQUIPE.name,
                                      ScrapWork.Status.AGUARDANDO_SCRAPING.name, idCompeticao)

            motorExtracao.salvarScrap(dadosPartida["url"], 1, ScrapWork.Tipo.PARTIDA.name,
                                      ScrapWork.Status.OK.name, idCompeticao)

            novaPartida = Partida(dadosPartida)

            resultado = partidaCore.salvarPartida(novaPartida)

            return resultado.acknowledged

        except Exception as e:
            print(e.args)
            return False

    def extrairPartidasDia(self):
        try:
            if self.extrator is None:
                self.extrator = ScraperPartida()

            indexLista = 0

            for urlPartida in self.listaProcessamento:
                executar = indexLista % self.totalThreads == self.idThread
                if executar:
                    resultado = self.salvarPartidaDoDia(urlPartida)

                    if resultado:
                        self.totalSucesso += 1
                    else:
                        self.totalErros += 1

                indexLista += 1

            self.extrator.finalizarWebDriver()
            self.processamentoFinalizado = True

        except Exception as e:
            print(e.args[0])
            if self.extrator is not None:
                self.extrator.finalizarWebDriver()

    def processarScrapingPaises(self):
        try:
            indexLista = 0

            for urlPais in self.listaProcessamento:
                executar = indexLista % self.totalThreads == self.idThread
                if executar:
                    resultado = self.salvarScrap(
                        urlPais,
                        ScrapWork.Tipo.PAIS.name,
                        ScrapWork.Status.SCRAPING_COMPETICOES.name)

                    if resultado:
                        self.totalSucesso += 1
                    else:
                        self.totalErros += 1

                indexLista += 1
        except Exception as e:
            print(e.args[0])

        self.processamentoFinalizado = True

    def processarScrapingCompeticoesPais(self):
        try:
            indexLista = 0

            for scrapPais in self.listaProcessamento:
                executar = indexLista % self.totalThreads == self.idThread
                if executar:
                    resultado = self.scrapListaCompeticoesPais(scrapPais)

                    if resultado is not None:
                        self.totalSucesso += resultado["resultado"]["totalSucesso"]
                    else:
                        self.totalErros += resultado["resultado"]["totalErro"]

                indexLista += 1
        except Exception as e:
            print(e.args[0])

        self.processamentoFinalizado = True

    def processarScrapingEquipesCompeticao(self):
        try:
            indexLista = 0

            for scrapCompeticao in self.listaProcessamento:
                executar = indexLista % self.totalThreads == self.idThread
                if executar:
                    resultado = self.scrapListaEquipesCompeticao(scrapCompeticao)

                    if resultado is not None:
                        self.totalSucesso += resultado["resultado"]["totalSucesso"]
                    else:
                        self.totalErros += resultado["resultado"]["totalErro"]

                indexLista += 1
        except Exception as e:
            print(e.args[0])

        self.processamentoFinalizado = True

    def processarScrapingPartidasCompeticao(self):
        try:
            if self.extrator is None:
                self.extrator = ScraperPartida()

            indexLista = 0

            for scrapCompeticao in self.listaProcessamento:
                executar = indexLista % self.totalThreads == self.idThread
                if executar:
                    resultado = self.scrapListaPartidasCompeticao(scrapCompeticao)

                    if resultado is not None:
                        self.totalSucesso += resultado["resultado"]["totalSucesso"]
                    else:
                        self.totalErros += resultado["resultado"]["totalErro"]

                indexLista += 1

        except Exception as e:
            print(e.args[0])

        self.extrator.finalizarWebDriver()
        self.processamentoFinalizado = True

    def processarSalvarCompeticoes(self):
        try:
            indexLista = 0

            for scrapCompeticao in self.listaProcessamento:
                executar = indexLista % self.totalThreads == self.idThread
                if executar:
                    resultado = self.salvarCompeticao(scrapCompeticao)

                    if resultado:
                        self.totalSucesso += 1
                    else:
                        self.totalErros += 1

                indexLista += 1

        except Exception as e:
            print(e.args[0])

        self.processamentoFinalizado = True

    def processarSalvarEquipes(self):
        try:
            indexLista = 0

            for scrapEquipe in self.listaProcessamento:
                executar = indexLista % self.totalThreads == self.idThread
                if executar:
                    resultado = self.salvarEquipe(scrapEquipe)

                    if resultado:
                        self.totalSucesso += 1
                    else:
                        self.totalErros += 1

                indexLista += 1

        except Exception as e:
            print(e.args[0])

        self.processamentoFinalizado = True

    def processarSalvarPartidas(self):
        try:
            if self.extrator is None:
                self.extrator = ScraperPartida()

            indexLista = 0

            for scrapPartida in self.listaProcessamento:
                executar = indexLista % self.totalThreads == self.idThread
                if executar:
                    resultado = self.salvarPartida(scrapPartida)

                    if resultado:
                        self.totalSucesso += 1
                    else:
                        self.totalErros += 1

                indexLista += 1


        except Exception as e:
            print(e.args[0])

        self.extrator.finalizarWebDriver()
        self.processamentoFinalizado = True

    def exibirAcoesMotor(self):
        for acao in self.Acao:
            print("{} ==> {}".format(acao.value, acao.name))

    def run(self):
        if self.acaoMotor == self.Acao.EXTRAIR_PARTIDAS_DO_DIA:
            self.extrairPartidasDia()

        elif self.acaoMotor == self.Acao.SCRAPING_PAISES:
            self.processarScrapingPaises()

        elif self.acaoMotor == self.Acao.SCRAPING_COMPETICOES:
            self.processarScrapingCompeticoesPais()

        elif self.acaoMotor == self.Acao.SCRAPING_EQUIPES:
            self.processarScrapingEquipesCompeticao()

        elif self.acaoMotor == self.Acao.SCRAPING_PARTIDAS:
            self.processarScrapingPartidasCompeticao()

        elif self.acaoMotor == self.Acao.SALVAR_COMPETICOES:
            self.processarSalvarCompeticoes()

        elif self.acaoMotor == self.Acao.SALVAR_EQUIPE:
            self.processarSalvarEquipes()

        elif self.acaoMotor == self.Acao.SALVAR_PARTIDAS:
            self.processarSalvarPartidas()

        else:
            print("ACAO INVALIDA")

        self.horaFim = time.strftime("%Y-%m-%d %H:%M:%S")

        if self.extrator is not None:
            self.extrator.finalizarWebDriver()

    class Acao(Enum):
        EXTRAIR_PARTIDAS_DO_DIA = 1
        SCRAPING_PAISES = 2
        SCRAPING_COMPETICOES = 3
        SCRAPING_EQUIPES = 4
        SCRAPING_PARTIDAS = 5
        SALVAR_COMPETICOES = 6
        SALVAR_EQUIPE = 7
        SALVAR_PARTIDAS = 8
