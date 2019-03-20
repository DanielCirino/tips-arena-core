# -*- coding: utf-8 -*-

from enum import Enum


class Partida(object):
    def __init__(self, documento: dict = {}):
        self._id = ""
        self.idCompeticao = ""
        self.idEquipeMandante = 0
        self.idEquipeVisitante = 0
        self.dataHora = ""
        self.faseCompeticao = ""
        self.status = self.Status.AGENDADO.name
        self.minutos = ""
        self.placarPrimeiroTempo = ":"
        self.placarSegundoTempo = ":"
        self.placarProrrogacao = ":"
        self.placarPenalties = ":"
        self.placarFinal = ":"

        self.url = ""
        self.tags = []
        self.timelineDisponivel = False
        self.timeline = []

        self.estatisticasDisponiveis = False
        self.estatisticas = ""

        self.oddsDisponiveis = False
        self.odds = []

        self.lineupsDisponivel = False
        self.lineups = []

        self.relatorioDisponivel = False
        self.relatorio = []

        self.headToHeadDisponivel = False
        self.headToHead = []

        self.videosDisponiveis = False
        self.videos = []

        self.fotosDisponiveis = False
        self.fotos = []

        self.noticiasDisponiveis = False
        self.noticias = []

        self.competicao = {}
        self.equipeMandante = {}
        self.equipeVisitante = {}

        self.dataCadastro = ""
        self.dataAtualizacao = ""

        for key in documento:
            setattr(self, key, documento[key])



    class Status(Enum):
        AGENDADO = 1
        ADIADO = 2
        SUSPENSO = 3
        CANCELADO = 4
        PRIMEIRO_TEMPO = 5
        INTERVALO = 6
        SEGUNDO_TEMPO = 7
        FINALIZADO = 8
        EM_ANDAMENTO = 9
        ABANDONADO = 10
        RESULTADO_NAO_DISPONIVEL = 11
        W_O = 12

    class StatusCalculoProbabilidades(Enum):
        PENDENTE = 1
        CALCULADO = 2
        ERRO = 3

    class StatusAnaliseProbabilidades(Enum):
        PENDENTE = 1
        ANALISADO = 2
        ERRO = 3
