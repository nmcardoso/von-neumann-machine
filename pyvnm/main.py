import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from pyvnm.system.os import OS
from pyvnm.vm.cpu import CPUState
from pyvnm.vm.vnm import VonNeumannMachine


class Colors:
  BLUE = ''
  CYAN = ''
  GREEN = ''
  YELLOW = ''
  MAGENTA = ''
  LIGHT_BLUE = ''
  LIGHT_CYAN = ''
  LIGHT_GREEN = ''
  LIGHT_YELLOW = ''
  LIGHT_MAGENTA = ''
  RESET = ''



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
    
    
    
def show_registers(state: CPUState):
  print('Acumulador:\t', format(state.acc.value or 0, '0>4x'))
  print('PC:\t\t', format(state.pc.value or 0, '0>4x'))


def cli():
  p = argparse.ArgumentParser(prog='python3 main.py', description='Simulador da Máquina de Von Neumann')
  p.add_argument(
    'programa', 
    nargs=1,
    action='store', 
    help=(
      'Caminho relativo ou absoluto do programa a ser executado. '
      'O simulador decide automaticamente o que fazer dependendo '
      'da extensão do arquivo forneceido. Caso a extensão seja `.hex`, '
      'o arquivo será considerado um programa-objeto absoluto na '
      'base hexadicimal e será carregado na memória por um carregador '
      'hexadecimal. Caso a extensão seja `.bin`, o arquivo será considerado '
      'um programa-objeto absoluto na base binária e será carregador na '
      'memória por um carregador binário.'
    )
  )
  p.add_argument(
    '-c',
    action='store_true',
    help=(
      'Usa cores na saída do terminal para facilitar a legibilidade da saída.'
    )
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
  args = cli()
  
  program_path = Path(args.programa[0])
  if not program_path.exists():
    return print(f'Arquivo não encontrado: str(program_path)')
  
  if args.c:
    try:
      from colorama import Fore, init
      init()
      Colors.BLUE = Fore.BLUE
      Colors.CYAN = Fore.CYAN
      Colors.GREEN = Fore.GREEN
      Colors.YELLOW = Fore.YELLOW
      Colors.MAGENTA = Fore.MAGENTA
      Colors.LIGHT_BLUE = Fore.LIGHTBLUE_EX
      Colors.LIGHT_CYAN = Fore.LIGHTCYAN_EX
      Colors.LIGHT_GREEN = Fore.LIGHTGREEN_EX
      Colors.LIGHT_YELLOW = Fore.LIGHTYELLOW_EX
      Colors.LIGHT_MAGENTA = Fore.LIGHTMAGENTA_EX
      Colors.RESET = Fore.RESET
    except:
      print('A coloração do terminal depende do pacote Colorama')
      print('Instale executando pip3 install colorama')
  
  heading('Simulador da Máquina de Von Neumann', '=')
  print()
  
  vnm = VonNeumannMachine(memory_size=int(args.m), load_path=program_path)
  input_base = 'x' if program_path.suffix == '.hex' else 'b'
  vnm.boot()
  
  print(Colors.LIGHT_BLUE + '>> Programa carregado na memória com sucesso' + Colors.RESET)
  print()
  heading('Memória')
  vnm.state.memory.hexdump(Colors())
  print()
  heading('Registradores')
  show_registers(vnm.state)
  
  print()
  print(Colors.LIGHT_BLUE + '>> Iniciando execução do programa' + Colors.RESET)
  print()
  
  vnm.execute_program()
  
  if OS.SIG_TRAP in OS.flags:
    print(Colors.MAGENTA + '>> O programa terminou com uma excessão' + Colors.RESET)
    
    if OS.LOADER_CHECKSUM_MISSMATCH in OS.flags:
      print(Colors.MAGENTA + '>> O programa não pôde ser carregado pois o checksum calculado não corresponde ao informado' + Colors.RESET)
  
  print()
  print(Colors.LIGHT_BLUE + '>> Fim da execução do programa' + Colors.RESET)
  print()
  heading('Memória')
  vnm.state.memory.hexdump(Colors())
  print()
  heading('Registradores')
  show_registers(vnm.state)
  
  print()
  print(Colors.LIGHT_BLUE + '>> Fim da simulação' + Colors.RESET)



if __name__ == '__main__':
  main()