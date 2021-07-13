# -*- coding: utf-8 -*-

""""
  Imprimir mensagem no console
  Tipos: OK, ALERTA, INFO, ERRO
"""


def OK(mensagem: str):
  print("\033[92m{} \033[00m[{}]".format('OK:     ', mensagem))


def ALERTA(mensagem: str):
  print("\033[93m{} \033[00m[{}]".format('ALERTA: ', mensagem))


def INFO(mensagem: str):
  print("\033[96m{} \033[00m [{}]".format('INFO:  ', mensagem))


def ERRO(mensagem: str, erros=""):
  print("\033[91m{} {} \033[00m[{}]".format('ERRO:   ', mensagem, erros))
