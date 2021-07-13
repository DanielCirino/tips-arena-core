#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse

from extratores.MotorFactory import MotorFactory


def main():
    parser = argparse.ArgumentParser(prog='Tips Arena',
                                     description='Rotinas batch Tips Arena App')

    parser.add_argument('motor', type=int, help='Código do motor que será executado.')
    parser.add_argument('acao', type=int, help='Ação que será executada pelo motor.')
    parser.add_argument('threads', type=int, help='Quantidade de processos paralelos que serão executados.')

    args = parser.parse_args()

    # print(args);

    if args.motor == 0:
        print("\n===============================")
        parser.exit(0, "Informe o código do motor.\n")

        MotorFactory(args.motor, args.acao, 1)

        print("\n===============================")

    if args.motor != 0 and args.acao == 0:
        print("\n===============================")
        print("Informe a ação do motor.\n")

        MotorFactory(args.motor, args.acao, 1)

        print("\n===============================")
        parser.exit(0, "")

    MotorFactory(args.motor, args.acao, args.threads)


if __name__ == '__main__':
    main()

else:
    print('Móldulo não pode ser importado por outro módulo.')
