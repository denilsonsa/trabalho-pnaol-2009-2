#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4 sw=4 et

import sys

import numpy
from numpy import array

numbolas = 180
raio = (
#   [ raio ] * quant  # <quant> bolas de <raio> cm
    [ 20.0 ] * 100 +
    [ 50.0 ] * 50  +
    [ 70.0 ] * 30
)


def f(x):
    """Função objetiva a ser minimizada, já incluindo as restrições.

    Esta função modela <numbolas> de raios diferentes a serem colocadas numa
    caixa. A caixa é definida pelos pontos C1 e C2, dois vértices opostos.
    Por modelagem, C1 está fixo em (0,0,0).

    O parâmetro x deve ser um array da seguinte forma:
    * O array deve conter números de ponto flutuante.
    * As dimensões devem ser (<numbolas> + 1, 3). Ou seja, x[i][0] é a
      coordenada X do i-ésimo elemento.
    * O primeiro elemento são as coordenadas X,Y,Z do vértice C2 da caixa.
    * Os <numbolas> elementos seguintes são as coordenadas X,Y,Z de cada
      uma das bolas.
    """
    area = 2 * (
        x[0][0] * x[0][1] +
        x[0][0] * x[0][2] +
        x[0][1] * x[0][2]
    )

    # TODO: adicionar custo das restrições
    #   | b_i - b_j |  >=  r_i + r_j  (para todo i,j)
    #   b_i - r_i  >= 0   (para todo i)
    #   b_i + r_i  <= C2  (para todo i)

    return area


def criar_um_chute_inicial():
    #x = numpy.zeros( shape=(numbolas+1, 3),  dtype=numpy.float64)
    x = numpy.empty( shape=(numbolas+1, 3),  dtype=numpy.float64)
    prev = 0.0
    for i, v in enumerate(x[1:]):
        v[0] = prev + raio[i]
        prev += 2*raio[i]
        v[1] = raio[i]
        v[2] = raio[i]
    x[0][0] = prev
    x[0][1] = max(raio)
    x[0][1] = max(raio)
    return x


def print_point(x, nome="", file=sys.stdout):
    opts = numpy.get_printoptions()
    numpy.set_printoptions(suppress=True, threshold=1000000)
    if nome:
        file.write("%s = %s\n" % (nome, repr(x)))
    else:
        file.write(repr(x) + "\n")
    numpy.set_printoptions(**opts)


def main():
    arquivo = open("points.txt", "w")
    arquivo.write("numbolas = " + str(numbolas) + "\n")
    arquivo.write("raio = " + repr(raio) + "\n")
    x = criar_um_chute_inicial()
    print f(x)
    print_point(x, file=arquivo)
    print_point(x/2, file=arquivo)
    print_point(x/2 + 2, file=arquivo)
    print_point(x + 2, file=arquivo)
    arquivo.close()

if __name__ == "__main__":
    main()
