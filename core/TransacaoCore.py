# -*- coding: utf-8 -*-

from datetime import datetime

from bson import ObjectId

from repository.Collection import Collection
from models.Transacao import Transacao


class TransacaoCore:
    def __init__(self):
        self.collection = Collection("transacoes")

    def getOpcoesFiltro(self):
        return {
            "idUsuario": "",
            "dataCadastroInicio": "",
            "dataCadastroFim": "",
            "tipo": [],
            "operacao": [],
            "efetivado": ""
        }

    def getOpcoesOrdenacao(self):
        return [{
            "dataCadastro": -1,
            "dataAtualizacao": -1
        }]

    def salvarTransacao(self, transacao: Transacao):
        try:
            transacao.dataAtualizacao = datetime.utcnow()
            if transacao._id == "":
                delattr(transacao, "_id")
                transacao.idUsuario = ObjectId(transacao.idUsuario)
                transacao.dataCadastro = datetime.utcnow()
                return self.collection.inserirDocumento(transacao)
            else:
                return self.collection.atualizarDocumento(transacao)
        except Exception as e:
            print(e.args)
            return False

    def obterTransacaoPorId(self, id):
        doc = self.collection.obterDocumentoPorId(id)
        if doc is not None:
            return Transacao(doc)
        else:
            return Transacao()

    def listarTransacoes(self, filter={}, sort=[], limit=0, skip=0):
        try:
            listaTransacoes = []
            filtroDataCadastro = {}

            if filter != {}:
                if filter["idUsuario"] == "":
                    del filter["idUsuario"]

                if filter["efetivado"] == "":
                    del filter["efetivado"]

                if filter["dataCadastroInicio"] != "":
                    filtroDataCadastro["$gte"] = filter["dataCadastroInicio"]

                del filter["dataCadastroInicio"]

                if filter["dataCadastroFim"] != "":
                    filtroDataCadastro["$lte"] = filter["dataCadastroFim"]

                del filter["dataCadastroFim"]

                if len(filter["mercado"]) == 0:
                    del filter["mercado"]
                else:
                    filter["mercado"] = {"$in": filter["mercado"]}

                if len(filter["status"]) == 0:
                    del filter["status"]
                else:
                    filter["status"] = {"$in": filter["status"]}

                filter["dataCadastro"] = filtroDataCadastro

            docs = self.collection.listarDocumentos(filter, [("dataCadastro", -1)], limit, skip)

            for doc in docs:
                listaTransacoes.append(Transacao(doc))

            return listaTransacoes
        except Exception as e:
            print(e.args)
            return None
