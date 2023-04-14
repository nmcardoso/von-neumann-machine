import re
from pathlib import Path

from ..vm.state import MachineState


class Dumper:
  """
  Descarregador do binário e hexadecimal. Efetua a descaga do conteúdo
  da memória da máquina (usualmente, código + dados) para um arquivo
  
  Parameters
  ----------
  state: MachineState
    O estado a da máquina contendo a memória a ser descarregada
  output_path: str | Path
    Caminho para onde o arquivo será salvo
  output_base: str, optional
    Base numérica do arquivo a ser descarregado.
    Valores usados: ``'x'`` para hexadecimal e ``'b'`` para binário.
    Valor padrão: ``'x'``
  """
  def __init__(
    self, 
    state: MachineState, 
    output_path: Path = None, 
    output_base: str = 'x'
  ):
    self._state = state
    self._output_path = output_path
    self._output_base = output_base
  
  
  def dump(self) -> str:
    """
    Efetua a persistência do conteúdo presente na memória para outra mídia

    Returns
    -------
    str
      Conteúdo da memória
    """
    first_word_addr = self._state.memory.get_first_word_address()
    last_word_addr = self._state.memory.get_last_word_address()
    delta = self._state.memory_start - first_word_addr
    code_entrypoint = self._state.code_entrypoint - self._state.memory_start + delta
    
    bytecode = format(first_word_addr, self._output_base)
    
    for mem_pos in range(first_word_addr, last_word_addr + 1):
      if mem_pos == self._state.instructions_begin:
        bytecode += ' ['
        
      word = self._state.memory.read(mem_pos).value or 0x0
      bytecode += ' ' + format(word, self._output_base)
      
      if mem_pos == self._state.instructions_end:
        bytecode += ' ]'
        
    bytecode += format(code_entrypoint, self._output_base)
    
    if self._output_path is not None:
      self._output_path.write_text(bytecode)
    return bytecode
    
    