# -*- coding: utf-8 -*-

class Competicao(object):
    def __init__(self, documento: dict = {}):
        self._id = ""
        self.nome = ""
        self.pais = ""
        self.urlLogo = ""
        self.url = ""
        self.dataCadastro = ""
        self.dataAtualizacao = ""

        for key in documento:
            setattr(self, key, documento[key])
