# -*- coding: utf-8 -*-

import threading
import time


class Motor(threading.Thread):
    def __init__(self, acaoMotor, idThread, totalThreads, listaProcessamento):
        try:
            self.acaoMotor = acaoMotor
            self.idThread = idThread
            self.totalThreads = totalThreads

            self.listaProcessamento = listaProcessamento
            self.totalItens = len(listaProcessamento)

            self.totalSucesso = 0
            self.totalErros = 0
            self.horaInicio = time.strftime("%Y-%m-%d %H:%M:%S")
            self.horaFim = None
            self.processamentoFinalizado = False

            self.extrator = None

        except Exception as e:
            print(e.args[0])

    def run(self):
        print("Processamento não implmentado....")
        exit(0)
