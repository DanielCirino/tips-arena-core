# -*- coding: utf-8 -*-
import json
from tipsarena_core.enums.enum_fila import FILA
from tipsarena_core import gerenciador_filas
from tipsarena_core.models.item_extracao import ItemExtracao
from tipsarena_core.services import log_service as log
from tipsarena_core.extratores import motor_extracao_flashscore

topicos = [FILA.FL_EXT_HTML_COMPETICOES_PAIS.value]


def consumirMensagens():
  # Read messages from Kafka, print to stdout
  consumer = gerenciador_filas.obterConsumer(topicos, "grupo-ext-html-competicoes-pais")
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


def processarMensagem(mensagem):
  try:
    payload = mensagem.value().decode("UTF-8")
    dadosMensagem = json.loads(payload)
    itemProcessamento = ItemExtracao(dadosMensagem)
    motor_extracao_flashscore.extrairHtmlCompeticoesPais(itemProcessamento.url)

  except Exception as e:
    log.ERRO(f"Erro ao processar mensagem", e.args)


def processarMensgemErro(erro):
  log.ERRO(erro)


if __name__ == "__main__":
  consumirMensagens()
