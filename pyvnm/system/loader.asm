            ORG     0
MAIN        LD      NUM_0
            ST      CHECK_SUM_CALCULADO
            GD      0x4                     @ lê o primeiro byte da fita 
            ST      PRIMEIRO_BYTE           @ PRIMEIRO_BYTE = endereço da memória onde ficará guardada o valor da variável PRIMEIRO_BYTE
            SC      SOMA_CHECK_SUM          @ 
            GD      0x4                     @ lê o segundo byte da fita
            ST      SEGUNDO_BYTE            @ SEGUNDO_BYTE = endereço da memória onde ficará guardada o valor da variável SEGUNDO_BYTE
            SC      SOMA_CHECK_SUM
            SC      CONCATENA_BYTES         @ chama a subrotina concatena instruçao longa
            LD      WORD
            ST      INICIO_MEMORIA          @ INICIO_MEMORIA = endereço da memória onde ficara guardado o endereço de inicio de gravaçao na memória
            GD      0x4                     @ lê o terceiro byte da fita
            ST      BYTES_TOTAIS            @ BYTES_TOTAIS = enderço da memória onde ficará guardada a quantidade total de bytes da fita
            SC      SOMA_CHECK_SUM
            LD      BYTES_TOTAIS            @ 
            SB      NUM_4                   @
            ST      BYTES_RESTANTES         @ BYTES_RESTANTES = 
            SC      CRIA_INSTRUCAO
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
            SC      CONCATENA_BYTES
            LD      WORD
            SC      GRAVA_INSTRUCAO
            JP      LOOP
END_LOOP    GD      0x4
            ST      CHECK_SUM_FORNECIDO
            LD      CHECK_SUM_CALCULADO
            ML      NUM_256                     @ ---
            DV      NUM_256                     @ com essa multiplicação e essa divisao eu pego os 8 bits menos significativos      
            AD      CHECK_SUM_FORNECIDO         @ o checksum fornecido estará em complemento de 2, por isso a adição funciona
            ML      NUM_256
            DV      NUM_256
            HJ      0x0
GRAVA_INSTRUCAO
INSTRUCAO   DATA    0
            SC      INC_INSTRUCAO
            RS      GRAVA_INSTRUCAO
CONCATENA_BYTES
            LD      PRIMEIRO_BYTE
            ML      NUM_256          @ multiplica por 256=2^8, equivalente a 8 shift left
            AD      SEGUNDO_BYTE
            ST      WORD
            RS      CONCATENA_BYTES
CRIA_INSTRUCAO
            LD      OPCODE_ST
            ML      NUM_4096
            AD      INICIO_MEMORIA
            ST      INSTRUCAO
            RS      CRIA_INSTRUCAO
INC_INSTRUCAO
            LD      INSTRUCAO
            AD      NUM_2
            ST      INSTRUCAO
            RS      INC_INSTRUCAO
DEC_BYTES_RESTANTES
            LD      BYTES_RESTANTES
            SB      NUM_1
            ST      BYTES_RESTANTES
            RS      DEC_BYTES_RESTANTES
SOMA_CHECK_SUM
            AD      CHECK_SUM_CALCULADO
            ST      CHECK_SUM_CALCULADO
            RS      SOMA_CHECK_SUM
ERRO_DE_CHECK_SUM
            OS      600
            RS      ERRO_DE_CHECK_SUM
NUM_0       DATA    0
NUM_1       DATA    1
NUM_2       DATA    2
NUM_4       DATA    4
NUM_256     DATA    256
NUM_4096    DATA    4096
OPCODE_ST   DATA    9
CHECK_SUM_CALCULADO DATA 0
CHECK_SUM_FORNECIDO DATA 0
PRIMEIRO_BYTE DATA 0
SEGUNDO_BYTE DATA 0
BYTES_TOTAIS DATA 0
BYTES_RESTANTES DATA 0
WORD DATA 0
INICIO_MEMORIA DATA 0
            END