            ORG       0x0
MAIN_LOOP   SC        MENU          @ imprime menu de opções
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
MENU
            LD        CH_EOT
            PD        3
            LD        CH_1          @ 1 - Soma
            PD        3
            LD        CH_SP
            PD        3
            LD        CH_HP
            PD        3
            LD        CH_SP
            PD        3
            LD        CH_S
            PD        3
            LD        CH_O
            PD        3
            LD        CH_M
            PD        3
            LD        CH_A
            PD        3
            LD        CH_EOT
            PD        3
            LD        CH_2          @ 2 - Subtração
            PD        3
            LD        CH_SP
            PD        3
            LD        CH_HP
            PD        3
            LD        CH_SP
            PD        3
            LD        CH_S
            PD        3
            LD        CH_U
            PD        3
            LD        CH_B
            PD        3
            LD        CH_EOT
            PD        3
            LD        CH_3          @ 3 - Subtração
            PD        3
            LD        CH_SP
            PD        3
            LD        CH_HP
            PD        3
            LD        CH_SP
            PD        3
            LD        CH_M
            PD        3
            LD        CH_U
            PD        3
            LD        CH_L
            PD        3
            LD        CH_T
            PD        3
            LD        CH_EOT
            PD        3
            LD        CH_4          @ 4- Divisao
            PD        3
            LD        CH_SP
            PD        3
            LD        CH_HP
            PD        3
            LD        CH_SP
            PD        3
            LD        CH_D
            PD        3
            LD        CH_I
            PD        3
            LD        CH_V
            PD        3
            LD        CH_I
            PD        3
            LD        CH_S
            PD        3
            LD        CH_A
            PD        3
            LD        CH_O
            PD        3
            LD        CH_EOT
            PD        3
            LD        CH_5          @ 5 - Sair
            PD        3
            LD        CH_SP
            PD        3
            LD        CH_HP
            PD        3
            LD        CH_SP
            PD        3
            LD        CH_S
            PD        3
            LD        CH_A
            PD        3
            LD        CH_I
            PD        3
            LD        CH_R
            PD        3
            LD        CH_EOT
            PD        3
            RS        MENU

CH_A        DATA      0cA
CH_B        DATA      0cB
CH_C        DATA      0cC
CH_D        DATA      0cD
CH_E        DATA      0cE
CH_F        DATA      0cF
CH_G        DATA      0cG
CH_H        DATA      0cH
CH_I        DATA      0cI
CH_J        DATA      0cJ
CH_L        DATA      0cL
CH_M        DATA      0cM
CH_N        DATA      0cN
CH_O        DATA      0cO
CH_P        DATA      0cP
CH_Q        DATA      0cQ
CH_R        DATA      0cR
CH_S        DATA      0cS
CH_T        DATA      0cT
CH_U        DATA      0cU
CH_V        DATA      0cV
CH_X        DATA      0cX
CH_Z        DATA      0cZ
CH_SP       DATA      32
CH_0        DATA      0c0
CH_1        DATA      0c1
CH_2        DATA      0c2
CH_3        DATA      0c3
CH_4        DATA      0c4
CH_5        DATA      0c5
CH_6        DATA      0c6
CH_7        DATA      0c7
CH_8        DATA      0c8
CH_9        DATA      0c9
CH_HP       DATA      45
CH_EOT      DATA      4
OP_1        DATA      0
OP_2        DATA      0
OPT         DATA      0
SUM_CODE    DATA      1
SUB_CODE    DATA      2
MUL_CODE    DATA      3
DIV_CODE    DATA      4
EXT_CODE    DATA      5
            END