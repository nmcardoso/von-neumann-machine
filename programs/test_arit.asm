        ORG     0x20
MAIN    LD      NUM_8   @ carrega o numero 8 no acumulador
        ST      4       @ guarda o número 8 na posição 4 da memória
        LD      NUM_2   @ carrega o número 2 no acumulador
        ST      5       @ guarda o número 2 na posição 5 da memória
        LD      NUM_0   @ carrega o número 0 no acumulador
        AD      NUM_8   @ soma o número 8 ao acumulador (Acc = 8)
        ST      7       @ guarda o resultado 8 na posiçao 7
        SB      NUM_2   @ subtrai o número 2 do acumulador (Acc = 6)
        ST      8       @ guarda o resultado 6 na posiçao 8
        DV      NUM_2   @ divide o valor do acumulador pelo número 2 (Acc = 3)
        ST      9       @ guarda o resultado 3 na posição 9
        ML      NUM_8   @ multiplica o acumulador pelo número 8 (Acc = 24(decimal) = 18(hexadecimal))
        ST      10      @ guarda o resultado 18 na posiçao 10 
NUM_0   DATA    0
NUM_2   DATA    2
NUM_8   DATA    8
        END