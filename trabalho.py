#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4 sw=4 et

import sys

import numpy
from numpy import array

numbolas = 180
raio = array(
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

    Esta função retorna uma tupla com três elementos:
    * total - é o custo, ou a imagem, correspondente ao ponto x
    * num_colisoes - quantidade de colisões detectadas
    * num_bordas - quantidade de bolas cruzando a borda da caixa
    De maneira geral, apenas o "total" é importante. Os outros dois valores
    são retornados apenas para fins informativos.
    """

    area = 2 * (
        x[0][0] * x[0][1] +
        x[0][0] * x[0][2] +
        x[0][1] * x[0][2]
    )

    # Restrição:
    #   | b_i - b_j |  >=  r_i + r_j  (para todo i,j)
    # ou seja:
    #   r_i + r_j - | b_i - b_j | <= 0
    num_colisoes = 0
    colisoes = 0.0
    for i in range(1, numbolas+1):
        for j in range(i+1, numbolas+1):
            delta = x[i]-x[j]
            dist = numpy.dot(delta, delta)  # quadrado da norma do vetor
            penalidade = raio[i-1] + raio[j-1] - dist
            if penalidade > 0.0:
                colisoes += penalidade
                num_colisoes += 1

    # Restrições:
    #   b_i - r_i  >= 0   (para todo i)
    #   b_i + r_i  <= C2  (para todo i)
    # ou seja:
    #  -b_i + r_i     <= 0
    #   b_i + r_i -C2 <= 0
    num_bordas = 0
    bordas = 0.0
    for i in range(1, numbolas+1):
        penalidade = 0.0
        for j in range(3):  # x,y,z
            penalidade += max(0.0, -x[i][j] + raio[i-1])
            penalidade += max(0.0,  x[i][j] + raio[i-1] - x[0][j])
        if penalidade > 0.0:
            bordas += penalidade
            num_bordas += 1

    total = area + colisoes + bordas

    return (total, num_colisoes, num_bordas)


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
    x[0][1] = 2*max(raio)
    x[0][2] = 2*max(raio)
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
    arquivo.write("raio = " + repr(list(raio)) + "\n")
    x = criar_um_chute_inicial()
    print f(x)
    print_point(x, file=arquivo)
    print_point(x/2, file=arquivo)
    print_point(x/2 + 20, file=arquivo)
    print_point(x + 20, file=arquivo)
    arquivo.close()

if __name__ == "__main__":
    main()
