# -*- coding: utf-8 -*-
from enum import Enum


class Transacao:
    def __init__(self, documento: dict = {}):
        self._id = ""
        self.idUsuario = ""
        self.tipo = ""
        self.descricao = ""
        self.operacao = ""
        self.valor = 0.0
        self.efetivado = False
        self.dataCadastro = ""
        self.dataAtualizacao = ""

        for key in documento:
            setattr(self, key, documento[key])

    class Tipo(Enum):
        ACESSO_DIARIO = 1
        APOSTA = 2
        CANCELAMENTO_APOSTA = 3
        RESULTADO_APOSTA = 4
        CONVITE = 5
        ATIVACAO_CADASTRO = 6
        BONUS_VIDEO = 7

    class Operacao(Enum):
        DEBITO = 1
        CREDITO = 2


