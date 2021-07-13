from tipsarena_core.extratores.flash_score import extrator_edicao_competicao


def teste_extrair_html_edicao_competicao():
  urlEdicao = "/futebol/brasil/campeonato-paulista-2019/"
  htmlEdicao = extrator_edicao_competicao.extrairHtmlEdicaoCompeticao(urlEdicao)
  assert htmlEdicao is not None


if __name__ == '__main__':
  teste_extrair_html_edicao_competicao ()
