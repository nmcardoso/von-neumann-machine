from .device import Devices
from .isa import Word
from .memory import Memory
from .utils import Lock


class MachineState:
  def __init__(
    self, 
    memory: Memory, 
    devices: Devices, 
    acc: int = 0, 
    pc: int = 0
  ):
    self.memory = memory
    self.devices = devices
    self.acc = Word(acc)
    self.pc = Word(pc)
    self.pc_lock = Lock()