from .isa import Instruction, InstructionSet, Word
from .state import MachineState


class ControlUnit:
  """
  Unidade de Controle: entidade responsavel por executar um código carregado
  na memória
  
  Parameters
  ----------
  initial_state: MachineState
    Estado inicial da máquina, usualmente gerado pelo carregador
  """
  def __init__(self, initial_state: MachineState):
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
    b = self.state.instructions_begin 
    e = self.state.instructions_end
    while not self.state.sig_term and (b <= self.state.pc.value <= e):
      curr_inst = self.state.memory.read(self.state.pc.value)
      action = self._action_switcher.get(curr_inst.opcode)
      action(curr_inst.operand)
      self._increment_pc()
  
  
  def _increment_pc(self):
    """
    Incrementa o registrador PC em uma unidade
    """
    if not self.state.pc_lock.is_locked():
      self.state.pc.value += 1
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
    self.state.sig_term = True
      
      
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
    self.state.acc.value *= self.state.memory.read(operand).value
    
    
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
    current_next_instr_addr = self.state.pc.value + 1
    subroutine_next_instr_addr = operand + 1
    return_jump = Instruction.build(InstructionSet.JP, current_next_instr_addr)
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
    self.state.acc = dev.read()
  
  
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
    print(f'Código {operand} enviado ao Sistema Operacional')