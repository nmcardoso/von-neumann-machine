import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from pyvnm.system.assembler import AbsoluteAssembler


def main():
  all_progs = Path(__file__).parent.glob('*.asm')
  for prog_path in all_progs:
    print(f'Montando programa {prog_path.name}')
    out_path = prog_path.parent / (prog_path.stem + '.hex')
    assembler = AbsoluteAssembler(program=prog_path, output_path=out_path, output_base='x')
    assembler.assemble()
    
    out_path = prog_path.parent / (prog_path.stem + '.bin')
    assembler = AbsoluteAssembler(program=prog_path, output_path=out_path, output_base='b')
    assembler.assemble()
  
  
if __name__ == '__main__':
  main()