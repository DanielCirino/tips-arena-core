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

