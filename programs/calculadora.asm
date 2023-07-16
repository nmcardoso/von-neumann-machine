            ORG       400
            EXT       CALC_MENU
MAIN_LOOP   SC        CALC_MENU     @ imprime menu de opções
            GD        1             @ pergunta opção
            ST        OPT           @ salva opção
            SB        SUM_CODE      @ compara com cod de soma
            JZ        SOMA          @ executa soma se acc=0
            LD        OPT           @ carrega opção
            SB        SUB_CODE      @ compara com cod de sub
            JZ        SUBTR         @ executa sub se acc=0
            LD        OPT           @ carrega opção
            SB        MUL_CODE      @ compara com cod de mult
            JZ        MULT          @ executa mult se acc=0
            LD        OPT           @ carrega opção
            SB        DIV_CODE      @ compara com cod de div
            JZ        DIVISAO       @ executa div se acc=0
            LD        OPT           @ carrega opção
            SB        EXT_CODE      @ compara com cod de div
            JZ        END_LOOP      @ sai se acc=0
END_LOOP    HJ        0             @ sai do loop
SOMA        SC        READ_OP       @ lê os operandos
            AD        OP_2          @ executa adição
            PD        2             @ exibe o resultado
            JP        MAIN_LOOP     @ retorna para loop pricipal
SUBTR       SC        READ_OP       @ lê os operandos
            SB        OP_2          @ executa subtração
            PD        2             @ exibe o resultado
            JP        MAIN_LOOP     @ retorna para loop pricipal
MULT        SC        READ_OP       @ lê os operandos
            ML        OP_2          @ executa multiplicação
            PD        2             @ exibe o resultado
            JP        MAIN_LOOP     @ retorna para loop pricipal
DIVISAO     SC        READ_OP       @ lê os operandos
            DV        OP_2          @ executa divisao
            PD        2             @ exibe o resultado
            JP        MAIN_LOOP     @ retorna para loop pricipal
READ_OP                             @ lê os operandos
            GD        1             @ lê o primeiro operando
            ST        OP_1          @ armazena o 1. op da memoria
            GD        1             @ lê o segundo operando   
            ST        OP_2          @ armazena o 2. op da memoria
            LD        OP_1          @ carrega o 1. op no acumulador
            RS        READ_OP       @ retorna


OP_1        DATA      0
OP_2        DATA      0
OPT         DATA      0
SUM_CODE    DATA      1
SUB_CODE    DATA      2
MUL_CODE    DATA      3
DIV_CODE    DATA      4
EXT_CODE    DATA      5
            END