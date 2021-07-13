from tipsarena_core.extratores.flash_score import extrator_partida


def teste_extrair_lista_ids_partida():
  listaIds = extrator_partida.obterListaIdsPartida("https://www.flashscore.com.br/futebol/brasil/serie-a/calendario/")

  assert len(listaIds) > 0


def teste_extrair_lista_ids_partida_edicao():
  listaPartidas = extrator_partida.obterListaPartidasEdicaoCompeticao("/futebol/brasil/campeonato-sergipano-2020/")
  listaConcatenada = listaPartidas["agendadas"] + listaPartidas["finalizadas"]
  assert len(listaConcatenada) > 0


def teste_extrair_lista_ids_partida_dia():
  listaPartidas = extrator_partida.obterListaPartidasDia()
  assert len(listaPartidas) > 0


def teste_extrair_dados_partida():
  dadosPartida = extrator_partida.obterDadosPartida("/jogo/2FgiFWv0/")

  assert dadosPartida is not None


def teste_extrair_estatisticas_partida():
  estatistiscas = extrator_partida.extrairEstatisticasPartida("/jogo/2FgiFWv0/")
  assert len(estatistiscas) == 15

if __name__ == '__main__':
  teste_extrair_estatisticas_partida()
