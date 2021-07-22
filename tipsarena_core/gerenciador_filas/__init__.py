# -*- coding: utf-8 -*-
import json
import socket
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer, Consumer
from tipsarena_core.services import log_service as log, auth_service
from tipsarena_core.enums.enum_fila import FILA
from tipsarena_core.models import serealizadorJson

CONF = {'bootstrap.servers': "localhost:9092,localhost:9092",
        'client.id': socket.gethostname()}

cliente = AdminClient(CONF)


def obterFilaPorChave(chave: str):
  for fila in FILA:
    if fila.name == chave:
      return fila


def criarTopicos():
  novosTopicos = [NewTopic(fila.value, 3, 1) for fila in FILA]
  res = cliente.create_topics(novosTopicos)
  for topic, f in res.items():
    try:
      f.result()  # The result itself is None
      log.OK(f"Fila '{topic}' criada com sucesso.")
    except Exception as e:
      log.ERRO(f"Erro ao criar topico '{topic}'.", e.args)


def deletarTopicos():
  nomesTopicos = [fila.value for fila in FILA]
  res = cliente.delete_topics(nomesTopicos)
  for topic, f in res.items():
    try:
      f.result()  # The result itself is None
      log.OK(f"Topico '{topic}' deletado com sucesso.")
    except Exception as e:
      log.ERRO(f"Erro ao deletar topico '{topic}'", e.args)


def produzirMensagem(topico: str, payload: dict):
  try:
    producer = Producer(CONF)
    valores = json.dumps(payload,
                         default=serealizadorJson)

    producer.produce(topico,
                     valores,
                     callback=callbackEntrega)
    producer.poll(1)
  except Exception as e:
    log.ERRO(f"Erro ao produzir mensagem para o topico '{topico}'. [{payload}]", e.args)


def obterConsumer(topicos: [str], idGrupo: str, timeoutSessao=6000):
  try:
    conf = {"bootstrap.servers": "localhost:9092,localhost:9092",
            "group.id": idGrupo, "session.timeout.ms": timeoutSessao,
            "auto.offset.reset": "earliest"}

    consumer = Consumer(conf)
    # Subscribe to topics
    consumer.subscribe(topicos, on_assign=callbackAssinaturaTopico)
    return consumer
  except Exception as e:
    log.ERRO("Erro ao gerar consumer...", e)


def callbackAssinaturaTopico(consumer: Consumer, particoes):
  for particao in particoes:
    if particao.error is None:
      log.OK(f"Assinatura ao topico: '{particao.topic}' feita com sucesso. [{particao}]")
    else:
      log.ERRO(f"Erro ao assinar topico: {particao.topic}", particao.error)


def callbackEntrega(err, msg):
  if err:
    log.ERRO(f"Erro ao produzir mensagem: [{err}].")
  else:
    log.OK(f"topico: {msg.topic()} | particao: {msg.partition()} offset:{msg.offset()}")


if __name__ == '__main__':
  deletarTopicos()
  criarTopicos()
