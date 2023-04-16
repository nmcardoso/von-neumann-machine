        ORG     0x5
MAIN    GD      0b1
        AD      5
        SB      3
        DV      4
        ML      2
        ST      0
        JP      LOOP
LOOP    SB      1
        JZ      ENDLP
        JP      LOOP
ENDLP   HJ      0x0
        END