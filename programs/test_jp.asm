        ORG      4      @ inicia carregamento na pos 4 da memória
MAIN    JZ       JP1    @ pula pra JP1 se acc = 0
        JP       JP2    @ pula pra JP2

JP1     LD       A      @ acc = 2
        PD       2      @ print 2
        JP       MAIN   @ pula para main

JP2     LD       ZERO   @ acc = 0
        PD       2      @ print 0
        HJ       0      @ termina o programa

ZERO    DATA     0 
A       DATA     2
        END