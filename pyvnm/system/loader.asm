                    
            ORG     0
MAIN        LD      NUM_1                   @
            ST      POSICAO_ARQUIVO         @ POSICAO_ARQUIVO = endereço da memória onde ficará guardado o valor da variável que varre os bytes do arquivo

            RD      POSICAO_ARQUIVO         @ lê o primeiro byte da fita (POSICAO = 1) 
            ST      PRIMEIRO_BYTE           @ PRIMEIRO_BYTE = endereço da memória onde ficará guardada o valor da variável PRIMEIRO_BYTE
            ST      CHECK_SUM_CALCULADO

            LD      POSICAO_ARQUIVO         @ carrego no acumulador 
            AD      NUM_1                   @ avança para o próximo byte
            ST      POSICAO_ARQUIVO         @

            RD      POSICAO_ARQUIVO         @ lê o segundo byte da fita (POSICAO = 2)
            ST      SEGUNDO_BYTE            @ SEGUNDO_BYTE = endereço da memória onde ficará guardada o valor da variável SEGUNDO_BYTE
            LD      CHECK_SUM_CALCULADO
            AD      SEGUNDO_BYTE
            ST      CHECK_SUM_CALCULADO

            SC      CONCATENA_INSTRU_LONGA  @ chama a subrotina concatena instruçao longa
            LD      INSTRU_LONGA
            ST      INICIO_MEMORIA          @ INICIO_MEMORIA = endereço da memória onde ficara guardado o endereço de inicio de gravaçao na memória

            LD      POSICAO_ARQUIVO
            AD      NUM_1
            ST      POSICAO_ARQUIVO

            RD      POSICAO_ARQUIVO         @ lê o terceiro byte da fita (POSICAO = 3)
            ST      BYTES_TOTAIS            @ BYTES_TOTAIS = enderço da memória onde ficará guardada a quantidade total de bytes da fita
            LD      CHECK_SUM_CALCULADO
            AD      BYTES_TOTAIS
            ST      CHECK_SUM_CALCULADO

            LD      BYTES_TOTAIS            @ 
            SB      NUM_3                   @
            ST      BYTES_CODIGO            @ BYTES_CODIGO = endereço da memória onde ficará guardada a quantidade de bytes referente ao programa

            LD      INICIO_MEMORIA
            ST      POSICAO_MEMORIA

            LD      POSICAO_ARQUIVO         @ -
            AD      NUM_1                   @ preparação para entrar no loop (posiciona no próximo byte da fita a ser lido)
            ST      POSICAO_ARQUIVO         @ -

LOOP        LD      BYTES_TOTAIS
            SB      POSICAO_ARQUIVO
            SB      NUM_1
            JZ      END_LOOP

            RD      POSICAO_ARQUIVO                       
            ST      PRIMEIRO_BYTE
            LD      CHECK_SUM_CALCULADO
            AD      PRIMEIRO_BYTE
            ST      CHECK_SUM_CALCULADO                 
            LD      POSICAO_ARQUIVO                       
            AD      NUM_1                         
            ST      POSICAO_ARQUIVO                       
            RD      POSICAO_ARQUIVO                       
            ST      SEGUNDO_BYTE
            LD      CHECK_SUM_CALCULADO
            AD      SEGUNDO_BYTE
            ST      CHECK_SUM_CALCULADO                  
            SC      CONCATENA_INSTRU_LONGA        
            LD      INSTRU_LONGA
            ST      POSICAO_MEMORIA

            LD      POSICAO_MEMORIA
            AD      NUM_1
            ST      POSICAO_MEMORIA

            LD      POSICAO_ARQUIVO
            AD      NUM_1
            ST      POSICAO_ARQUIVO

            JP      LOOP

END_LOOP    RD      POSICAO_ARQUIVO             @ nessa posiçao o valor guardado em POSICAO_ARQUIVO deve ser igual ao valor guardado em BYTES_TOTAIS
            ST      CHECK_SUM_FORNECIDO
            LD      CHECK_SUM_CALCULADO
            ML      NUM_256                     @ ---
            DV      NUM_256                     @ com essa multiplicação e essa divisao eu pego os 8 bits menos significativos      
            AD      CHECK_SUM_FORNECIDO         @ o checksum fornecido estará em complemento de 2, por isso a adição funciona
            ML      NUM_256
            DV      NUM_256
            JZ      END
            SC      ERRO_DE_CHECK_SUM

CONCATENA_INSTRU_LONGA
            LD      PRIMEIRO_BYTE
            ML      NUM_256          @ multiplica por 256=2^8, equivalente a 8 shift left
            AD      SEGUNDO_BYTE
            ST      INSTRU_LONGA
            RS      CONCATENA_INSTRU_LONGA

ERRO_DE_CHECK_SUM
            ...
            RS      ERRO_DE_CHECK_SUM

POSICAO_ARQUIVO     DATA 98
POSICAO_MEMORIA     DATA 99
PRIMEIRO_BYTE       DATA 100
SEGUNDO_BYTE        DATA 101
INSTRU_LONGA        DATA 102
INICIO_MEMORIA      DATA 103
BYTES_TOTAIS        DATA 104
BYTES_CODIGO        DATA 105
CHECK_SUM_FORNECIDO DATA 106
CHECK_SUM_CALCULADO DATA 107
NUM_1               DATA 1
NUM_3               DATA 3
NUM_256             DATA 256