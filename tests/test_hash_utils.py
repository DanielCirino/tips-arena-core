# -*- coding: utf-8 -*-

from tipsarena_core.utils import hash_utils as hash


def teste_hash_string_iguais():
  h1 = (hash.gerarHash("/futebol/africa-do-sul/"))
  h1_teste = (hash.gerarHash("/futebol/africa-do-sul/"))

  assert h1 == h1_teste


def teste_hash_string_diferentes():
  h3 = (hash.gerarHash("/futebol/africa-do-sul/primeira-liga/"))
  h3_teste = (hash.gerarHash(
    "/futebol/africa-do-sul/primeira-liga"))

  assert h3 != h3_teste
