# -*- coding: utf-8 -*-
from enum import Enum


class Aposta:
    def __init__(self, documento: dict = {}):
        self._id = ""
        self.idUsuario = ""
        self.idPartida = ""
        self.descricao = ""
        self.mercado = ""
        self.opcaoMercado = ""
        self.valor = 0.0
        self.valorOdd = 0.0
        self.lucro = 0.0
        self.status = ""
        self.resultado = ""
        self.dataCadastro = ""
        self.dataAtualizacao = ""

        for key in documento:
            setattr(self, key, documento[key])

    class Status(Enum):
        PENDENTE = 1
        FINALIZADA = 2
        CANCELADA = 3

    class Mercados(Enum):
        RESULT = 1
        DNB = 2
        DOUBLE_CHANCE = 3
        ODD_EVEN = 4
        BTTS = 5
        CORRECT_SCORE = 6
        UNDER_OVER = 7

    class Resultado(Enum):
        PENDENTE = 1
        LUCRO = 2
        PREJUIZO = 3
        CANCELADA = 4
