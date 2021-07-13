import os

from dotenv import load_dotenv

from tipsarena_core.services import log_service as log

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AMBIENTE = os.getenv('TA_ENV')
PATH_ARQUIVO_CONFIG = f"{ROOT_DIR}/.env.test"

if AMBIENTE is None:
  log.ALERTA("Variável de ambiente TA_ENV não existe.")
  AMBIENTE='DEV'

if AMBIENTE == 'PROD':
  PATH_ARQUIVO_CONFIG = f'{ROOT_DIR}/.env'

load_dotenv(PATH_ARQUIVO_CONFIG)
log.INFO("Ambiente:{}".format(os.getenv('TA_ENV')))

