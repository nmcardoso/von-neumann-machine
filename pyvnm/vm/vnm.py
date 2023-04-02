from pathlib import Path

from .control import ControlUnit
from .device import DeviceBus, Keyboard, Screen
from .io import Assembler, Dumper, Loader
from .memory import Memory
from .state import MachineState


class VonNeumannMachine:
  def __init__(
    self, 
    memory_size: int, 
    initial_acc: int = 0, 
    initial_pc: int = 0
  ):
    memory = Memory(memory_size)
    devices = DeviceBus()
    devices.add(0x1, Keyboard())
    devices.add(0x2, Screen())
    
    self.state = MachineState(
      memory=memory, 
      devices=devices, 
      acc=initial_acc, 
      pc=initial_pc
    )
    self.cu = ControlUnit(self.state)
    
    
  def load(self, bytecode: str | Path):
    bytecode = bytecode if isinstance(bytecode, str) else bytecode.read_text()
    loader = Loader(initial_state=self.state, bytecode=bytecode)
    loader.load()
    
    
  def execute_program(self):
    self.cu.event_loop()
    
  
  def dump(self) -> str:
    dumper = Dumper(self.state)
    return dumper.dump()