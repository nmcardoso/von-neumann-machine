from pathlib import Path

from ..system.dumper import Dumper
from ..system.loader import Loader
from .control import ControlUnit
from .device import DeviceBus, Keyboard, Screen
from .memory import Memory
from .state import MachineState


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
    Quantidade de posições de memória da Maquina criada, cada palavra da
    memória possui, por padrão, 16 bits.
  initial_acc: int
    Valor inicial do registrador acumulador
  initial_pc: int
    Valor inicial do contador de programa
  """
  def __init__(self, memory_size: int):
    memory = Memory(memory_size)
    devices = DeviceBus()
    devices.add(0x1, Keyboard())
    devices.add(0x2, Screen())
    
    self.state = MachineState(memory=memory, devices=devices)
    self.control_unit = ControlUnit(self.state)
    
    
  def load(self, bytecode: str | Path, input_base: str = 'x'):
    """
    Carrega o bytecode fornecido na memória da máquina

    Parameters
    ----------
    bytecode : str | Path
      Bytecode a ser carregado
    input_base: str, opcional
      Base numérica que em que se encontra o bytecode a ser carregado.
      Valores usados: ``'x'`` para hexadecimal e ``'b'`` para binário.
      Valor padrão: ``'x'``
    """
    bytecode = bytecode if isinstance(bytecode, str) else bytecode.read_text()
    loader = Loader(initial_state=self.state, bytecode=bytecode, input_base=input_base)
    loader.load()
    
    
  def execute_program(self):
    """
    Aciona a Unidade de Controle para o início da execução do programa
    """
    self.control_unit.event_loop()
    
  
  def dump(self, output_path: str | Path = None, output_base: str = 'x') -> str:
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
    dumper = Dumper(self.state, output_path=output_path, output_base=output_base)
    return dumper.dump()