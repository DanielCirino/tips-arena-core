# -*- coding: utf-8 -*-

from datetime import datetime
from tipsarena_core.utils import datetime_utils as dtu


def teste_conversao_data(log):
  str_data = "16.02.2019 11:00"
  data_from_string = datetime.strptime(str_data, "%d.%m.%Y %H:%M")
  log.INFO(f"Data convertida: {data_from_string}")
  assert data_from_string != None


def teste_salvar_data_mongodb(database):
  database.excluirColecao("teste_data_hora")
  str_data = "29.05.2019 23:30"
  data_from_string = datetime.strptime(str_data, "%d.%m.%Y %H:%M")

  datas = {"dataOriginal":str_data,
           "dataLocal": data_from_string,
           "dataUtc": dtu.converterHoraLocalToUtc(data_from_string)

           }
  resultado = database.inserirDocumento("teste_data_hora", datas)
  assert resultado is not None

def teste_obter_numero_mes():
  numeroMes = dtu.obterNumeroMes("Outubro")
  assert numeroMes == '10'