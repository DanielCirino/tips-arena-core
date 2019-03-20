# -*- coding: utf-8 -*-

from enum import Enum


class ScrapWork(object):
    def __init__(self, documento: dict = {}):
        self._id = ""
        self.idPai = 0
        self.url = ""
        self.tipo = ""
        self.status = ""
        self.target = 0
        self.prioridadeExtracao = 0
        self.dataCadastro = ""
        self.dataAtualizacao = ""

        if documento is not None:
            for key in documento:
                setattr(self, key, documento[key])

    class Tipo(Enum):
        PAIS = 1
        COMPETICAO = 2
        EQUIPE = 3
        PARTIDA = 4
        EDICAO_COMPETICAO = 5

    class Status(Enum):
        SCRAPING_COMPETICOES = 1
        SCRAPING_PARTIDAS = 2
        AGUARDANDO_SCRAPING = 3
        ERRO = 4
        OK = 5
        PROCESSANDO = 6
        SCRAPING_EQUIPES = 7
        SCRAPING_EDICOES_COMPETICAO = 8
        ERRO_SCRAPING_EQUIPES = 9
        ERRO_SCRAPING_PARTIDAS = 10
