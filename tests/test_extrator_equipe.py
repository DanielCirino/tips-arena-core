from tipsarena_core.extratores.flash_score import navegador_web, extrator_equipe


def teste_extrair_lista_equipes_edicao_competicao(navegadorWeb):
  browser = navegador_web.obterNavegadorWeb()
  urlEdicao = f"{navegador_web.URL_BASE}/futebol/america-do-sul/copa-libertadores-2019/"
  browser.get(urlEdicao)

  lista = extrator_equipe.obterListaEquipesEdicaoCompeticao(navegadorWeb)

  assert navegadorWeb.finalizarNavegadorWeb()
  assert len(lista) == 32


def teste_extrair_dados_equipe():
  urlEquipe = "/equipe/liverpool/lId4TMwf/"
  dadosEquipe = extrator_equipe.obterDadosEquipe(urlEquipe)
  assert dadosEquipe["nome"] =="Liverpool"


if __name__ == '__main__':
  teste_extrair_dados_equipe()
