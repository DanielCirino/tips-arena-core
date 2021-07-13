# -*- coding: utf-8 -*-

""""
  Imprimir mensagem no console
  Tipos: OK, ALERTA, INFO, ERRO, ALERTA
"""


def imprimirMensagem(tipo: str, mensagem, erros= ""):
  if tipo == "OK":
    print("\n\033[92m [{}] {}\033[00m".format(tipo, mensagem))
    return

  if tipo == "ALERTA":
    print("\n\033[93m [{}] {}\033[00m".format(tipo, mensagem))
    return

  if tipo == "INFO":
    print("\n\033[96m [{}] {}\033[00m".format(tipo, mensagem))
    return

  if tipo == "ERRO":
    print("\033[91m [{}] {} [{}]\033[00m".format(tipo, mensagem, erros))
    return

  print("\033[94m [{}] {}\033[00m".format(tipo, mensagem))
