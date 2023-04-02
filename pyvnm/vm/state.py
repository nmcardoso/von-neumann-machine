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
    self.memory = memory
    self.devices = devices
    self.acc = Word(acc)
    self.pc = Word(pc)
    self.pc_lock = Lock()
    self.memory_start = memory_start
    self.instructions_begin = instructions_begin
    self.instructions_end = instructions_end
    self.code_entrypoint = code_entrypoint