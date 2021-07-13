
# -*- coding: utf-8 -*-

import binascii
import hashlib


class HashString():

    def encode(self, text: str):
        dk = hashlib.pbkdf2_hmac('sha256', text.encode(), b'salt', 100000)
        str_hash = binascii.hexlify(dk)
        return str_hash.decode("utf-8")[:24]
