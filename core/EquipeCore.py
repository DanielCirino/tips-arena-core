#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime

from utils.HashString import HashString
from repository.Collection import Collection
from models.Equipe import Equipe


class EquipeCore:
    def __init__(self):
        self.collection = Collection("equipes")

    def getOpcoesFiltro(self):
        return {
            "pais": []
        }

    def getOpcoesOrdenacao(self):
        return [{
            "dataCadastro": -1,
            "dataAtualizacao":-1
        }]

    def salvarEquipe(self, equipe: Equipe):
        try:
            equipe.dataAtualizacao = datetime.now()
            if equipe._id == "":
                equipe._id = HashString().encode(equipe.url)
                equipe.dataCadastro = datetime.now()
                return self.collection.inserir_documento(equipe)
            else:
                return self.collection.atualizar_documento(equipe)
        except Exception as e:
            print(e.args)
            return False

    def getEquipePorId(self, id):
        doc = self.collection.get_documento_por_id(id)
        if doc is not None:
            return Equipe(doc)
        else:
            return Equipe()
