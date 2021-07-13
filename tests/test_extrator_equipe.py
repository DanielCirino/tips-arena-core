from tests.conftest import navegadorWeb
from tipsarena_core.extratores.flash_score import navegador_web, extrator_equipe


def teste_extrair_html_equipes_edicao_competicao():
  urlEdicao = "/futebol/brasil/serie-a-2019/"
  htmlEquipes = extrator_equipe.extrairHtmlEquipesEdicaoCompeticao(urlEdicao)

  assert htmlEquipes is not None


def teste_extrair_dados_equipe():
  urlEquipe = "/equipe/liverpool/lId4TMwf/"
  htmlEquipe = extrator_equipe.extrairHtmlEquipe(urlEquipe)
  assert htmlEquipe is not None


if __name__ == '__main__':
  teste_extrair_html_equipes_edicao_competicao()
