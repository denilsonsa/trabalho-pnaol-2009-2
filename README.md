Trabalho de Programação Não Linear, 2009/2, [DCC/UFRJ][1], Prof. Luziane.

O objetivo do trabalho é achar uma solução para o problema de *empacotamento de bolas*. Dadas 180 bolas de tamanhos diferentes, encontrar uma disposição das bolas de modo que minimize a área da caixa que as contenha.

Foi implementado o método de otimização não-linear *busca coordenada* (ou *busca padrão usando as direções coordenadas*).

Sem restrição para o valor C2, o método não convergiu e reduziu as coordenadas de C2 de maneira irrestrita, chegando a coordenadas negativas e, por erro na fórmula inicial, à área negativa.

[1]: https://dcc.ufrj.br/
