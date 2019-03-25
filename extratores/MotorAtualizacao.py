
# -*- coding: utf-8 -*-

import threading
import time
from datetime import datetime, timedelta
from enum import Enum

from core.CompeticaoCore import CompeticaoCore
from core.EquipeCore import EquipeCore
from core.PartidaCore import PartidaCore
from core.ScrapWorkCore import ScrapWorkCore
from extratores.MotorExtracao import MotorExtracao
from models.Competicao import Competicao
from models.Partida import Partida
from models.ScrapWork import ScrapWork
from utils.HashString import HashString
from webscraping.ScraperCompeticao import ScraperCompeticao
from webscraping.ScraperEquipe import ScraperEquipe
from webscraping.ScraperPais import ScraperPais
from webscraping.ScraperPartida import ScraperPartida


class MotorAtualizacao(threading.Thread):
    def __init__(self, acao, idThread, totalThreads, listaProcessamento):

        try:
            self.acao = acao
            self.idThread = idThread
            self.totalThreads = totalThreads

            self.listaProcessamento = listaProcessamento
            self.totalRegistros = len(listaProcessamento)

            self.rangeInicio = idThread * \
                round(len(self.listaProcessamento) / self.totalThreads)
            self.rangeFim = (
                (idThread + 1) * round(len(self.listaProcessamento) / self.totalThreads)) - 1

            if self.rangeFim + 1 > len(self.listaProcessamento):
                self.rangeFim = len(self.listaProcessamento) - 1

            if idThread + 1 == totalThreads:
                if self.rangeFim + 1 < len(self.listaProcessamento):
                    self.rangeFim = len(self.listaProcessamento) - 1

            # print("[{}a{}][{}]".format(self.range_inicio, self.range_fim, self.id_thread))

            self.totalSucesso = 0
            self.totalErros = 0
            self.horaInicio = time.strftime("%Y-%m-%d %H:%M:%S")
            self.horaFim = None
            self.processamentoFinalizado = False

            self.extrator = None

            threading.Thread.__init__(self)
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
            dadosPartida = self.extrator.getDadosPartida(partida.url)

            dadosPartida["_id"] = partida._id
            dadosPartida["idCompeticao"] = partida.idCompeticao

            dadosPartida["dataCadastro"] = partida.dataCadastro

            partidaAtualizada = Partida(dadosPartida)

            ret = partidaCore.salvarPartida(partidaAtualizada)

            if ret:
                partidaCore.analisarAlteracoesPartida(
                    partida, partidaAtualizada)

            return ret
        except Exception as e:
            print(e.args)
            return False

    def validarPartidaDoDia(self, urlPartida, partidasCadastradas):
        try:

            partidaCore = PartidaCore()
            partidaJaCadastrada = False

            for partida in partidasCadastradas:
                if partida.url == urlPartida:
                    partidaJaCadastrada = True
                    break

            if partidaJaCadastrada:
                return True

            motorExtracao = MotorExtracao()
            hashString = HashString()

            dadosPartida = self.extrator.getDadosPartida(urlPartida)

            urlPais = dadosPartida["competicao"]["pais"]["url"]
            idPais = hashString.encode(urlPais)

            urlCompeticao = dadosPartida["competicao"]["url"]
            # idCompeticao = hashString.encode(urlCompeticao)
            #
            # edicaoMaisRecenteCompeticao = ScraperEdicaoCompeticao().get_edicao_mais_recente_competicao(
            #     urlCompeticao)
            # edicaoMaisRecenteCompeticao["competicao"] = dadosPartida["edicaoCompeticao"]["competicao"]
            #
            # urlEdicaoCompeticao = edicaoMaisRecenteCompeticao["url"]
            idCompeticao = hashString.encode(urlCompeticao)

            dadosPartida["idCompeticao"] = idCompeticao
            # dadosPartida["edicaoCompeticao"] = edicaoMaisRecenteCompeticao

            motorExtracao.salvarScrap(urlPais, 1, ScrapWork.Tipo.PAIS.name,
                                      ScrapWork.Status.SCRAPING_COMPETICOES.name)

            motorExtracao.salvarScrap(urlCompeticao, 1, ScrapWork.Tipo.COMPETICAO.name,
                                      ScrapWork.Status.SCRAPING_EDICOES_COMPETICAO.name, idPais)

            # motorExtracao.salvarScrap(urlEdicaoCompeticao, 1, ScrapWork.Tipo.EDICAO_COMPETICAO.name,
            #                           ScrapWork.Status.SCRAPING_EQUIPES.name, idCompeticao)

            motorExtracao.salvarScrap(dadosPartida["equipeMandante"]["url"], 1, ScrapWork.Tipo.EQUIPE.name,
                                      ScrapWork.Status.AGUARDANDO_SCRAPING.name, idCompeticao)

            motorExtracao.salvarScrap(dadosPartida["equipeVisitante"]["url"], 1, ScrapWork.Tipo.EQUIPE.name,
                                      ScrapWork.Status.AGUARDANDO_SCRAPING.name, idCompeticao)

            motorExtracao.salvarScrap(dadosPartida["url"], 1, ScrapWork.Tipo.PARTIDA.name,
                                      ScrapWork.Status.OK.name, idCompeticao)

            novaPartida = Partida(dadosPartida)
            ret = partidaCore.salvarPartida(novaPartida)

            if ret:
                return ret
            else:
                return False

        except Exception as e:
            print(e.args)
            return False

    def exibirAcoesMotor(self):
        for acao in self.Acao:
            print("{} ==> {}".format(acao.value, acao.name))

    def run(self):
        # atualizar partidas do dia
        # atualizar partidas antigas não finalizadas
        # validar partidas do dia
        # atualizar ediçoes competicao

        if self.acao == self.Acao.ATUALIZAR_PARTIDAS:
            self.extrator = ScraperPartida()

            for i in range(self.rangeInicio, self.rangeFim + 1):
                partida = self.listaProcessamento[i]
                ret = self.atualizarPartida(partida)

                if ret:
                    self.totalSucesso += 1
                else:
                    self.totalErros += 1

            self.extrator.finalizarWebDriver()

        elif self.acao == self.Acao.ATUALIZAR_PARTIDAS_ANTIGAS_NAO_FINALIZADAS:
            self.extrator = ScraperPartida()

            for i in range(self.rangeInicio, self.rangeFim + 1):
                partida = self.listaProcessamento[i]
                ret = self.atualizarPartida(partida)

                if ret:
                    self.totalSucesso += 1
                else:
                    self.totalErros += 1

            self.extrator.finalizarWebDriver()

        elif self.acao == self.Acao.VALIDAR_PARTIDAS_DO_DIA:
            self.extrator = ScraperPartida()
            partidaCore = PartidaCore()

            data_inicio = datetime.strftime(
                datetime.now() - timedelta(days=3), "%Y-%m-%d") + " 00:00:00"
            data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d %H:%M:%S")

            data_fim = datetime.strftime(
                datetime.now() + timedelta(days=3), "%Y-%m-%d") + " 23:59:59"
            data_fim = datetime.strptime(data_fim, "%Y-%m-%d %H:%M:%S")

            filtrosPartida = partidaCore.getOpcoesFiltro()

            filtrosPartida["dataHoraInicio"] = data_inicio
            filtrosPartida["dataHoraFim"] = data_fim

            partidasCadastradas = partidaCore.listPartidas(filtrosPartida)

            contadorExecucao = 0
            for urlPartida in self.listaProcessamento:
                executar = contadorExecucao % self.totalThreads == self.idThread
                if executar:
                    # urlPartida = self.listaProcessamento[contadorExecucao]
                    ret = self.validarPartidaDoDia(urlPartida, partidasCadastradas)
                    if ret:
                        try:
                            partidasCadastradas.remove(urlPartida)
                        except:
                            pass
                        self.totalSucesso += 1
                    else:
                        self.totalErros += 1



            # for i in range(self.rangeInicio, self.rangeFim + 1):
            #     urlPartida = self.listaProcessamento[i]
            #
            #     ret = self.validarPartidaDoDia(urlPartida, partidasCadastradas)
            #     if ret:
            #         try:
            #             partidasCadastradas.remove(urlPartida)
            #         except:
            #             pass
            #         self.totalSucesso += 1
            #     else:
            #         self.totalErros += 1

            self.extrator.finalizarWebDriver()
            self.processamentoFinalizado = True

        else:
            print("ACAO INVALIDA")

            self.processamentoFinalizado = True
            self.horaFim = time.strftime("%Y-%m-%d %H:%M:%S")

    class Acao(Enum):
        ATUALIZAR_PARTIDAS = 1
        ATUALIZAR_PARTIDAS_ANTIGAS_NAO_FINALIZADAS = 2
        VALIDAR_PARTIDAS_DO_DIA = 3
        ATUALIZAR_EDICOES_COMPETICAO = 4
