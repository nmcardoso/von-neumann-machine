from .isa import Instruction, InstructionSet, Word
from .state import MachineState


class ControlUnit:  
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
    while True:
      if 0 < self.state.pc.value < self.state.memory.size:
        curr_inst = self.state.memory.read(self.state.pc.value)
      else:
        return

      if not isinstance(curr_inst, Instruction):
        self._increment_pc()
        continue
      
      action = self._action_switcher.get(curr_inst.opcode)
      action(curr_inst.operand)
      self._increment_pc()
  
  
  def _increment_pc(self):
    if not self.state.pc_lock.is_locked():
      self.state.pc.value += 1
    self.state.pc_lock.release()
  
  
  def _action_JP(self, operand: int):
    self.state.pc.value = operand
    self.state.pc_lock.aquire()
    
    
  def _action_RS(self, operand: int):
    pass
    
    
  def _action_JZ(self, operand: int):
    if self.state.acc.value == 0:
      self.state.pc.value = operand
      self.state.pc_lock.aquire()
      
      
  def _action_JN(self, operand: int):
    if self.state.acc.value < 0:
      self.state.pc.value = operand
      self.state.pc_lock.aquire()
      
      
  def _action_HJ(self, operand: int):
    pass
      
      
  def _action_AD(self, operand: int):
    self.state.acc.value += self.state.memory.read(operand).value
    
    
  def _action_SB(self, operand: int):
    self.state.acc.value -= self.state.memory.read(operand).value
    
    
  def _action_ML(self, operand: int):
    self.state.acc.value *= self.state.memory.read(operand).value
    
    
  def _action_DV(self, operand: int):
    self.state.acc.value //= self.state.memory.read(operand).value
    
    
  def _action_LD(self, operand: int):
    self.state.acc.value = self.state.memory.read(operand).value
    
    
  def _action_ST(self, operand: int):
    self.state.memory.write(operand, Word(self.state.acc.value))
    
    
  def _action_SC(self, operand: int):
    pass
  
  
  def _action_GD(self, operand: int):
    dev = self.state.devices.get(operand)
    self.state.acc = dev.read()
  
  
  def _action_PD(self, operand: int):
    dev = self.state.devices.get(operand)
    dev.write(self.state.acc)
  
  
  def _action_OS(self, operand: int):
    pass