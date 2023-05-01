        ORG      0x160
MAIN    LD       A      @ carrega dado de A no acumulador
        ST       B      @ armazena valor carregado na memoria
        PD       3      @ adiciona letra P ao buffer do Monitor
        GD       1      @ guarda valor do teclado no acumulador
        PD       2      @ exibe valor do acc no Monitor
        PD       3      @ adiciona letra C ao buffer do Monitor
        LD       C      @ carrega conteúdo de C no acumulador
        PD       3      @ adiciona letra S ao buffer do Monitor
        LD       EOT    @ carrega caractere de controle EOT no acc
        PD       3      @ envia EOT para monitor e encerra stream
        HJ       0

A       DATA     80
B       DATA     1
C       DATA     83
EOT     DATA     4
        END