import pathlib
from tipsarena_core.parsers_html.flash_score import parser_competicao


def teste_parser_html_competicao():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_competicao.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    dadosCompeticao = parser_competicao.processarHtmlCompeticao(html)
    assert dadosCompeticao["nome"] == 'Premier League'


def teste_parser_html_competicoes_pais():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_competicoes_pais.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    listaCompeticoes = parser_competicao.processarHtmlCompeticoesPais(html)
    assert len(listaCompeticoes) >= 7

def teste_parser_html_edicoes_competicoes():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_edicoes_competicao.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    listaEdicoes = parser_competicao.processarHtmlEdicoesCompeticao(html)
    assert len(listaEdicoes) >= 23

if __name__ == "__main__":
  teste_parser_html_edicoes_competicoes()
