#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime

from utils.HashString import HashString
from repository.Collection import Collection
from models.Competicao import Competicao


class CompeticaoCore:
    def __init__(self):
        self.collection = Collection("competicoes")

    def getOpcoesFiltro(self):
        return {
            "pais": []
        }

    def getOpcoesOrdenacao(self):
        return [{
            "dataCadastro": -1,
            "dataAtualizacao":-1
        }]

    def salvarCompeticao(self, competicao: Competicao):
        try:
            competicao.dataAtualizacao = datetime.now()
            if competicao._id == "":
                competicao._id = HashString().encode(competicao.url)
                competicao.dataCadastro = datetime.now()
                return self.collection.inserir_documento(competicao)
            else:
                return self.collection.atualizar_documento(competicao)
        except Exception as e:
            print(e.args)
            return False

    def getCompeticaoPorId(self, id):
        try:
            doc = self.collection.get_documento_por_id(id)
            if doc is not None:
                return Competicao(doc)
            else:
                return Competicao()
        except Exception as e:
            return None