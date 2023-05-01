        ORG     400
MAIN    GD      0b1
        AD      X
        SB      Y
        DV      Z
        ML      A
        ST      0
        JP      LOOP
LOOP    SB      B
        JZ      ENDLP
        JP      LOOP
ENDLP   HJ      0x0

X       DATA    5
Y       DATA    3
Z       DATA    4
A       DATA    2
B       DATA    1
        END