import os

import pytest
from tipsarena_core.repository import mongodb
from tipsarena_core.extratores.flash_score import navegador_web
from tipsarena_core.services import log_service

os.environ["GD_ENV"] = 'DEV'


@pytest.fixture(scope="module")
def database():
  """
  Cria uma instância do cliente de banco de dados
  :return: um cliente de banco de dados
  """

  return mongodb

@pytest.fixture(scope="module")
def navegadorWeb():
  """
   Cria uma instância do navegador web
   :return: um navegador web
   """
  return navegador_web

@pytest.fixture(scope="module")
def log():
  """
   Cria uma instância do serviço de logs
   :return: uma instância do serviço de logs
   """
  return log_service
