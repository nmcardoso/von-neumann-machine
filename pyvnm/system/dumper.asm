        ORG     208             @ carrega dumper após o loader
MAIN    LD      MEM_START       @ carrega posição inicial proveniente do loader
        SC      CREATE_LD       @ cria instrução LD para ler a posição inicial
        SC      EXEC_LD         @ executa a instrução LD
        SC      INC_CHECKSUM    @ incrementa checksum com os 2 bytes da posição
        SC      WRITE_BYTES     @ grava os bytes da posição inicial no disco
        LD      180             @ carrega número de bytes proveniente do loader
        SC      INC_CHECKSUM    @ incrementa checksum com o número de bytes
        PD      0x4             @ grava o byte menos signif. de N_BYES no disco
        SB      NUM_2           @ subtrai os 2 bytes de endereço
        SB      NUM_1           @ subtrai 1 byte de N_BYTES
        SB      NUM_1           @ subtrai 1 byte correspondente ao checksum
        ST      REMAINING_BYTES @ salva no contador de bytes restantes
        LD      182             @ carrega posição inicial proveninete do loader
        SC      CREATE_LD       @ cria função LD apontando para posição inicial
LOOP    SC      EXEC_LD         @ carrega conteúdo da posição de memória apontada
        SC      WRITE_BYTES     @ inicia o loop de escrita no disco
        SC      INC_CHECKSUM    @ incrementa o checksum
        LD      LD_INST         @ carrega instrução LD no acumulador
        AD      NUM_2           @ incrementa uma unidade
        ST      LD_INST         @ armazena novo valor na memória
        LD      REMAINING_BYTES @ carrega contador de bytes restantes
        SB      NUM_2           @ decrementa uma unidade do contador
        ST      REMAINING_BYTES @ armazena novo valor do contador na memória
        JZ      FINISH          @ sai do loop se contador for 0
        JP      LOOP            @ retorna ao loop caso contrário
FINISH  LD      CHECKSUM        @ carerga checksum
        ML      NUM_256         @ deslocamento lógico para esqueda de 8 bits
        DV      NUM_256         @ deslocamento lógico para direita de 8 bits
        ST      CHECKSUM_BYTE   @ salva o byte menos significativo do checksum
        LD      NUM_0           @ carrega 0 no acumulador
        SB      CHECKSUM_BYTE   @ calcula 0 - checksum
        PD      0x4             @ armazena complemento de 2 do byte checksum
        HJ      0               @ finaliza o programa
CREATE_LD                       @ subrotina: cria uma instrução LD dinamicamente
        ST      TMP             @ armazena valor de acc na posição temporária
        LD      OPCODE_LD       @ carrega opcode de LD
        ML      NUM_4096        @ deslocamento lógido para esquerda de 12 bits
        AD      TMP             @ insere valor do endereço, proveniente do acc
        ST      LD_INST         @ armazena instrução criada
        RS      CREATE_LD
EXEC_LD                         @ subrotina: executa instrução LD
LD_INST DATA    0x0             @ referência da inst. LD criada dinamicamente
        RS      EXEC_LD
WRITE_BYTES                     @ subrotina: escreve uma palavra no disco
        ST      TMP             @ armazena o valor da instrução atual
        DV      NUM_256         @ deslocamento lógico para direita de 8 bits
        PD      0x4             @ escreve o byte mais significativo no disco
        LD      TMP             @ carrega novamente a instrução atual
        PD      0x4             @ escreve o byte menos significativo no disco
        RS      WRITE_BYTES
INC_CHECKSUM                    @ subrotina: inc. checksum sem causar side-effect
        ST      TMP             @ armazena valor atual do acc
        AD      CHECKSUM        @ adicona o valor anterior do checksum ao acc
        ST      CHECKSUM        @ armazena novo valor do checksum
        LD      TMP             @ recarrega valor inicial do acc (evita SE)
        RS      INC_CHECKSUM
MEM_START       DATA    182     @ endereço onde o loader armazena a posição inicial do programa carregado
N_BYTES         DATA    180     @ endereço onde o loader armazena a quantidade de bytes do programa
REMAINING_BYTES DATA    0       @ contador de bytes restantes
CHECKSUM        DATA    0       @ acumulador checksum
CHECKSUM_BYTE   DATA    0       @ byte menos significativo do checksum
OPCODE_LD       DATA    8       @ constante valor do opcode da instrução LD
NUM_0           DATA    0       @ constante 0
NUM_1           DATA    1       @ constante 1
NUM_2           DATA    2       @ constante 2
NUM_256         DATA    256     @ constante 256 = 2^8
NUM_4096        DATA    4096    @ constante 4096 = 2^12
TMP             DATA    0       @ variavel de trabalho temporária
                END