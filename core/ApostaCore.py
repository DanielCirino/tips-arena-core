# -*- coding: utf-8 -*-

from datetime import datetime

from bson import ObjectId

from core.TransacaoCore import TransacaoCore
from models.Partida import Partida
from models.Transacao import Transacao
from repository.Collection import Collection
from models.Aposta import Aposta


class ApostaCore:
    def __init__(self):
        self.collection = Collection("apostas")

    def getOpcoesFiltro(self):
        return {
            "idUsuario": "",
            "idPartida": "",
            "dataCadastroInicio": "",
            "dataCadastroFim": "",
            "status": [],
            "mercado": []
        }

    def getOpcoesOrdenacao(self):
        return [{
            "dataCadastro": -1,
            "dataAtualizacao": -1
        }]

    def salvarAposta(self, aposta: Aposta):
        try:
            aposta.dataAtualizacao = datetime.utcnow()
            if aposta._id == "":
                delattr(aposta, "_id")
                aposta.idUsuario = ObjectId(aposta.idUsuario)
                aposta.dataCadastro = datetime.utcnow()
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
            filtroDataCadastro = {}

            if filter != {}:
                if filter["idUsuario"] == "":
                    del filter["idUsuario"]

                if filter["idPartida"] == "":
                    del filter["idPartida"]

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

                if filtroDataCadastro != {}:
                    filter["dataCadastro"] = filtroDataCadastro

            docs = self.collection.listarDocumentos(filter, [("dataCadastro", -1)], limit, skip)

            for doc in docs:
                listaApostas.append(Aposta(doc))

            return listaApostas
        except Exception as e:
            print(e.args)
            return None

    def analisarResultadoPartida(self, placarMandante: int, placarVisitante: int):
        analise = {
            "resultado": "",
            "drawNoBet": "ANULA_APOSTA",
            "duplaChance": "",
            "imparPar": "",
            "btts": "",
            "underOver": [],
            "placar": "PLACAR_{}_{}".format(placarMandante, placarVisitante),
        }
        try:
            totalGols = placarMandante + placarVisitante

            if placarMandante == placarVisitante:
                analise["resultado"] = "EMPATE"

            elif placarMandante > placarVisitante:
                analise["resultado"] = "VITORIA_MANDANTE"
                analise["drawNoBet"] = "DNB_MANDANTE"
            else:
                analise["resultado"] = "VITORIA_VISITANTE"
                analise["drawNoBet"] = "DNB_VISITANTE"

            if analise["resultado"] == "EMPATE" or analise["resultado"] == "VITORIA_MANDANTE":
                analise["duplaChance"] = "CONTRA_VISITANTE"
            elif analise["resultado"] == "EMPATE" or analise["resultado"] == "VITORIA_VISITANTE":
                analise["duplaChance"] = "CONTRA_MANDANTE"
            elif analise["resultado"] == "VITORIA_MANDANTE" or analise["resultado"] == "VITORIA_VISITANTE":
                analise["duplaChance"] = "CONTRA_EMPATE"

            analise["imparPar"] = "ODD" if totalGols % 2 == 0 else "EVEN"

            if placarMandante > 0 and placarVisitante > 0:
                analise["btts"] = "BTTS_YES"
            else:
                analise["btts"] = "BTTS_NO"

            analise["totalGols"] = totalGols

            return analise

        except Exception as e:
            print(e.argsp[0])
            return analise

    def finalizarApostasPartida(self, partida: Partida):
        try:
            placarPartida = partida.placarFinal.split(":")
            analiseResultado = self.analisarResultadoPartida(int(placarPartida[0]), int(placarPartida[1]))

            filtrosAposta = self.getOpcoesFiltro()
            filtrosAposta["idPartida"] = partida._id
            filtrosAposta["status"].append(Aposta.Status.PENDENTE.name)

            apostasPartida = ApostaCore().listarApostas(filtrosAposta)

            for aposta in apostasPartida:
                if (partida.status == Partida.Status.FINALIZADO.name):
                    if aposta.mercado == Aposta.Mercados.RESULT.name:
                        self.finalizarAposta(aposta, aposta.opcaoMercado == analiseResultado["resultado"])

                    if aposta.mercado == Aposta.Mercados.DNB.name:
                        if analiseResultado["drawNoBet"] == "ANULA_APOSTA":
                            self.cancelarAposta(aposta)
                        else:
                            self.finalizarAposta(aposta, aposta.opcaoMercado == analiseResultado["drawNoBet"])

                    if aposta.mercado == Aposta.Mercados.DOUBLE_CHANCE.name:
                        self.finalizarAposta(aposta, aposta.opcaoMercado == analiseResultado["duplaChance"])

                    if aposta.mercado == Aposta.Mercados.BTTS.name:
                        self.finalizarAposta(aposta, aposta.opcaoMercado == analiseResultado["btts"])

                    if aposta.mercado == Aposta.Mercados.ODD_EVEN.name:
                        self.finalizarAposta(aposta, aposta.opcaoMercado == analiseResultado["imparPar"])

                    if aposta.mercado == Aposta.Mercados.CORRECT_SCORE.name:
                        self.finalizarAposta(aposta, aposta.opcaoMercado == analiseResultado["placar"])

                    if aposta.mercado == Aposta.Mercados.UNDER_OVER.name:
                        self.finalizarApostaUnderOver(aposta, analiseResultado["totalGols"])
                else:
                    if aposta.mercado == Aposta.Mercados.CORRECT_SCORE.name:
                        self.analisarApostaPlacarExato(aposta, int(placarPartida[0]), int(placarPartida[1]))

                    if aposta.mercado == Aposta.Mercados.BTTS.name:
                        self.analisarApostaBtts(aposta, int(placarPartida[0]), int(placarPartida[1]))

                    if aposta.mercado == Aposta.Mercados.UNDER_OVER.name:
                        self.analisarApostaUnderOver(aposta, analiseResultado["totalGols"])


        except Exception as e:
            print(e.args[0])

    def finalizarAposta(self, aposta: Aposta, apostaCerta):
        try:

            lucroAposta = (aposta.valor * aposta.valorOdd) - aposta.valor if apostaCerta else 0
            resultadoAposta = Aposta.Resultado.LUCRO.name if apostaCerta else Aposta.Resultado.PREJUIZO.name

            # Salvar transacao da aposta em caso de acerto
            if apostaCerta:
                transacao = Transacao()
                transacao.idUsuario = aposta.idUsuario
                transacao.tipo = Transacao.Tipo.RESULTADO_APOSTA.name
                transacao.operacao = Transacao.Operacao.CREDITO.name
                transacao.descricao = "Muito bem \\0/. Você acertou a aposta {}.".format(aposta.descricao)
                transacao.valor = round(aposta.valor * aposta.valorOdd, 2)

                transacaoSalva = TransacaoCore().salvarTransacao(transacao)
                print(transacaoSalva.inserted_id)

            aposta.lucro = round(lucroAposta, 2)
            aposta.resultado = resultadoAposta
            aposta.status = Aposta.Status.FINALIZADA.name
            self.salvarAposta(aposta)

        except Exception as e:
            print(e.args)

    def analisarApostaPlacarExato(self, aposta, placarMandante: int, placarVisitante: int):
        try:
            detalhesAposta = aposta.opcaoMercado.split("_")
            finalizarAposta = int(detalhesAposta[1]) < placarMandante or int(detalhesAposta[2]) < placarVisitante

            if finalizarAposta:
                self.finalizarAposta(aposta, False)

        except Exception as e:
            print(e.args[0])

    def finalizarApostaUnderOver(self, aposta: Aposta, totalGols: int):
        try:
            detalhesAposta = aposta.opcaoMercado.split("_")  # UNDER_4_5
            if detalhesAposta[0] == "UNDER":
                apostaCerta = int(detalhesAposta[1]) <= totalGols
            if detalhesAposta[0] == "OVER":
                apostaCerta = int(detalhesAposta[1]) > totalGols

            self.finalizarAposta(aposta, apostaCerta)

        except Exception as e:
            print(e.args[0])

    def analisarApostaUnderOver(self, aposta: Aposta, totalGols: int):
        try:
            detalhesAposta = aposta.opcaoMercado.split("_")  # UNDER_1_5
            finalizarAposta = totalGols > int(detalhesAposta[1])

            if finalizarAposta:
                apostaCerta = detalhesAposta[0] == "OVER"
                self.finalizarAposta(aposta, apostaCerta)

        except Exception as e:
            print(e.args[0])

    def analisarApostaBtts(self, aposta, placarMandante: int, placarVisitante: int):
        try:
            ambosMarcaram = placarMandante > 0 and placarVisitante > 0

            if ambosMarcaram:
                apostaCerta = (aposta.opcaoMercado == "BTTS_YES")
                self.finalizarAposta(aposta, apostaCerta)

        except Exception as e:
            print(e.args[0])

    def cancelarAposta(self, aposta: Aposta):
        try:
            transacao = Transacao()
            transacao.idUsuario = aposta.idUsuario
            transacao.tipo = Transacao.Tipo.CANCELAMENTO_APOSTA.name
            transacao.operacao = Transacao.Operacao.CREDITO.name
            transacao.descricao = "Apota cancelada: {}".format(aposta.descricao)
            transacao.valor = aposta.valor

            transacaoSalva = TransacaoCore().salvarTransacao(transacao)
            print(transacaoSalva.inserted_id)

            if transacaoSalva:
                aposta.resultado = Aposta.Resultado.CANCELADA.name
                aposta.status = Aposta.Status.CANCELADA.name
                self.salvarAposta(aposta)

        except Exception as e:
            print(e.args[0])
