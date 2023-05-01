import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import numpy as np

from pyvnm.system.os import OS
from pyvnm.vm.cpu import CPUCallback, CPUState, InstructionSet
from pyvnm.vm.memory import Word
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

    

class DebugCallback(CPUCallback):
  def _hexdump_line(self, state: CPUState, line: int, highlight: int):
    print(Colors.LIGHT_YELLOW + Word(line * 16).hex + ':' + Colors.RESET + ' ', end='')
    for i in range(0, 16, 2):
      addr = line * 16 + i
      w = state.memory.read(addr)
      if w.value is None:
        print('00 00 ', sep='', end='')
      elif addr == highlight:
        print(Colors.LIGHT_GREEN + w.hex[:2] + ' ' + w.hex[2:], ' ' + Colors.RESET, sep='', end='')
      else:
        print(w.hex[:2] + ' ' + w.hex[2:], ' ', sep='', end='')
    print()
    
    
  def on_event_loop_begin(self, state: CPUState):
    heading('Depuração', '~')

  
  def on_instruction_begin(self, state: CPUState):
    instruction = state.memory.read(state.pc.uint)
    mnemonic = InstructionSet.get_mnemonic(instruction.opcode)
    operand = Word(instruction.operand).hex
    print()
    print('Instrução: ' + Colors.LIGHT_CYAN + mnemonic + ' ' + operand[1:] + Colors.RESET)
  
  
  def on_instruction_end(self, state: CPUState):
    instruction = state.memory.read(state.pc.uint)
    print(f'    PC: {state.pc.uint}\tACC: {state.acc.int} (0x{state.acc.hex})')
    if instruction.opcode == InstructionSet.ST or instruction.opcode == InstructionSet.LD:
      line = int(np.floor(instruction.operand / 16))
      highlight = instruction.operand
      print('    MEM: ', end='')
      self._hexdump_line(state, line, highlight)



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
    
    
    
def machine_summary(state: CPUState):
  print()
  heading('Memória')
  state.memory.hexdump(Colors())
  print()
  heading('Registradores')
  print('Acumulador:\t', format(state.acc.value or 0, '0>4x'))
  print('PC:\t\t', format(state.pc.value or 0, '0>4x'))
  print()
    
    

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
    '-m', 
    action='store',
    default=4096,
    help='Número de posições na memória. Padrão: 4096'
  )
  p.add_argument(
    '-d', '--dump',
    action='store',
    default=None,
    help=(
      'Caminho absoluto ou relativo para onde o dump da memória deve ser '
      'salvo após a execução do programa'
    )
  )
  p.add_argument(
    '-b', '--debug',
    action='store_true',
    help=(
      'Executa o programa no modo depuração. Este modo exibe detalhadamente '
      'as mudanças nos registradores e na memória em cada instrução'
    )
  )
  p.add_argument(
    '-s', '--sysdebug',
    action='store_true',
    help=(
      'Executa o programa no modo depuração de sistema. Este modo exibe '
      'detalhadamente as mudanças nos registradores e na memória em cada '
      'instrução durante a execução dos programas de sistema LOADER e DUMPER'
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
    '--latex',
    action='store_true',
    help=(
      'Exibe a saída no programa no formato interpretável pelo Latex'
    )
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
      Colors.RED = Fore.RED
      Colors.BLUE = Fore.BLUE
      Colors.CYAN = Fore.CYAN
      Colors.GREEN = Fore.GREEN
      Colors.YELLOW = Fore.YELLOW
      Colors.MAGENTA = Fore.MAGENTA
      Colors.LIGHT_RED = Fore.LIGHTRED_EX
      Colors.LIGHT_BLUE = Fore.LIGHTBLUE_EX
      Colors.LIGHT_CYAN = Fore.LIGHTCYAN_EX
      Colors.LIGHT_GREEN = Fore.LIGHTGREEN_EX
      Colors.LIGHT_YELLOW = Fore.LIGHTYELLOW_EX
      Colors.LIGHT_MAGENTA = Fore.LIGHTMAGENTA_EX
      Colors.RESET = Fore.RESET
    except:
      print('A coloração do terminal depende do pacote Colorama')
      print('Instale executando pip3 install colorama')
      
      
  if args.latex:
    Colors.RED = '|*\color{red}'
    Colors.BLUE = '|*\color{blue!60!white}'
    Colors.CYAN = '|*\color{cyan}'
    Colors.GREEN = '|*\color{green}'
    Colors.YELLOW = '|*\color{yellow}'
    Colors.MAGENTA = '|*\color{magenta}'
    Colors.LIGHT_RED = '|*\color{red}'
    Colors.LIGHT_BLUE = '|*\color{blue!60!white}'
    Colors.LIGHT_CYAN = '|*\color{cyan}'
    Colors.LIGHT_GREEN = '|*\color{green}'
    Colors.LIGHT_YELLOW = '|*\color{yellow}'
    Colors.LIGHT_MAGENTA = '|*\color{magenta}'
    Colors.RESET = '*|'
  
  program_callback = None
  loader_callback = None
  dumper_callback = None
  
  if args.debug:
    program_callback = DebugCallback()
  
  if args.sysdebug:
    loader_callback = DebugCallback()
    dumper_callback = DebugCallback()
  
  heading('Simulador da Máquina de Von Neumann', '=')
  print()
  
  vnm = VonNeumannMachine(
    memory_size=int(args.m), 
    load_path=program_path,
    dump_path=args.dump,
    loader_callback=loader_callback,
    dumper_callback=dumper_callback,
    program_callback=program_callback,
  )
  input_base = 'x' if program_path.suffix == '.hex' else 'b'
  
  print(Colors.LIGHT_BLUE + '>> Iniciando boot do sistema' + Colors.RESET)
  print()
  
  vnm.boot()
  
  print(Colors.LIGHT_BLUE + '>> Programas de sistema carregados com sucesso na memória' + Colors.RESET)
  print()
  
  machine_summary(vnm.cpu.state)
  
  print(Colors.LIGHT_BLUE + '>> Iniciando carregamento do programa na memória' + Colors.RESET)
  print()
  
  vnm.load()
  
  print()
  print(Colors.LIGHT_BLUE + '>> Programa carregado na memória com sucesso' + Colors.RESET)
  
  machine_summary(vnm.cpu.state)
  
  print(Colors.LIGHT_BLUE + '>> Iniciando execução do programa' + Colors.RESET)
  print()
  
  vnm.execute_program()
  
  if OS.SIG_TRAP in OS.flags:
    print()
    print(Colors.LIGHT_RED + '>> O programa terminou com uma excessão' + Colors.RESET)
    
    if OS.LOADER_CHECKSUM_MISSMATCH in OS.flags:
      print(Colors.LIGHT_RED + '>> O programa não pôde ser carregado pois o checksum calculado não corresponde ao informado' + Colors.RESET)
  else:
    print()
    print(Colors.LIGHT_BLUE + '>> Fim da execução do programa' + Colors.RESET)
  
  machine_summary(vnm.cpu.state)
  
  if args.dump:
    print()
    print(Colors.LIGHT_BLUE + f'>> Iniciando dump da memória' + Colors.RESET)
    print()
    
    vnm.dump()
    
    print()
    print(Colors.LIGHT_BLUE + f'>> Memória descarregada com sucesso em {args.dump}' + Colors.RESET)
    print()
  
  print()
  print(Colors.LIGHT_BLUE + '>> Fim da simulação' + Colors.RESET)



if __name__ == '__main__':
  main()