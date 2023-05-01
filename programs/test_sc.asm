        ORG     400
MAIN    SC      FUNC_A  @ chama função A
        HJ      0x1     @ termina o programa

FUNC_A  
        SC      FUNC_B  @ chama função B
        LD      A       @ carrega valor 10 no acc
        PD      2       @ imprime valor 10
        RS      FUNC_A

FUNC_B  
        LD      B       @ carrega valor 20 no acc
        PD      2       @ imprime valor 20
        RS      FUNC_B

A       DATA    10
B       DATA    20
        END