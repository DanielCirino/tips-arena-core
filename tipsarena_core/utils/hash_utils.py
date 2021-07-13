# -*- coding: utf-8 -*-

import binascii
import hashlib


def gerarHash(texto: str):
  dk = hashlib.pbkdf2_hmac('sha256', texto.encode(), b'salt', 100000)
  str_hash = binascii.hexlify(dk)
  return str_hash.decode("utf-8")[:24]
