# -*- coding: utf-8 -*-

from datetime import datetime
from repository.Collection import Collection
from models.Aposta import Aposta


class ApostaCore:
    def __init__(self):
        self.collection = Collection("apostas")

    def getOpcoesFiltro(self):
        return {
            "idUsuario": "",
            "idPartida":"",
            "status":[],
            "mercado":[]
        }

    def getOpcoesOrdenacao(self):
        return [{
            "dataCadastro": -1,
            "dataAtualizacao":-1
        }]

    def salvarAposta(self, aposta: Aposta):
        try:
            aposta.dataAtualizacao = datetime.now()
            if aposta._id == "":
                aposta.dataCadastro = datetime.now()
                return self.collection.inserirDocumento(aposta)
            else:
                return self.collection.atualizarDocumento(aposta)
        except Exception as e:
            print(e.args)
            return False

    def obterApostaPorId(self, id):
        doc = self.collection.obterDocumentoPorId(id)
        if doc is not None:
            return Aposta(doc)
        else:
            return Aposta()

    def listarApostas(self, filter={}, sort=[], limit=0, skip=0):
        try:
            listaApostas = []
            filtroDataHora = {}

            if filter != {}:
                if filter["idEdicaoCompeticao"] == "":
                    del filter["idEdicaoCompeticao"]

                if filter["dataHoraInicio"] != "":
                    filtroDataHora["$gte"] = filter["dataHoraInicio"]

                del filter["dataHoraInicio"]

                if filter["dataHoraFim"] != "":
                    filtroDataHora["$lte"] = filter["dataHoraFim"]

                del filter["dataHoraFim"]

                if len(filter["status"]) == 0:
                    del filter["status"]
                else:
                    filter["status"] = {"$in": filter["status"]}

                filter["dataHora"] = filtroDataHora
            docs = self.collection.listarDocumentos(filter, [("dataHora", -1)], limit, skip)

            for doc in docs:
                listaApostas.append(Aposta(doc))

            return listaApostas
        except Exception as e:
            print(e.args)
            return None
