# -*- coding: utf-8 -*-
import os
import json
from tipsarena_core.enums.enum_fila import FILA
from tipsarena_core import gerenciador_filas
from tipsarena_core.models.item_extracao import ItemExtracao
from tipsarena_core.services import log_service as log
from tipsarena_core.parsers_html import motor_parser_flashscore

topicos = [FILA.FL_PROC_HTML_EDICOES_COMPETICAO.value]
ID_GRUPO = "grupo-proc-html-edicoes-competicao"


def consumirMensagens():
  """
  Método para consumir processar as mensagens presentes no tópico de processar o html das edições de uma competição.
  """
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
  """
  Método para consumir processar as mensagens presentes no tópico de processamento do html das edições de uma competição.
  """
  try:
    payload = mensagem.value().decode("UTF-8")
    dadosMensagem = json.loads(payload)
    itemProcessamento = ItemExtracao(dadosMensagem)
    caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}edicoes_competicao/{itemProcessamento.nomeArquivo}"
    motor_parser_flashscore.processarHtmlEdicoesCompeticao(caminhoArquivo)

  except Exception as e:
    log.ERRO(f"Erro ao processar mensagem", e.args)


def processarMensgemErro(erro):
  log.ERRO(erro)


if __name__ == "__main__":
  consumirMensagens()
