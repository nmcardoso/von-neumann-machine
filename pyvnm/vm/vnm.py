from pathlib import Path

from .control import ControlUnit
from .device import Devices, Keyboard, Screen
from .io import SymbolicLoader
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
    devices = Devices()
    devices.add(0x1, Keyboard())
    devices.add(0x2, Screen())
    
    self.state = MachineState(
      memory=memory, 
      devices=devices, 
      acc=initial_acc, 
      pc=initial_pc
    )
    self.cu = ControlUnit(self.state)
    
  
  def execute_program(self, path: Path):
    loader = SymbolicLoader(initial_state=self.state, input_path=path)
    loader.load()
    self.cu.event_loop()