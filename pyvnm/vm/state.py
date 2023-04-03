from .device import DeviceBus
from .isa import Word
from .memory import Memory
from .utils import Lock


class MachineState:
  def __init__(
    self, 
    memory: Memory, 
    devices: DeviceBus, 
    acc: int = 0, 
    pc: int = 0,
    memory_start: int = 0,
    instructions_begin: int = 0,
    instructions_end: int = 0,
    code_entrypoint: int = 0,
  ):
    """
    Entidade que armazena o estado da Máquina de Von Neumann

    Parameters
    ----------
    memory : Memory
      A memória da máquina
    devices : DeviceBus
      O bus de dispositivos da máquina
    acc : int, optional
      O valor inicial do registrador acumulador, valor padrão: 0
    pc : int, optional
      O valor inicial do registrador PC, valor padrão: 0
    memory_start : int, optional
      Instrução de controle obtida pelo carregador que especifica o endereço 
      inicial de carregamento na memória, valor padrão: 0
    instructions_begin : int, optional
      Instrução de controle obtida pelo carregador que especifica o endereço 
      na memória da primeira instrução do programa, valor padrão: 0
    instructions_end : int, optional
      Instrução de controle obtida pelo carregador que especifica o endereço na
      memória da última linha do programa, valor padrão: 0
    code_entrypoint : int, optional
      Instrução de controle obtida pelo carregador que especifica a posição
      na memória da primeira linha do programa a ser executada, valor padrão: 0
      
    Attributes
    ----------
    pc_lock: Lock
      Cadeado usado para implementação da lógica de bloqueio do registrador
      PC (program counter)
    """
    self.memory = memory
    self.devices = devices
    self.acc = Word(acc)
    self.pc = Word(pc)
    self.pc_lock = Lock()
    self.memory_start = memory_start
    self.instructions_begin = instructions_begin
    self.instructions_end = instructions_end
    self.code_entrypoint = code_entrypoint