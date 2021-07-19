# -*- coding: utf-8 -*-
from tipsarena_core.extratores.flash_score import extrator_competicao

def teste_extrair_html_competicoes_pais():
  urlPais = "/futebol/africa-do-sul/"
  htmlCompeticoesPais = extrator_competicao.extrairHtmlCompeticoesPais(urlPais)
  assert htmlCompeticoesPais is not None


def test_extrair_html_competicao():
  urlCompeticao = "/futebol/africa-do-sul/primeira-liga/"
  htmlCompeticao = extrator_competicao.extrairHtmlCompeticao(urlCompeticao)

  assert htmlCompeticao is not None


def test_extrair_html_edicoes_competicao():
  urlCompeticao = "/futebol/eslovaquia/copa-da-eslovaquia/"
  htmlEdicoes = extrator_competicao.extrairHtmlEdicoesCompeticao(urlCompeticao)
  assert htmlEdicoes is not None


if __name__ == '__main__':
  test_extrair_html_edicoes_competicao()
