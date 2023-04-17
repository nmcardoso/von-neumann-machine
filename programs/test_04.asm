        ORG     0x6
MAIN    GD      0b1
        ST      0x1
        SB      0x1
        AD      X
        ST      0x2
        ST      0x3
        ST      0x4
LOOP    LD      0x1
        SB      0x3
        JZ      ENDLP
        LD      0x4
        AD      Y
        ST      0x4
        AD      0x3
        ST      0x3
        LD      0x2
        AD      X
        ST      0x2
        JP      LOOP
ENDLP   LD      0x2
        HJ      0x0
X       DATA    1
Y       DATA    2
        END