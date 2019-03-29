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
    def __init__(self, codigo_motor, codigo_acao_motor, qtd_threads):
        try:
            self.data_inicio = datetime.now()

            self.codigo_motor = codigo_motor
            self.codigo_acao_motor = codigo_acao_motor
            self.qtd_threads = qtd_threads
            self.itens_processamento = []
            self.total_itens_processamento = 0

            self.total_itens_processados = 0
            self.total_itens_erro = 0
            self.processamento_finalizado = False

            self.tipo_motor = self.Motor(codigo_motor)
            self.acao_motor = None
            self.id_processamento_batch = ""

            if self.codigo_motor != 0:
                if self.codigo_acao_motor == 0:
                    self.exibir_acoes_motor()
                else:
                    self.iniciar_processamento()
            else:
                self.exibir_opcoes_motor()

        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__))
            print("Erro processamento.[Motor:{}][Acao:{}]".format(self.tipo_motor, self.codigo_acao_motor))

    def iniciar_processamento(self):
        try:
            itens_processamento = []
            if self.tipo_motor == self.tipo_motor.MOTOR_EXTRACAO:
                motor = MotorExtracao
                self.getItensProcessamentoMotorExtracao()
            elif self.tipo_motor == self.tipo_motor.MOTOR_ATUALIZACAO:
                motor = MotorAtualizacao
                itens_processamento = self.getItensProcessamentoMotorAtualizacao()
            else:
                print("Motor inválido...")
                return

            total_itens_processamento = len(itens_processamento)

            print("Lista de processamento possui {}".format(total_itens_processamento))

            processamento = ProcessamentoBatch()
            processamento.tipo = self.acao_motor.name
            processamento.status = ProcessamentoBatch.Status.NAO_INICIADO.name
            processamento.totalRegistros = total_itens_processamento

            processamentoBatch = ProcessamentoBatchCore().salvarProcessamentoBatch(processamento)

            if processamentoBatch is not None:
                self.id_processamento_batch = processamentoBatch.inserted_id
                self.lista_threads = []

                for id_thread in range(0, self.qtd_threads):
                    thread = motor(self.acao_motor, id_thread, self.qtd_threads,
                                   itens_processamento)
                    thread.start()
                    self.lista_threads.insert(id_thread, thread)

                self.atualizar_processamento()
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__))

    def atualizar_processamento_batch(self, quantidade_sucesso, quantidade_erro, status, data_hora_fim=None):
        try:
            processamentoCore = ProcessamentoBatchCore()
            processamento_batch = processamentoCore.getProcessamentoBatchById(self.id_processamento_batch)

            if processamento_batch._id != "":
                processamento_batch.totalSucesso = quantidade_sucesso
                processamento_batch.totalErro = quantidade_erro
                processamento_batch.status = status
                processamento_batch.dataHoraFim = data_hora_fim

            return processamentoCore.salvarProcessamentoBatch(processamento_batch)
        except Exception as e:
            print(e.args[0])
            return None

    def atualizar_processamento(self):
        try:
            while not self.verificar_fim_processamento():
                time.sleep(300)
                quantidades_processadas = self.get_quantidade_processada()
                self.atualizar_processamento_batch(quantidades_processadas[0], quantidades_processadas[1],
                                                   ProcessamentoBatch.Status.EM_PROCESSAMENTO.name)

            quantidades_processadas = self.get_quantidade_processada()
            self.atualizar_processamento_batch(quantidades_processadas[0], quantidades_processadas[1],
                                               ProcessamentoBatch.Status.FINALIZADO.name, datetime.now())
        except Exception as e:
            print(e.args)

    def verificar_fim_processamento(self) -> bool:
        finalizado = True
        for thread in self.lista_threads:
            finalizado = finalizado and thread.processamentoFinalizado

        return finalizado

    def get_quantidade_processada(self):
        qtd_sucesso = 0
        qtd_erro = 0

        for thread in self.lista_threads:
            qtd_sucesso += thread.totalSucesso
            qtd_erro += thread.totalErros

        return [qtd_sucesso, qtd_erro]

    def getItensProcessamentoMotorExtracao(self):
        self.acao_motor = MotorExtracao.Acao(self.codigo_acao_motor)
        scrapWorkCore = ScrapWorkCore()

        if self.acao_motor == MotorExtracao.Acao.SCRAPING_PAISES:
            self.itens_processamento = ScraperPais().getListaPaises()

        elif self.acao_motor == MotorExtracao.Acao.SCRAPING_COMPETICOES:
            self.itens_processamento = scrapWorkCore.getScrapWorksPorTipo(ScrapWork.Tipo.PAIS.name,
                                                                          ScrapWork.Status.SCRAPING_COMPETICOES.name)

        elif self.acao_motor == MotorExtracao.Acao.SCRAPING_EDICOES_COMPETICAO:
            self.itens_processamento = scrapWorkCore.getScrapWorksPorTipo(ScrapWork.Tipo.COMPETICAO.name,
                                                                          ScrapWork.Status.SCRAPING_EDICOES_COMPETICAO.name)
        elif self.acao_motor == MotorExtracao.Acao.SCRAPING_EQUIPES:
            self.itens_processamento = scrapWorkCore.getScrapWorksPorTipo(ScrapWork.Tipo.EDICAO_COMPETICAO.name,
                                                                          ScrapWork.Status.SCRAPING_EQUIPES.name)
        elif self.acao_motor == MotorExtracao.Acao.SCRAPING_PARTIDAS:
            scrapWorkCore = ScrapWorkCore()
            filtros = scrapWorkCore.getOpcoesFiltro()
            filtros["tipo"].append(ScrapWork.Tipo.EDICAO_COMPETICAO.name)
            filtros["status"] = [ScrapWork.Status.SCRAPING_PARTIDAS.name,
                                 ScrapWork.Status.PROCESSANDO.name,
                                 ScrapWork.Status.ERRO.name]

            self.itens_processamento = scrapWorkCore.listScrapWorks(filtros, scrapWorkCore.getOpcoesOrdenacao())

        elif self.acao_motor == MotorExtracao.Acao.SALVAR_COMPETICOES:
            self.itens_processamento = scrapWorkCore.getScrapWorksPorTipo(ScrapWork.Tipo.COMPETICAO.name,
                                                                          ScrapWork.Status.AGUARDANDO_SCRAPING.name)


        elif self.acao_motor == MotorExtracao.Acao.SALVAR_EDICAO_COMPETICAO:
            self.itens_processamento = scrapWorkCore.getScrapWorksPorTipo(ScrapWork.Tipo.EDICAO_COMPETICAO.name,
                                                                          ScrapWork.Status.AGUARDANDO_SCRAPING.name)


        elif self.acao_motor == MotorExtracao.Acao.SALVAR_EQUIPE:
            self.itens_processamento = scrapWorkCore.getScrapWorksPorTipo(ScrapWork.Tipo.EQUIPE.name,
                                                                          ScrapWork.Status.AGUARDANDO_SCRAPING.name)


        elif self.acao_motor == MotorExtracao.Acao.SALVAR_PARTIDAS:
            self.itens_processamento = scrapWorkCore.getScrapWorksPorTipo(ScrapWork.Tipo.PARTIDA.name,
                                                                          ScrapWork.Status.AGUARDANDO_SCRAPING.name)

    def getItensProcessamentoMotorAtualizacao(self):
        self.acao_motor = MotorAtualizacao.Acao(self.codigo_acao_motor)
        if self.acao_motor == MotorAtualizacao.Acao.ATUALIZAR_PARTIDAS:

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

        elif self.acao_motor == MotorAtualizacao.Acao.ATUALIZAR_PARTIDAS_ANTIGAS_NAO_FINALIZADAS:

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

        elif self.acao_motor == MotorAtualizacao.Acao.VALIDAR_PARTIDAS_DO_DIA:
            try:
                extrator = ScraperPartida()
                itens_processamento = extrator.getListaPartidasDia()
                extrator.finalizarWebDriver()
                return itens_processamento
            except Exception as e:
                print(e.args[0])
                return []
        else:
            print("Ação de motor inválida")

    def exibir_opcoes_motor(self):
        for motor in self.tipo_motor:
            print("{} ==> {}".format(motor.value, motor.name))

    def exibir_acoes_motor(self):
        self.tipo_motor.exibirAcoesMotor()

    class Motor(Enum):
        MOTOR_EXTRACAO = 1
        MOTOR_ATUALIZACAO = 2
