            ORG       0x16          @ Subrotina chamando outra Subrotina
MAIN        SC        APRESENTACAO  @ imprime apresentacao
            HJ        0 
APRESENTACAO
            LD        CH_EOT
            PD        3
            LD        CH_T
            PD        3
            LD        CH_E
            PD        3
            LD        CH_S
            PD        3
            LD        CH_T
            PD        3
            LD        CH_E
            PD        3
            LD        CH_SP
            PD        3
            LD        CH_D
            PD        3
            LD        CH_E
            PD        3
            LD        CH_SP
            PD        3
            LD        CH_S
            PD        3
            LD        CH_U
            PD        3
            LD        CH_B
            PD        3
            LD        CH_R
            PD        3
            LD        CH_O
            PD        3
            LD        CH_T
            PD        3
            LD        CH_I
            PD        3
            LD        CH_N
            PD        3
            LD        CH_A
            PD        3
            LD        CH_EOT
            PD        3
            GD        1
            ST        NUM
            SC        RESPOSTA
            RS        APRESENTACAO
RESPOSTA
            LD        CH_EOT
            PD        3
            LD        CH_R
            PD        3
            LD        CH_E
            PD        3
            LD        CH_S
            PD        3
            LD        CH_P
            PD        3
            LD        CH_O
            PD        3
            LD        CH_S
            PD        3
            LD        CH_T
            PD        3
            LD        CH_A
            PD        3
            LD        CH_SP
            PD        3
            LD        CH_HP
            PD        3
            LD        CH_SP
            PD        3
            LD        NUM
            PD        2
            LD        CH_EOT
            PD        3
            RS        RESPOSTA

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
NUM         DATA      0
            END