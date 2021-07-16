from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer
from tipsarena_core.services import log_service as log
from tipsarena_core.enums.enum_fila import Fila

conf = {'bootstrap.servers': 'localhost:9092'}
cliente = AdminClient(conf)

def obterFilaPorChave(chave: str):
  for fila in Fila:
    if fila.name == chave:
      return fila


def criarTopicos():
  novosTopicos = [NewTopic(fila.value, 3, 1) for fila in Fila]
  res = cliente.create_topics(novosTopicos)
  for topic, f in res.items():
    try:
      f.result()  # The result itself is None
      log.OK(f"Fila '{topic}' criada com sucesso.")
    except Exception as e:
      log.ERRO(f"Erro ao criar topico '{topic}'.", e.args)


def deletarTopicos():
  nomesTopicos = [fila.value for fila in Fila]
  res = cliente.delete_topics(nomesTopicos)
  for topic, f in res.items():
    try:
      f.result()  # The result itself is None
      log.OK(f"Topico '{topic}' deletado com sucesso.")
    except Exception as e:
      log.ERRO(f"Erro ao deletar topico '{topic}'", e.args)


def produzirMensagem(topico: str, conteudo: str):
  try:
    Producer.produce(topico, conteudo)
  except Exception as e:
    pass


if __name__ == '__main__':
  deletarTopicos()
  criarTopicos()
