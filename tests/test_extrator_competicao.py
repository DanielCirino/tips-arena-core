import unittest

from tipsarena_core.extratores import extrator_competicao


def teste_extrair_competicoes_pais():
  urlPais = "/futebol/africa-do-sul/"
  listaCompeticoes = extrator_competicao.obterListaCompeticoesPais(urlPais)
  assert len(listaCompeticoes) > 0


def test_extrair_conteudo_competicao():
  urlCompeticao = "/futebol/africa-do-sul/primeira-liga/"
  dadosCompeticao = extrator_competicao.obterDadosCompeticao(urlCompeticao)
  assert dadosCompeticao is not None


def test_extrair_edicoes_competicao():
  urlCompeticao = "/futebol/eslovaquia/copa-da-eslovaquia/"
  listaEdicoes = extrator_competicao.obterListaEdicoesCompeticao(urlCompeticao)
  assert len(listaEdicoes) > 0


def test_extrair_edicao_recente_competicao():
  urlCompeticao = "/futebol/africa-do-sul/primeira-liga/"
  edicaoMaisRecente = extrator_competicao.obterEdicaoMaisRecenteCompeticao(urlCompeticao)
  assert edicaoMaisRecente != None


if __name__ == '__main__':
  test_extrair_conteudo_competicao()
