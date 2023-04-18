import argparse
from pathlib import Path

from .vm.memory import Memory
from .vm.state import MachineState
from .vm.vnm import VonNeumannMachine


class Colors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'



def heading(msg: str, sep: str = '-'):
    """
    Função auxiliar: exibe uma mensagem no terminal com uma regua abaixo
    do mesmo tamanho da mensagem
    Parameters
    ----------
    msg: str
      mensagem a ser exibida
    sep: str
      caractere de separação
    """
    print(msg)
    print(sep*len(msg))
    
    
    
def hexdump(mem: Memory):
  for i in range(mem.size // 16):
    print(Colors.WARNING + format(i*16, '0>4x') + Colors.ENDC, ' ', sep='', end='')
    for j in range(16):
      w = mem.read(i*16 + j)
      if w.value is None:
        print(format(0, '0>4x'), ' ', sep='', end='')
      else:
        print(Colors.BOLD + Colors.OKGREEN + format(w.value, '0>4x') + Colors.ENDC, ' ', sep='', end='')
    print()
    
    
    
def show_registers(state: MachineState):
  print('Acumulador:\t', format(state.acc.value or 0, '0>4x'))
  print('PC:\t\t', format(state.pc.value or 0, '0>4x'))


def cli():
  p = argparse.ArgumentParser(prog='Simulador da Maquina de Von Neumann')
  p.add_argument(
    'programa', 
    nargs=1,
    action='store', 
    help='Caminho relativo ou absoluto do programa a ser executado'
  )
  p.add_argument(
    '-m', 
    action='store',
    default=4096,
    help='Número de posições na memória. Padrão: 4096'
  )
  args = p.parse_args()
  return args
  


def main():
  # vnm = VonNeumannMachine(memory_size=128)
  # test_file = Path(__file__).parent.parent / 'programs' / 'test_02.hex'
  # vnm.execute_program(test_file)
  args = cli()
  
  program_path = Path(args.programa[0])
  if not program_path.exists():
    return print(f'Arquivo não encontrado: str(program_path)')
  
  heading('Simulador da Máquina de Von Neumann', '=')
  print()
  
  vnm = VonNeumannMachine(memory_size=int(args.m))
  input_base = 'x' if program_path.suffix == '.hex' else 'b'
  vnm.load(program_path, input_base=input_base)
  
  print(Colors.OKBLUE + '>> Programa carregado na memória com sucesso' + Colors.ENDC)
  print()
  heading('Memória')
  hexdump(vnm.state.memory)
  print()
  heading('Registradores')
  show_registers(vnm.state)
  
  print()
  print(Colors.OKBLUE + '>> Iniciando execução do programa' + Colors.ENDC)
  print()
  
  vnm.execute_program()
  
  print()
  print(Colors.OKBLUE + '>> Fim da execução do programa' + Colors.ENDC)
  print()
  heading('Memória')
  hexdump(vnm.state.memory)
  print()
  heading('Registradores')
  show_registers(vnm.state)
  
  print()
  print(Colors.OKBLUE + '>> Fim da simulação' + Colors.ENDC)



if __name__ == '__main__':
  main()