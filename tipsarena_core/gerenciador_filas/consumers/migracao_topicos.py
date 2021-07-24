# -*- coding: utf-8 -*-
import json
from tipsarena_core.enums.enum_fila import FILA
from tipsarena_core import gerenciador_filas
from tipsarena_core.models.item_extracao import ItemExtracao
from tipsarena_core.services import log_service as log
from tipsarena_core.extratores import motor_extracao_flashscore

topicos = [FILA.FL_EXT_HTML_PARTIDA.value]
ID_GRUPO = "grupo-migracao-topicos"


def consumirMensagens():
  consumer = gerenciador_filas.obterConsumer(topicos, ID_GRUPO)
  try:
    while True:
      msg = consumer.poll(timeout=1.0)
      if msg is None:
        continue
      if msg.error():
        processarMensgemErro(msg.error())
      else:
        processarMensagem(msg)

  except Exception as e:
    log.ERRO("Erro ao consumir mensagens kafka...", e.args)
  finally:
    consumer.close()


def processarMensagem(mensagem):
  try:
    payload = mensagem.value().decode("UTF-8")
    dadosMensagem = json.loads(payload)

    gerenciador_filas.produzirMensagem(FILA.FL_PROC_HTML_PARTIDAS_EDICAO_COMPETICAO.value, dadosMensagem)

  except Exception as e:
    log.ERRO(f"Erro ao processar mensagem", e.args)


def processarMensgemErro(erro):
  log.ERRO(erro)


if __name__ == "__main__":
  consumirMensagens()
