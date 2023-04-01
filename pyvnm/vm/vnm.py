from pathlib import Path

from .control import ControlUnit
from .device import Devices, Keyboard, Screen
from .io import Assembler, Loader
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
    assembler = Assembler(program=path.read_text())
    bytecode = assembler.assemble()
    # print(bytecode)
    loader = Loader(initial_state=self.state, bytecode=bytecode)
    loader.load()
    # print(self.state.memory._data)
    self.cu.event_loop()