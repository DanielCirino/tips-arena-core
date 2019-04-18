# -*- coding: utf-8 -*-

import time
from datetime import datetime
from enum import Enum
from threading import Thread

from core.ApostaCore import ApostaCore
from core.CompeticaoCore import CompeticaoCore
from core.EquipeCore import EquipeCore
from core.PartidaCore import PartidaCore
from core.ScrapWorkCore import ScrapWorkCore
from extratores.Motor import Motor
from models.Competicao import Competicao
from models.Partida import Partida
from models.ScrapWork import ScrapWork
from utils.HashString import HashString
from webscraping.ScraperCompeticao import ScraperCompeticao
from webscraping.ScraperEquipe import ScraperEquipe
from webscraping.ScraperPais import ScraperPais
from webscraping.ScraperPartida import ScraperPartida


class MotorAtualizacao(Motor):
    def __init__(self, acaoMotor, idThread, totalThreads, listaProcessamento):

        try:
            super(MotorAtualizacao, self).__init__(acaoMotor, idThread, totalThreads, listaProcessamento)
            Thread.__init__(self)

        except Exception as e:
            print(e.args[0])

    def salvarScrap(self, url: str, tipo: str, status: str, idPai=0):
        try:
            scrapWorkCore = ScrapWorkCore()
            objectId = HashString().encode(url["url"])
            scrap = scrapWorkCore.getScrapWorkById(objectId)

            scrap.url = url["url"]
            scrap.tipo = tipo
            scrap.idPai = idPai
            scrap.status = status
            scrap.prioridadeExtracao = url["seq"]
            scrap.dataCadastro = datetime.now()

            scrapWorkCore.salvarScrapWork(scrap)
            return True
        except Exception as e:
            return False

    def salvarListaScraping(self, listaUrls, status, tipo, idPai):
        try:
            contadorSucesso = 0
            contadorErro = 0

            for item in listaUrls:
                ret = self.salvarScrap(item, tipo, status, idPai)
                if ret:
                    contadorSucesso += 1
                else:
                    contadorErro += 1
            return {"totalSucesso": contadorSucesso, "totalErro": contadorErro}

        except Exception as e:
            print(e.args)
            return None

    def scrapListaPaises(self):
        try:
            horaInicio = datetime.now()
            paises = ScraperPais().getListaPaises()

            ret = self.salvarListaScraping(paises,
                                           ScrapWork.Status.SCRAPING_COMPETICOES.name,
                                           ScrapWork.Tipo.PAIS.name, "")

            horaFim = datetime.now()

            return {
                "horaInicio": horaInicio,
                "horaFim": horaFim,
                "acaoMotor": self.acao,
                "totalItens": len(paises),
                "resultado": ret,
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

            ret = self.salvarListaScraping(competicoes,
                                           ScrapWork.Status.SCRAPING_EDICOES_COMPETICAO.name,
                                           ScrapWork.Tipo.COMPETICAO.name, scrapPais._id)

            scrapPais.status = ScrapWork.Status.OK.name
            scrapWorkCore.salvarScrapWork(scrapPais)

            horaFim = datetime.now()

            return {
                "horaInicio": horaInicio,
                "horaFim": horaFim,
                "acaoMotor": self.acao,
                "totalItens": len(competicoes),
                "resultado": ret,
                "idThread": self.idThread,
                "totalThread": self.totalThreads
            }

        except Exception as e:
            print(e.args)
            scrapPais.status = ScrapWork.Status.ERRO.name
            scrapWorkCore.salvarScrapWork(scrapPais)

            return None

    def scrapListaPartidasEdicaoCompeticao(self, scrapEdicao):
        try:
            scrapWorkCore = ScrapWorkCore()
            horaInicio = datetime.now()
            partidas = ScraperPartida().getListaPartidasEdicaoCompeticao(scrapEdicao.url)
            totalPartidas = len(partidas["agendadas"]) + \
                            len(partidas["finalizadas"])

            scrapEdicao.target = totalPartidas
            scrapEdicao.status = ScrapWork.Status.PROCESSANDO.name
            scrapWorkCore.salvarScrapWork(scrapEdicao)

            ret = self.salvarListaScraping(partidas["agendadas"] + partidas["finalizadas"],
                                           ScrapWork.Status.AGUARDANDO_SCRAPING.name,
                                           ScrapWork.Tipo.PARTIDA.name, scrapEdicao._id)

            scrapEdicao.status = ScrapWork.Status.AGUARDANDO_SCRAPING.name
            scrapWorkCore.salvarScrapWork(scrapEdicao)

            horaFim = datetime.now()

            return {
                "horaInicio": horaInicio,
                "horaFim": horaFim,
                "acaoMotor": self.acao,
                "totalItens": totalPartidas,
                "resultado": ret,
                "idThread": self.idThread,
                "totalThread": self.totalThreads
            }

        except Exception as e:
            print(e.args)
            scrapEdicao.status = ScrapWork.Status.ERRO.name
            scrapWorkCore.salvarScrapWork(scrapEdicao)

            return None

    def salvarCompeticao(self, scrapCompeticao: ScrapWork):
        try:
            competicaoCore = CompeticaoCore()
            dadosCompeticao = ScraperCompeticao().getDadosCompeticao(scrapCompeticao.url)
            objectId = HashString().encode(scrapCompeticao.url)

            competicao = competicaoCore.getCompeticaoPorId(objectId)
            dadosCompeticao["_id"] = competicao._id
            dadosCompeticao["dataCadastro"] = competicao.dataCadastro

            competicao = Competicao(dadosCompeticao)

            ret = competicaoCore.salvarCompeticao(competicao)

            if ret:
                scrapCompeticao.status = ScrapWork.Status.OK.name
            else:
                scrapCompeticao.status = ScrapWork.Status.ERRO.name

            ScrapWorkCore().salvarScrapWork(scrapCompeticao)

            return ret
        except Exception as e:
            print(e.args)
            scrapCompeticao.status = ScrapWork.Status.ERRO.name
            ScrapWorkCore().salvarScrapWork(scrapCompeticao)
            return False

    def salvarEquipe(self, scrapEquipe: ScrapWork):
        try:
            equipeCore = EquipeCore()
            dadosEquipe = ScraperEquipe().getDadosEquipe(scrapEquipe.url)
            objectId = HashString().encode(scrapEquipe.url)

            equipe = equipeCore.getEquipePorId(objectId)
            dadosEquipe["_id"] = equipe._id
            dadosEquipe["dataCadastro"] = equipe.dataCadastro

            equipe = Competicao(dadosEquipe)

            ret = equipeCore.salvarEquipe(equipe)

            if ret:
                scrapEquipe.status = ScrapWork.Status.OK.name
            else:
                scrapEquipe.status = ScrapWork.Status.ERRO.name

            ScrapWorkCore().salvarScrapWork(scrapEquipe)

            return ret
        except Exception as e:
            print(e.args)
            scrapEquipe.status = ScrapWork.Status.ERRO.name
            ScrapWorkCore().salvarScrapWork(scrapEquipe)
            return False

    def atualizarPartida(self, partida: Partida):
        try:

            partidaCore = PartidaCore()
            dadosPartida = self.extrator.getDadosPartida(partida.url, extrairOdds=not partida.oddsDisponiveis)

            if dadosPartida is None:
                return False

            dadosPartida["_id"] = partida._id
            dadosPartida["idCompeticao"] = partida.idCompeticao

            dadosPartida["dataCadastro"] = partida.dataCadastro

            partidaAtualizada = Partida(dadosPartida)

            ret = partidaCore.salvarPartida(partidaAtualizada)

            if ret:
                analiseAlteracoes = partidaCore.analisarAlteracoesPartida(
                    partida, partidaAtualizada)

                workerAtualizacao = Thread(target=PartidaCore().processarAlteracoesPartida,
                                           args=(partidaAtualizada, analiseAlteracoes,))
                workerAtualizacao.start()

            return ret
        except Exception as e:
            print(e.args)
            return False

    def exibirAcoesMotor(self):
        for acao in self.Acao:
            print("{} ==> {}".format(acao.value, acao.name))

    def atualizarPartidas(self):
        try:
            if self.extrator is None:
                self.extrator = ScraperPartida()

            indexLista = 0
            for partida in self.listaProcessamento:
                executar = indexLista % self.totalThreads == self.idThread
                if executar:
                    ret = self.atualizarPartida(partida)

                    if ret:
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

    def atualizarPartidasAntigasNaoFinalizadas(self):
        try:
            if self.extrator is None:
                self.extrator = ScraperPartida()

            indexLista = 0
            for partida in self.listaProcessamento:
                executar = indexLista % self.totalThreads == self.idThread
                if executar:
                    ret = self.atualizarPartida(partida)

                    if ret:
                        self.totalSucesso += 1
                    else:
                        self.totalErros += 1

                indexLista += 1

            self.extrator.finalizarWebDriver()
            self.processamentoFinalizado = True
        except Exception as e:
            print(e.args[0])

    def atualizarApostas(self):
        try:
            if self.extrator is None:
                self.extrator = ScraperPartida()

            partidaCore = PartidaCore()
            apostaCore = ApostaCore()

            indexLista = 0
            for aposta in self.listaProcessamento:
                executar = indexLista % self.totalThreads == self.idThread
                if executar:
                    partida = partidaCore.getPartidaPorId(aposta.idPartida)

                    if partida.status == Partida.Status.FINALIZADO.name:
                        apostaCore.finalizarApostaPartida(aposta)
                    else:
                        self.atualizarPartida(partida)

                indexLista += 1
            self.extrator.finalizarWebDriver()
        except Exception as e:
            print(e.args[0])

    def run(self):
        if self.acaoMotor == self.Acao.ATUALIZAR_PARTIDAS:
            self.atualizarPartidas()

        elif self.acaoMotor == self.Acao.ATUALIZAR_PARTIDAS_ANTIGAS_NAO_FINALIZADAS:
            self.atualizarPartidasAntigasNaoFinalizadas()

        elif self.acaoMotor == self.Acao.ATUALIZAR_APOSTAS:
            self.atualizarApostas()
        else:
            print("ACAO INVALIDA")

            self.processamentoFinalizado = True
            self.horaFim = time.strftime("%Y-%m-%d %H:%M:%S")

    class Acao(Enum):
        ATUALIZAR_PARTIDAS = 1
        ATUALIZAR_PARTIDAS_ANTIGAS_NAO_FINALIZADAS = 2
        ATUALIZAR_APOSTAS = 3
