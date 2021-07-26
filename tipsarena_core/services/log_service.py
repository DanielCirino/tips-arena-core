# -*- coding: utf-8 -*-
from datetime import datetime

""""
  Imprimir mensagem no console
  Tipos: OK, ALERTA, INFO, ERRO
"""


def OK(mensagem: str):
  print(f"\033[92mOK:     \033[00m | {datetime.now()} | {mensagem} |")


def ALERTA(mensagem: str):
  print(f"\033[93mALERTA: \033[00m | {datetime.now()} | {mensagem} |")


def INFO(mensagem: str):
  print(f"\033[96mINFO:   \033[00m | {datetime.now()} | {mensagem} |")


def ERRO(mensagem: str, erros=""):
  print(f"\033[91mERRO:   \033[00m | {datetime.now()} | \033[91m{mensagem} | {erros} | ")
