            ORG     0
MAIN        LD      NUM_0
            ST      CHECK_SUM_CALCULADO
            GD      0x4                     @ lê o primeiro byte da fita 
            ST      PRIMEIRO_BYTE           @ PRIMEIRO_BYTE = endereço da memória onde ficará guardada o valor da variável PRIMEIRO_BYTE
            SC      SOMA_CHECK_SUM          @ 
            GD      0x4                     @ lê o segundo byte da fita
            ST      SEGUNDO_BYTE            @ SEGUNDO_BYTE = endereço da memória onde ficará guardada o valor da variável SEGUNDO_BYTE
            SC      SOMA_CHECK_SUM
            SC      CONCATENA_INSTRU_LONGA  @ chama a subrotina concatena instruçao longa
            LD      INSTRU_LONGA
            ST      INICIO_MEMORIA          @ INICIO_MEMORIA = endereço da memória onde ficara guardado o endereço de inicio de gravaçao na memória

            GD      0x4                     @ lê o terceiro byte da fita
            ST      BYTES_TOTAIS            @ BYTES_TOTAIS = enderço da memória onde ficará guardada a quantidade total de bytes da fita
            SC      SOMA_CHECK_SUM

            LD      BYTES_TOTAIS            @ 
            SB      NUM_3                   @
            ST      BYTES_RESTANTES         @ BYTES_RESTANTES = 

            LD      ST_OC
            ML      NUM_4096
            AD      INICIO_MEMORIA
            ST      INSTRUCAO

LOOP        LD      BYTES_RESTANTES
            JZ      END_LOOP
            GD      0x4
            ST      PRIMEIRO_BYTE
            SC      SOMA_CHECK_SUM
            SC      DEC_BYTES_RESTANTES
            GD      0x4
            ST      SEGUNDO_BYTE
            SC      SOMA_CHECK_SUM
            SC      DEC_BYTES_RESTANTES
            SC      CONCATENA_INSTRU_LONGA
            LD      INSTRU_LONGA
            SC      GRAVA_INSTRUCAO
            JP      LOOP
END_LOOP    
            GD      0x4
            ST      CHECK_SUM_FORNECIDO
            LD      CHECK_SUM_CALCULADO
            ML      NUM_256                     @ ---
            DV      NUM_256                     @ com essa multiplicação e essa divisao eu pego os 8 bits menos significativos      
            AD      CHECK_SUM_FORNECIDO         @ o checksum fornecido estará em complemento de 2, por isso a adição funciona
            ML      NUM_256
            DV      NUM_256
            JZ      FIM
            SC      ERRO_DE_CHECK_SUM

ERRO_DE_CHECK_SUM
            OS      0x0
            RS      ERRO_DE_CHECK_SUM

GRAVA_INSTRUCAO
INSTRUCAO
            SC      INC_INSTRUCAO
            RS      GRAVA_INSTRUCAO

CONCATENA_INSTRU_LONGA
            LD      PRIMEIRO_BYTE
            ML      NUM_256          @ multiplica por 256=2^8, equivalente a 8 shift left
            AD      SEGUNDO_BYTE
            ST      INSTRU_LONGA
            RS      CONCATENA_INSTRU_LONGA

DEC_BYTES_RESTANTES
            LD      BYTES_RESTANTES
            SB      NUM_1
            ST      BYTES_RESTANTES
            RS      DEC_BYTES_RESTANTES

INC_INSTRUCAO
            LD      INSTRUCAO
            AD      NUM_1
            ST      INSTRUCAO
            RS      INC_INSTRUCAO

SOMA_CHECK_SUM
            AD      CHECK_SUM_CALCULADO
            ST      CHECK_SUM_CALCULADO
            RS      SOMA_CHECK_SUM

FIM         HJ      0x0

NUM_0       DATA    0
NUM_1       DATA    1
NUM_3       DATA    3
NUM_256     DATA    256
NUM_4096    DATA    4096
ST_OC       DATA    9

CHECK_SUM_CALCULADO
CHECK_SUM_FORNECIDO
PRIMEIRO_BYTE
SEGUNDO_BYTE
INSTRU_LONGA
INICIO_MEMORIA
BYTES_TOTAIS
BYTES_RESTANTES
            END