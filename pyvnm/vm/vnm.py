from pathlib import Path

from ..system.bootloader import BootLoader
from .cpu import CPU, CPUCallback, CPUState
from .device import CharScreen, DeviceBus, HardDisk, Keyboard, Screen
from .memory import Byte, Memory


class VonNeumannMachine:
  """
  O mais alto nível de abstração da Máquina de Von Neumann, todas as operações
  de entrada/saída, a manipulação de dados, as mudanças de estado 
  e o carregamento de dispositivos estão abstraídos.
  
  Esta classe permite a criação de uma máquina de Von Neumann, bem como a 
  carga e descarga de conteúdo em sua memória e execução de programas 
  sem necessidade de manipulação de componentes de hardware
  
  Parameters
  ----------
  memory_size: int
    Quantidade de posições de memória da Maquina criada
  initial_pc: int
    Valor inicial do contador de programa
  """
  def __init__(
    self, 
    memory_size: int, 
    load_path: Path, 
    dump_path: Path = None, 
    cpu_callback: CPUCallback = CPUCallback()
  ):
    self._load_path = load_path
    self._dump_path = dump_path
    
    # inicializa memória
    memory = Memory(memory_size)
    
    # inicializa dispositivos
    devices = DeviceBus()
    devices.add(0x1, Keyboard())
    devices.add(0x2, Screen())
    devices.add(0x3, CharScreen())
    devices.add(0x4, HardDisk(input_path=load_path, output_path=dump_path))
    
    # inicializa CPU
    cpu_state = CPUState(memory=memory, devices=devices)
    self.cpu = CPU(cpu_state, cpu_callback)
    
    
  def boot(self):
    """
    Carregamento inicial dos principais programas de sistema na máquina
    """
    loader_path = Path(__file__).parent.parent / 'system' / 'loader.hex'
    # loader_path = Path(__file__).parent.parent.parent / 'programs' / 'test_07.hex'
    # dumper_path = Path(__file__).parent.parent / 'system' / 'dumper.hex'
    bl = BootLoader(initial_state=self.cpu.state, input_base='x')
    self.cpu.state.loader_addr = bl.load(loader_path.read_text())
    # self.cpu.state.dumper_addr = bl.load(dumper_path.read_text())
    
    
  def load(self):
    self.cpu.state.pc = self.cpu.state.loader_addr
    self.execute_program()
    
    
  def execute_program(self):
    """
    Aciona a Unidade de Controle para o início da execução do programa
    """
    self.cpu.event_loop()
    
  
  def dump(self) -> str:
    """
    Aciona o Dumper para a persistência dos dados carregados na memória
    para outra mídia
    
    Parameters
    ----------
    output_path: str | Path
      Caminho para onde o arquivo será salvo
    output_base: str
      Base numérica do arquivo a ser descarregado.
      Valores usados: ``'x'`` para hexadecimal e ``'b'`` para binário.
      Valor padrão: ``'x'``

    Returns
    -------
    str
      Valor da memória codificado na base especificada
    """
    self.cpu.state.pc = self.cpu.state.dumper_addr
    self.execute_program()
    hd = self.cpu.state.devices.get(4)
    hd.save()