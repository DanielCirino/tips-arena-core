# -*- coding: utf-8 -*-

from enum import Enum
from datetime import datetime


class ProcessamentoBatch(object):
    def __init__(self, documento: dict = {}):
        self._id = ""
        self.tipo = ""
        self.status = ""
        self.totalRegistros = 0
        self.totalSucesso = 0
        self.totalErro = 0
        self.detalhes = 0
        self.dataHoraInicio = datetime.now()
        self.dataHoraFim = None
        self.dataAtualizacao = datetime.now()

        if documento is not None:
            for key in documento:
                setattr(self, key, documento[key])

    class Tipo(Enum):
        EXTRACAO_PARTIDAS_DIA = 1
        ATUALIZACAO_PARTIDAS_DIA = 2
        ATUALIZACAO_PARTIDAS_ANTIGAS_NAO_FINALIZADAS = 3

    class Status(Enum):
        NAO_INICIADO = 1
        EM_PROCESSAMENTO = 2
        FINALIZADO = 3
        ERRO = 4
