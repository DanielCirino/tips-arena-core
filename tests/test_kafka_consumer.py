# -*- coding: utf-8 -*-
import sys
from confluent_kafka.error import KafkaException
from tipsarena_core import gerenciador_filas
from tipsarena_core.services import log_service as log


def teste_gerar_consumer():
  topicos = ['ta-teste-kafka-python']
  consumer = gerenciador_filas.obterConsumer(topicos, "grupo_teste")

  # Read messages from Kafka, print to stdout
  try:
    while True:
      msg = consumer.poll(timeout=1.0)
      if msg is None:
        continue
      if msg.error():
        raise KafkaException(msg.error())
      else:
        # Proper message
        sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                         (msg.topic(), msg.partition(), msg.offset(),
                          str(msg.key())))
        print(msg.value())
  except Exception as e:
    log.ERRO("Erro consumer kafka...", e.args)


if __name__ == "__main__":
  teste_gerar_consumer()
