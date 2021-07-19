# -*- coding: utf-8 -*-
from tipsarena_core import gerenciador_filas
from tipsarena_core.services import log_service as log
import random


def teste_gerar_100_mensagens():
  i = 0
  for i in range(100):
    gerenciador_filas.produzirMensagem('ta-teste-kafka-python', str(random.randint(1, 999)))
    i += 1

  log.INFO("100 mensagens geradas...")
  assert i == 100


if __name__ == "__main__":
  teste_gerar_100_mensagens()
