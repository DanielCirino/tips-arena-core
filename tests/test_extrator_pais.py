import os

from tipsarena_core.extratores.flash_score import extrator_pais


def teste_extracao_html_lista_paises():
  htmlPaises = extrator_pais.extrairHtmlPaises()
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS')}{htmlPaises.nomeArquivo}"
  with open(caminhoArquivo, mode="w") as arquivo:
    arquivo.write(htmlPaises.html)

  assert os.path.isfile(caminhoArquivo)


if __name__ == '__main__':
  teste_extracao_html_lista_paises()
