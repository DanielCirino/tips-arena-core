from tipsarena_core.extratores.flash_score import extrator_pais


def teste_extracao_html_lista_paises():
  htmlPaises = extrator_pais.extrairHtmlPaises()
  assert htmlPaises is not None


if __name__ == '__main__':
  teste_extracao_html_lista_paises()
