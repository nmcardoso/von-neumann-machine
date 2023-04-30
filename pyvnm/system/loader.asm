            ORG     0
MAIN        LD      NUM_0
            ST      CHECK_SUM_CALCULADO     @ zera o check_sum_calculado
            GD      0x4                     @ le o primeiro byte da fita 
            ST      PRIMEIRO_BYTE           @ guarda o primeiro byte para concatena-lo
            SC      SOMA_CHECK_SUM          @ soma o byte lido ao check_sum
            GD      0x4                     @ le o segundo byte da fita
            ST      SEGUNDO_BYTE            @ guarda o segundo byte para concatena-lo
            SC      SOMA_CHECK_SUM          @ soma o byte lido ao check_sum
            SC      CONCATENA_BYTES         @ chama a subrotina que concatena dois bytes
            LD      WORD                    @ carrega os dois bytes concatenados
            ST      INICIO_MEMORIA          @ guarda o endereco de inicio de gravacao na memoria em INICIO_MEMORIA
            GD      0x4                     @ le o terceiro byte da fita
            ST      BYTES_TOTAIS            @ guarda a quantidade total de bytes da fita em BYTES_TOTAIS
            SC      SOMA_CHECK_SUM          @ soma o byte lido ao check_sum
            LD      BYTES_TOTAIS             
            SB      NUM_4                    
            ST      BYTES_RESTANTES         @ guarda a quantidade de bytes restantes referentes ao codigo a ser carregado 
            SC      CRIA_INSTRUCAO          @ subrotina que cria a instrucao de gravacao que sera incrementada a cada gravacao na memoria
LOOP        LD      BYTES_RESTANTES
            JZ      END_LOOP                @ verifica se e o final do arquivo
            GD      0x4                     @ le um byte do programa
            ST      PRIMEIRO_BYTE           @ guarda o byte para ser concatenado
            SC      SOMA_CHECK_SUM          @ soma o byte lido ao check_sum
            SC      DEC_BYTES_RESTANTES     @ decrementa a quantidade de bytes restantes
            GD      0x4                     @ le o proximo byte
            ST      SEGUNDO_BYTE            @ guarda o byte para ser concatenado
            SC      SOMA_CHECK_SUM          @ soma o byte lido ao check_sum
            SC      DEC_BYTES_RESTANTES     @ decrementa a quantidade de bytes restantes
            SC      CONCATENA_BYTES         @ chama a subrotina que concatena dois bytes
            LD      WORD                    @ carrega os dois bytes concatenados
            SC      GRAVA_INSTRUCAO         @ subrotina que grava os dois bytes lidos na memoria
            JP      LOOP                    @ pula pro inincio do loop
END_LOOP    GD      0x4                     @ le o byte do check_sum do arquivo
            ST      CHECK_SUM_FORNECIDO     @ guarda o byte de check_sum fornecido no arquivo
            LD      CHECK_SUM_CALCULADO     @ carrega o check_sum calculado ao longo da leitura do arquivo
            ML      NUM_256                 @ ---
            DV      NUM_256                 @ com essa multiplicacao e essa divisao eu pego os 8 bits menos significativos      
            AD      CHECK_SUM_FORNECIDO     @ o checksum fornecido estara em complemento de 2, por isso a adicao zera o resultado
            ML      NUM_256                 @ ---
            DV      NUM_256                 @ com essa multiplicacao e essa divisao eu pego os 8 bits menos significativos
            JZ      FIM                     @ pula para fim se o check_sum estiver OK
            SC      ERRO_DE_CHECK_SUM       @ chama a subrotina q identifica o erro de check_sum
FIM         HJ      0x0                     @ para a maquina
GRAVA_INSTRUCAO
INSTRUCAO   DATA    0
            SC      INC_INSTRUCAO
            RS      GRAVA_INSTRUCAO
CONCATENA_BYTES
            LD      PRIMEIRO_BYTE
            ML      NUM_256                 @ multiplica por 256=2^8, equivalente a 8 shift left
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
            OS      400
            OS      5
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
BYTES_RESTANTES DATA 0
WORD DATA 0
BYTES_TOTAIS DATA 0
INICIO_MEMORIA DATA 0
            END