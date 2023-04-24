from pathlib import Path
from typing import Tuple

from ..vm.cpu import CPUState
from ..vm.memory import Byte, Word


class BootLoader:
  """
  Carregador do binário e hexadecimal. Efetua o carregamento do conteúdo
  de um arquivo (usualmente, código + dados) na memória da máquina
  
  Parameters
  ----------
  initial_state: MachineState
    O estado a da máquina a ser modificado com o carregamento dos dados na
    memória
  input_base: str, optional
    Base numérica que em que se encontra o programa objeto a ser carregado.
    Valores usados: ``'x'`` para hexadecimal e ``'b'`` para binário.
    Valor padrão: ``'x'``
  """
  def __init__(
    self, 
    initial_state: CPUState,
    input_base: str = 'x'
  ):
    self._state = initial_state
    self._input_base = input_base

    
  def load(self, program_obj: str | Path):
    """Carrega os principais programas de sistema na memória

    Parameters
    ----------
    program_obj : str | Path
      Caminho ou conteúdo do programa objeto a ser carregado
    """
    program_obj = program_obj.read_text() if isinstance(program_obj, Path) else program_obj
    program_bytes = program_obj.split(' ')
    
    initial_addr = self._to_word(''.join(program_bytes[:2])).uint
    addr = initial_addr
    
    # ignora os 4 primeiros bytes (endereço inicial e número de bytes) 
    # e o último byte (checksum)
    for i in range(4, len(program_bytes) - 1):
      self._state.memory.write_byte(addr, self._to_byte(program_bytes[i]))
      addr += 1
      
    return initial_addr
    
  
  def _to_byte(self, value) -> Byte:
    b = '0x' + value if self._input_base == 'x' else '0b' + value
    return Byte(b)
  
  
  def _to_word(self, value) -> Word:
    w = '0x' + value if self._input_base == 'x' else '0b' + value
    return Word(w)