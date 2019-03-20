# -*- coding: utf-8 -*-

from enum import Enum

class EdicaoCompeticao:
    def __init__(self, documento:dict={}):
        self._id = ""
        self.idCompeticao = ""
        self.ano = ""
        self.url = ""
        self.totalPartidas = 0
        self.totalPartidasFinalizadas = 0
        self.status = self.Status.NAO_DEFINIDO
        self.dataCadastro = ""
        self.dataAtualizacao = ""

        for key in documento:
            setattr(self, key, documento[key])

    class Status(Enum):
        NAO_INICIADA = 1
        EM_ANDAMENTO = 2
        FINALIZADA = 3
        NAO_DEFINIDO = 4