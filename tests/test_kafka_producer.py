from tipsarena_core import gerenciador_filas
from tipsarena_core.services import log_service as log
import random


def teste_gerar_100000_mensagens():
  i = 0
  for i in range(100000):
    gerenciador_filas.produzirMensagem('ta-teste-kafka-python', random.randint(1, 999))
    i += 1

  log.INFO("10000 mensagens geradas...")
  assert i == 100000


if __name__ == "__main__":
  teste_gerar_100000_mensagens()
