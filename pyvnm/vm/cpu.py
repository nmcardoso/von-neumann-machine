from ..system.os import OS
from .device import DeviceBus
from .memory import Memory, Word
from .utils import Lock


class CPUState:
  """
  Entidade que armazena o estado da Unidade Central de Processamento da
  Máquina de Von Neumann

  Parameters
  ----------
  memory: Memory
    A memória da máquina
  devices: DeviceBus
    O bus de dispositivos da máquina
  acc: int, opcional
    O valor inicial do registrador acumulador, valor padrão: 0
  pc: int, opcional
    O valor inicial do registrador PC, valor padrão: 0
    
  Attributes
  ----------
  pc_lock: Lock
    Cadeado usado para implementação da lógica de bloqueio do registrador
    PC (program counter)
  sig_term: bool
    Sinal que indica a terminação da execução de um programa em execução
  """
  def __init__(
    self, 
    memory: Memory, 
    devices: DeviceBus, 
    acc: int = 0, 
    pc: int = 0
  ):
    self.memory = memory
    self.devices = devices
    self.acc = Word(acc)
    self.pc = Word(pc)
    self.pc_lock = Lock()
    self.loader_addr = None
    self.dumper_addr = None


class CPU:
  """
  Responsavel por executar um código carregado na memória
  
  Parameters
  ----------
  initial_state: MachineState
    Estado inicial da máquina, usualmente gerado pelo carregador
  """
  def __init__(self, initial_state: CPUState):
    self._action_switcher = {
      InstructionSet.JP: self._action_JP,
      InstructionSet.RS: self._action_RS,
      InstructionSet.JZ: self._action_JZ,
      InstructionSet.JN: self._action_JN,
      InstructionSet.HJ: self._action_HJ,
      InstructionSet.AD: self._action_AD,
      InstructionSet.SB: self._action_SB,
      InstructionSet.ML: self._action_ML,
      InstructionSet.DV: self._action_DV,
      InstructionSet.LD: self._action_LD,
      InstructionSet.ST: self._action_ST,
      InstructionSet.SC: self._action_SC,
      InstructionSet.GD: self._action_GD,
      InstructionSet.PD: self._action_PD,
      InstructionSet.OS: self._action_OS,
    }
    self.state = initial_state
    
  
  def event_loop(self):
    """
    Inicia a execução de um programa a partir da posição indicada pelo
    registrador PC.
    """
    print(self.state.memory.read(83 * 2 - 0).int)
    while not OS.SIG_TERM in OS.flags:
      curr_inst = self.state.memory.read(self.state.pc.value)
      print(self.state.pc.value // 2 + 2, '\t', InstructionSet.get_mnemonic(curr_inst.opcode), curr_inst.operand // 2 + 2, end='')
      if not curr_inst.is_instruction():
        break
      action = self._action_switcher.get(curr_inst.opcode)
      action(curr_inst.operand)
      print('\t\tacc:', self.state.acc.int)
      self._increment_pc()
  
  
  def _increment_pc(self):
    """
    Incrementa o registrador PC em uma unidade
    """
    if not self.state.pc_lock.is_locked():
      self.state.pc.value += 2
    self.state.pc_lock.release()
    
  
  def _action_JP(self, operand: int):
    """
    Ação realizada pela instrução JP (Jump uncondicional)

    Parameters
    ----------
    operand : int
      Endereço da memória
    """
    self.state.pc.value = operand
    self.state.pc_lock.aquire()
    
    
  def _action_RS(self, operand: int):
    """
    Ação realizada pela instrução RS (Return from subroutine)

    Parameters
    ----------
    operand : int
      Endereço da memória
    """
    self.state.pc.value = operand
    self.state.pc_lock.aquire()
    
    
  def _action_JZ(self, operand: int):
    """
    Ação realizada pela instrução JZ (Jump if acc = 0)

    Parameters
    ----------
    operand : int
      Endereço da memória
    """
    if self.state.acc.value == 0:
      self.state.pc.value = operand
      self.state.pc_lock.aquire()
      
      
  def _action_JN(self, operand: int):
    """
    Ação realizada pela instrução JN (Jump if acc < 0)

    Parameters
    ----------
    operand : int
      Endereço da memória
    """
    if self.state.acc.value < 0:
      self.state.pc.value = operand
      self.state.pc_lock.aquire()
      
      
  def _action_HJ(self, operand: int):
    """
    Ação realizada pela instrução HJ (Jump after halt)

    Parameters
    ----------
    operand : int
      Endereço da memória
    """
    self.state.pc.value = operand
    self.state.pc_lock.aquire()
    OS.flags.add(OS.SIG_TERM)
      
      
  def _action_AD(self, operand: int):
    """
    Ação realizada pela instrução AD (Adição)

    Parameters
    ----------
    operand : int
      Endereço da memória
    """
    self.state.acc.value += self.state.memory.read(operand).value
    
    
  def _action_SB(self, operand: int):
    """
    Ação realizada pela instrução SB (Subtração)

    Parameters
    ----------
    operand : int
      Endereço da memória
    """
    self.state.acc.value -= self.state.memory.read(operand).value
    
    
  def _action_ML(self, operand: int):
    """
    Ação realizada pela instrução ML (Jump multiplicação)

    Parameters
    ----------
    operand : int
      Endereço da memória
    """
    # print('\n', self.state.acc.value, '*', self.state.memory.read(operand).value, '=', self.state.acc.value * self.state.memory.read(operand).value)
    self.state.acc.value *= self.state.memory.read(operand).value
    # print(Word(self.state.acc.value * self.state.memory.read(operand).value).bin)
    
    
  def _action_DV(self, operand: int):
    """
    Ação realizada pela instrução DV (Divisão)

    Parameters
    ----------
    operand : int
      Endereço da memória
    """
    self.state.acc.value //= self.state.memory.read(operand).value
    
    
  def _action_LD(self, operand: int):
    """
    Ação realizada pela instrução LD (Load)

    Parameters
    ----------
    operand : int
      Endereço da memória
    """
    self.state.acc.value = self.state.memory.read(operand).value
    
    
  def _action_ST(self, operand: int):
    """
    Ação realizada pela instrução ST (Store)

    Parameters
    ----------
    operand : int
      Endereço da memória
    """
    self.state.memory.write(operand, Word(self.state.acc.value))
    
    
  def _action_SC(self, operand: int):
    """
    Ação realizada pela instrução SC (Subroutine Call)

    Parameters
    ----------
    operand : int
      Endereço da memória
    """
    current_next_instr_addr = self.state.pc.value + 2
    subroutine_next_instr_addr = operand + 2
    return_jump = Word.from_instruction(InstructionSet.JP, current_next_instr_addr)
    self.state.memory.write(operand, return_jump)
    self.state.pc.value = subroutine_next_instr_addr
    self.state.pc_lock.aquire()
  
  
  def _action_GD(self, operand: int):
    """
    Ação realizada pela instrução GD (Get Data)

    Parameters
    ----------
    operand : int
      Endereço do dispositivo
    """
    dev = self.state.devices.get(operand)
    self.state.acc.value = dev.read().value
  
  
  def _action_PD(self, operand: int):
    """
    Ação realizada pela instrução PD (Put Data)

    Parameters
    ----------
    operand : int
      Endereço do dispositivo
    """
    dev = self.state.devices.get(operand)
    dev.write(self.state.acc)
  
  
  def _action_OS(self, operand: int):
    """
    Ação realizada pela instrução OS (Chamada no sistema operacional)

    Parameters
    ----------
    operand : int
      Código
    """
    print(f'Chamada ao sistema com código {operand}')

  
class InstructionSet:
  JP = 0x0
  """Instrução JP (Jump uncondicional)"""
  RS = 0x0
  """Instrução RS (Return from subroutine)"""
  JZ = 0x1
  """Instrução JZ (Jump if acc = 0)"""
  JN = 0x2
  """Instrução JN (Jump if acc < 0)"""
  HJ = 0x3
  """Instrução HJ (Jump after halt)"""
  AD = 0x4
  """Instrução AD (Adição)"""
  SB = 0x5
  """Instrução SB (Subtração)"""
  ML = 0x6
  """Instrução ML (Multiplicação)"""
  DV = 0x7
  """Instrução DV (Divisão)"""
  LD = 0x8
  """Instrução LD (Load)"""
  ST = 0x9
  """Instrução ST (Store)"""
  SC = 0xA
  """Instrução SC (Subroutine Call)"""
  GD = 0xB
  """Instrução GD (Get Data)"""
  PD = 0xC
  """Instrução PD (Put Data)"""
  OS = 0xD
  """Instrução OS (Chamada no sistema operacional)"""
  
  
  @classmethod
  def get_opcode(cls, mnemonic: str) -> int:
    """
    Obtém o código da operação (opcode) a partir de seu símbolo

    Parameters
    ----------
    mnemonic : str
      Mnemonico do opcode buscado

    Returns
    -------
    int
      Valor do opcode
    """
    return cls.__dict__.get(mnemonic, None)
  
  
  @classmethod
  def get_mnemonic(cls, opcode: int) -> str:
    """
    Obtém o mnemônico da instrução a partir de seu opcode

    Parameters
    ----------
    opcode : int
      O código da operação

    Returns
    -------
    str
      O mnemônico correspondente
    """
    for name, code in cls.__dict__.items():
      if code == opcode:
        return name
    return None