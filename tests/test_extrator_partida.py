from tipsarena_core.extratores.flash_score import extrator_partida


def teste_extrair_html_partidas():
  url = "https://www.flashscore.com.br/futebol/brasil/serie-a/calendario/"
  htmlListaPartidas = extrator_partida.extrairHtmlPartidas(url)
  assert htmlListaPartidas.tipo == "PARTIDAS"


def teste_extrair_html_partidas_finalizadas_edicao_competicao():
  urlEdicao = "/futebol/brasil/campeonato-sergipano-2020/"
  htmlPartidasFinalizadas = extrator_partida.extrairHtmlPartidasEdicaoCompeticao(urlEdicao)
  assert htmlPartidasFinalizadas.tipo == "PARTIDAS"


def teste_extrair_html_partidas_agendadas_edicao_competicao():
  urlEdicao = "/futebol/brasil/serie-a-2020/"
  htmlPartidasAgendadas = extrator_partida.extrairHtmlPartidasEdicaoCompeticao(urlEdicao, finalizadas=False)
  assert htmlPartidasAgendadas.tipo == "PARTIDAS"


def teste_extrair_html_partidas_dia():
  htmlPartidas = extrator_partida.extrairHtmlPartidasDia()
  assert htmlPartidas is not None

def teste_extrair_html_partidas_dia_ontem():
  htmlPartidas = extrator_partida.extrairHtmlPartidasDia(-1)
  assert htmlPartidas is not None

def teste_extrair_html_partidas_dia_anteontem():
  htmlPartidas = extrator_partida.extrairHtmlPartidasDia(-2)
  assert htmlPartidas is not None

def teste_extrair_html_partidas_dia_amanha():
  htmlPartidas = extrator_partida.extrairHtmlPartidasDia(1)
  assert htmlPartidas is not None

def teste_extrair_html_partidas_dia_depois_de_amanha():
  htmlPartidas = extrator_partida.extrairHtmlPartidasDia(2)
  assert htmlPartidas is not None

def teste_extrair_dados_partida():
  dadosPartida = extrator_partida.obterDadosPartida("/jogo/2FgiFWv0/")

  assert dadosPartida is not None


def teste_extrair_estatisticas_partida():
  estatistiscas = extrator_partida.extrairEstatisticasPartida("/jogo/2FgiFWv0/")
  assert len(estatistiscas) == 15


if __name__ == '__main__':
  teste_extrair_html_partidas_dia_ontem()
