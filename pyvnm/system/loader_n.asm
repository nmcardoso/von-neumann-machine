@ este programa não funciona
          ORG     0
INICIO    GD      4           @ lê um byte do arquivo
          LD      MEM_POS
          GD      4
          LD      PROG_LEN
          JP      LOAD_LP
LOAD_LP   LD      DIFF
          JZ      END_LP
          GD      4
          PD      4

          LD      CI
          AD      ONE
          ST      CI
          SB      PROG_LEN
          ST      DIFF
END_LP    HJ      0

DATA      ONE       1
DATA      MEM_START 300
DATA      PROG_LEN  0
DATA      CI        0
DATA      DIFF      0
          END