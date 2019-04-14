# -*- coding: utf-8 -*-
import sys
import traceback
import time
from enum import Enum
from datetime import datetime, timedelta

from core.PartidaCore import PartidaCore
from core.ProcessamentoBatchCore import ProcessamentoBatchCore
from extratores.MotorExtracao import MotorExtracao
from extratores.MotorAtualizacao import MotorAtualizacao
from models.ProcessamentoBatch import ProcessamentoBatch

from webscraping.ScraperPais import ScraperPais

from core.ScrapWorkCore import ScrapWorkCore
from webscraping.ScraperPartida import ScraperPartida

from models.ScrapWork import ScrapWork
from models.Partida import Partida


class MotorFactory:
    def __init__(self, codigoMotor, codigoAcaoMotor, qtdThreads):
        try:
            self.dataHoraInicio = datetime.now()

            self.codigoMotor = codigoMotor
            self.codigoAcaoMotor = codigoAcaoMotor
            self.qtdThreads = qtdThreads
            self.itensProcessamento = []
            self.totalItensProcessamento = 0

            self.totalItensSucesso = 0
            self.totaltensErro = 0
            self.processamentoFinalizado = False

            self.tipoMotor = self.Motor(codigoMotor)
            self.acaoMotor = None
            self.idProcessamentoBatch = ""

            if self.codigoMotor != 0:
                if self.codigoAcaoMotor == 0:
                    self.exibirAcoesMotor()
                else:
                    self.iniciarProcessamento()
            else:
                self.exibirOpcoesMotor()

        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__))
            print("Erro processamento.[Motor:{}][Acao:{}]".format(self.tipoMotor, self.codigoAcaoMotor))

    def iniciarProcessamento(self):
        try:
            itensProcessamento = []
            if self.tipoMotor == self.tipoMotor.MOTOR_EXTRACAO:
                motor = MotorExtracao
                itensProcessamento = self.getItensProcessamentoMotorExtracao()
            elif self.tipoMotor == self.tipoMotor.MOTOR_ATUALIZACAO:
                motor = MotorAtualizacao
                itensProcessamento = self.getItensProcessamentoMotorAtualizacao()
            else:
                print("Motor inválido...")
                return

            totalItensProcessamento = len(itensProcessamento)

            print("Lista de processamento possui {}".format(totalItensProcessamento))

            processamento = ProcessamentoBatch()
            processamento.tipo = self.acaoMotor.name
            processamento.status = ProcessamentoBatch.Status.NAO_INICIADO.name
            processamento.totalRegistros = totalItensProcessamento

            processamentoBatch = ProcessamentoBatchCore().salvarProcessamentoBatch(processamento)

            if processamentoBatch is not None:
                self.idProcessamentoBatch = processamentoBatch.inserted_id
                self.listaThreads = []

                for idThread in range(0, self.qtdThreads):
                    thread = motor(self.acaoMotor, idThread, self.qtdThreads,
                                   itensProcessamento)
                    thread.start()
                    self.listaThreads.insert(idThread, thread)

                self.verificarProcessamento()
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__))

    def salvarProcessamentoBatch(self, quantidade_sucesso, quantidade_erro, status, data_hora_fim=None):
        try:
            processamentoCore = ProcessamentoBatchCore()
            processamento_batch = processamentoCore.getProcessamentoBatchById(self.idProcessamentoBatch)

            if processamento_batch._id != "":
                processamento_batch.totalSucesso = quantidade_sucesso
                processamento_batch.totalErro = quantidade_erro
                processamento_batch.status = status
                processamento_batch.dataHoraFim = data_hora_fim

            return processamentoCore.salvarProcessamentoBatch(processamento_batch)
        except Exception as e:
            print(e.args[0])
            return None

    def verificarProcessamento(self):
        try:
            while not self.verificarFimDoProcessamento():
                time.sleep(300)
                quantidadesProcessadas = self.getQuantidadeProcessada()
                self.salvarProcessamentoBatch(quantidadesProcessadas[0], quantidadesProcessadas[1],
                                              ProcessamentoBatch.Status.EM_PROCESSAMENTO.name)

            quantidadesProcessadas = self.getQuantidadeProcessada()
            self.salvarProcessamentoBatch(quantidadesProcessadas[0], quantidadesProcessadas[1],
                                          ProcessamentoBatch.Status.FINALIZADO.name, datetime.utcnow())
        except Exception as e:
            print(e.args)

    def verificarFimDoProcessamento(self) -> bool:
        finalizado = True
        for thread in self.listaThreads:
            finalizado = finalizado and not thread.is_alive()

        return finalizado

    def getQuantidadeProcessada(self):
        quantidadeSucesso = 0
        quantidadeErro = 0

        for thread in self.listaThreads:
            quantidadeSucesso += thread.totalSucesso
            quantidadeErro += thread.totalErros

        return [quantidadeSucesso, quantidadeErro]

    def getItensProcessamentoMotorExtracao(self):
        self.acaoMotor = MotorExtracao.Acao(self.codigoAcaoMotor)
        scrapWorkCore = ScrapWorkCore()

        if self.acaoMotor == MotorExtracao.Acao.EXTRAIR_PARTIDAS_DO_DIA:
            try:
                extrator = ScraperPartida()
                itensProcessamento = extrator.getListaPartidasDia()
                extrator.finalizarWebDriver()
                return itensProcessamento
            except Exception as e:
                print(e.args[0])
                return []

        elif self.acaoMotor == MotorExtracao.Acao.SCRAPING_PAISES:
            self.itensProcessamento = ScraperPais().getListaPaises()

        elif self.acaoMotor == MotorExtracao.Acao.SCRAPING_COMPETICOES:
            self.itensProcessamento = scrapWorkCore.getScrapWorksPorTipo(ScrapWork.Tipo.PAIS.name,
                                                                         ScrapWork.Status.SCRAPING_COMPETICOES.name)

        elif self.acaoMotor == MotorExtracao.Acao.SCRAPING_EDICOES_COMPETICAO:
            self.itensProcessamento = scrapWorkCore.getScrapWorksPorTipo(ScrapWork.Tipo.COMPETICAO.name,
                                                                         ScrapWork.Status.SCRAPING_EDICOES_COMPETICAO.name)
        elif self.acaoMotor == MotorExtracao.Acao.SCRAPING_EQUIPES:
            self.itensProcessamento = scrapWorkCore.getScrapWorksPorTipo(ScrapWork.Tipo.EDICAO_COMPETICAO.name,
                                                                         ScrapWork.Status.SCRAPING_EQUIPES.name)
        elif self.acaoMotor == MotorExtracao.Acao.SCRAPING_PARTIDAS:
            scrapWorkCore = ScrapWorkCore()
            filtros = scrapWorkCore.getOpcoesFiltro()
            filtros["tipo"].append(ScrapWork.Tipo.EDICAO_COMPETICAO.name)
            filtros["status"] = [ScrapWork.Status.SCRAPING_PARTIDAS.name,
                                 ScrapWork.Status.PROCESSANDO.name,
                                 ScrapWork.Status.ERRO.name]

            self.itensProcessamento = scrapWorkCore.listScrapWorks(filtros, scrapWorkCore.getOpcoesOrdenacao())

        elif self.acaoMotor == MotorExtracao.Acao.SALVAR_COMPETICOES:
            self.itensProcessamento = scrapWorkCore.getScrapWorksPorTipo(ScrapWork.Tipo.COMPETICAO.name,
                                                                         ScrapWork.Status.AGUARDANDO_SCRAPING.name)


        elif self.acaoMotor == MotorExtracao.Acao.SALVAR_EDICAO_COMPETICAO:
            self.itensProcessamento = scrapWorkCore.getScrapWorksPorTipo(ScrapWork.Tipo.EDICAO_COMPETICAO.name,
                                                                         ScrapWork.Status.AGUARDANDO_SCRAPING.name)


        elif self.acaoMotor == MotorExtracao.Acao.SALVAR_EQUIPE:
            self.itensProcessamento = scrapWorkCore.getScrapWorksPorTipo(ScrapWork.Tipo.EQUIPE.name,
                                                                         ScrapWork.Status.AGUARDANDO_SCRAPING.name)


        elif self.acaoMotor == MotorExtracao.Acao.SALVAR_PARTIDAS:
            self.itensProcessamento = scrapWorkCore.getScrapWorksPorTipo(ScrapWork.Tipo.PARTIDA.name,
                                                                         ScrapWork.Status.AGUARDANDO_SCRAPING.name)

    def getItensProcessamentoMotorAtualizacao(self):
        self.acaoMotor = MotorAtualizacao.Acao(self.codigoAcaoMotor)
        if self.acaoMotor == MotorAtualizacao.Acao.ATUALIZAR_PARTIDAS:

            try:
                partidaCore = PartidaCore()
                data_inicio = datetime.strftime(datetime.today(), "%Y-%m-%d") + " 00:00:00"
                data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d %H:%M:%S")
                data_fim = datetime.now()

                filtrosPartida = partidaCore.getOpcoesFiltro()

                filtrosPartida["dataHoraInicio"] = data_inicio
                filtrosPartida["dataHoraFim"] = data_fim
                filtrosPartida["status"].append(Partida.Status.AGENDADO.name)
                filtrosPartida["status"].append(Partida.Status.RESULTADO_NAO_DISPONIVEL.name)
                filtrosPartida["status"].append(Partida.Status.EM_ANDAMENTO.name)
                filtrosPartida["status"].append(Partida.Status.PRIMEIRO_TEMPO.name)
                filtrosPartida["status"].append(Partida.Status.INTERVALO.name)
                filtrosPartida["status"].append(Partida.Status.SEGUNDO_TEMPO.name)

                return partidaCore.listPartidas(filtrosPartida)
            except Exception as e:
                print(e.args[0])
                return []

        elif self.acaoMotor == MotorAtualizacao.Acao.ATUALIZAR_PARTIDAS_ANTIGAS_NAO_FINALIZADAS:

            try:
                partidaCore = PartidaCore()
                data_inicio = datetime.strftime(datetime.today() - timedelta(days=365 * 10), "%Y-%m-%d") + " 00:00:00"
                data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d %H:%M:%S")
                data_fim = datetime.now()

                filtrosPartida = partidaCore.getOpcoesFiltro()

                # filtrosPartida["dataHoraInicio"] = data_inicio
                filtrosPartida["dataHoraFim"] = data_fim
                filtrosPartida["status"].append(Partida.Status.AGENDADO.name)
                filtrosPartida["status"].append(Partida.Status.RESULTADO_NAO_DISPONIVEL.name)
                filtrosPartida["status"].append(Partida.Status.EM_ANDAMENTO.name)
                filtrosPartida["status"].append(Partida.Status.PRIMEIRO_TEMPO.name)
                filtrosPartida["status"].append(Partida.Status.INTERVALO.name)
                filtrosPartida["status"].append(Partida.Status.SEGUNDO_TEMPO.name)

                return partidaCore.listPartidas(filtrosPartida)
            except Exception as e:
                print(e.args[0])
                return []


        else:
            print("Ação de motor inválida")

    def exibirOpcoesMotor(self):
        for motor in self.tipoMotor:
            print("{} ==> {}".format(motor.value, motor.name))

    def exibirAcoesMotor(self):
        self.tipoMotor.exibirAcoesMotor()

    class Motor(Enum):
        MOTOR_EXTRACAO = 1
        MOTOR_ATUALIZACAO = 2
