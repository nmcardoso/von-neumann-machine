        ORG     400
MAIN    LD      NUM_8   @ carrega o numero 8 no acumulador
        ST      A       @ guarda o número 8 na posição A da memória
        LD      NUM_2   @ carrega o número 2 no acumulador
        ST      B       @ guarda o número 2 na posição B da memória
        LD      NUM_0   @ carrega o número 0 no acumulador
        AD      NUM_8   @ soma o número 8 ao acumulador (Acc = 8)
        ST      C       @ guarda o resultado 8 na posiçao C
        SB      NUM_2   @ subtrai o número 2 do acumulador (Acc = 6)
        ST      D       @ guarda o resultado 6 na posiçao D
        DV      NUM_2   @ divide o valor do acumulador pelo número 2 (Acc = 3)
        ST      E       @ guarda o resultado 3 na posição E
        ML      NUM_8   @ multiplica o acumulador pelo número 8 (Acc = 24(decimal) = 18(hexadecimal))
        ST      F      @ guarda o resultado 18 na posiçao F 
        HJ      0x0     @ termina execução
NUM_0   DATA    0
NUM_2   DATA    2
NUM_8   DATA    8
A       DATA    0
B       DATA    0
C       DATA    0
D       DATA    0
E       DATA    0
F       DATA    0
        END