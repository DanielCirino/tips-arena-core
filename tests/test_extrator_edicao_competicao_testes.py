
from tipsarena_core.extratores import extrator_edicao_competicao


def teste_extrair_lista_edicoes_competicoes():
  urlCompeticao = "/futebol/alemanha/bundesliga/"
  listaEdicoes = extrator_edicao_competicao.obterListaEdicoesCompeticao(urlCompeticao)

  assert len(listaEdicoes) > 0


def teste_extrair_edicao_mais_recente_competicao():
  urlCompeticao = "/futebol/brasil/campeonato-paulista/"
  edicao = extrator_edicao_competicao.obterEdicaoMaisRecenteCompeticao(urlCompeticao)
  assert edicao is not None


def teste_extrair_dados_edicao_competicao():
  urlEdicao = "/futebol/brasil/campeonato-paulista-2019/"
  dadosEdicao = extrator_edicao_competicao.obterDadosEdicaoCompeticao(urlEdicao)
  assert dadosEdicao["ano"] == "2019"


if __name__ == '__main__':
  teste_extrair_dados_edicao_competicao ()
