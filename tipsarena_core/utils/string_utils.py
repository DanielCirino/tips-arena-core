# -*- coding: utf-8 -*-

def limparString(texto: str):
  texto = texto.strip()
  texto = texto.replace("'", "''")
  texto = texto.replace("  ", "")
  texto = bytes(texto, 'utf-8').decode('utf-8', 'ignore')
  return texto
