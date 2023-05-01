        ORG     400      @ Define o endereço de início do programa
MAIN    GD      0b1      @ Aciona dispositivo de entrada (teclado) para obter um dado (valor 1) e armazena no acumulador
        ST      0x1      @ Armazena o valor do acumulador na posição de memória 0x1
        SB      0x1      @ Subtrai o valor armazenado na posição de memória 0x1 do conteúdo do acumulador
        AD      X        @ Soma o valor armazenado em X ao conteúdo do acumulador
        ST      0x2      @ Armazena o conteúdo do acumulador na posição de memória 0x2
        ST      0x3      @ Armazena o conteúdo do acumulador na posição de memória 0x3
        ST      0x4      @ Armazena o conteúdo do acumulador na posição de memória 0x4
LOOP    LD      0x1      @ Carrega o valor armazenado na posição de memória 0x1 no acumulador
        SB      0x3      @ Subtrai o valor armazenado na posição de memória 0x3 do conteúdo do acumulador
        JZ      ENDLP    @ Desvia para ENDLP se o conteúdo do acumulador for zero
        LD      0x4      @ Carrega o valor armazenado na posição de memória 0x4 no acumulador
        AD      Y        @ Soma o valor armazenado em Y ao conteúdo do acumulador
        ST      0x4      @ Armazena o conteúdo do acumulador na posição de memória 0x4
        AD      0x3      @ Soma o valor armazenado na posição de memória 0x3 ao conteúdo do acumulador
        ST      0x3      @ Armazena o conteúdo do acumulador na posição de memória 0x3
        LD      0x2      @ Carrega o valor armazenado na posição de memória 0x2 no acumulador
        AD      X        @ Soma o valor armazenado em X ao conteúdo do acumulador
        ST      0x2      @ Armazena o conteúdo do acumulador na posição de memória 0x2
        JP      LOOP     @ Desvia para LOOP
ENDLP   LD      0x2      @ Carrega o valor armazenado na posição de memória 0x2 no acumulador
        HJ      0x0      @ Para a execução do programa e desvia para o endereço 0x0
X       DATA    1
Y       DATA    2
        END      