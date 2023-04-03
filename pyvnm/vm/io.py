import re
from pathlib import Path
from typing import List, Tuple

from .isa import Instruction, InstructionSet, Word
from .state import MachineState


class Loader:
  """
  Carregador do binário e hexadecimal. Efetua o carregamento do conteúdo
  de um arquivo (usualmente, código + dados) na memória da máquina
  
  Parameters
  ----------
  initial_state: MachineState
    O estado a da máquina a ser modificado com o carregamento dos dados na
    memória
  bytecode: str | Path
    Bytecode a ser decodificado e carredado no sistema
  input_base: str, optional
    Base numérica que em que se encontra o bytecode a ser carregado.
    Valores usados: ``'x'`` para hexadecimal e ``'b'`` para binário.
    Valor padrão: ``'x'``
  """
  def __init__(
    self, 
    initial_state: MachineState, 
    bytecode: str | Path, 
    input_base: str = 'x'
  ):
    self._state = initial_state
    self._bytecode = bytecode.read_text() if isinstance(bytecode, Path) else bytecode
    self._input_base = input_base
    self._words = self._bytecode.split(' ')
    
    
  def _get_instructions_range(self) -> Tuple[int, int]:
    """
    Faz uma busca no bytecode pelos caracteres de controle de início e fim das
    instruções
    
    Returns
    -------
    int, int
      Índice inicial e final, respectivamente, do intervalo onde se encontram
      as instruções de programa no bytecode a ser carregado
    """
    try:
      instr_begin = self._words.index('[')
    except ValueError as _:
      instr_begin = 0
    
    try:
      instr_end = self._words.index(']')
    except ValueError as _:
      instr_end = len(self._words)
      
    return instr_begin, instr_end
    
    
  def load(self):
    """
    Efetua o carregamento do código na memória da máquina fazendo modificações
    em uma instancia de `StateMachine`.
    """
    memory_start = Word.convert_to_int(f'0{self._input_base}{self._words[0]}')
    code_entrypoint = Word.convert_to_int(f'0{self._input_base}{self._words[-1]}')
    instruction_begin, instruction_end = self._get_instructions_range()
    
    for index in range(1, len(self._words) - 1):
      word = self._words[index]
      prefixed_word = f'0{self._input_base}{word}'
      
      if index < instruction_begin:
        w = Word(prefixed_word)
        shift = -1
      elif instruction_begin < index < instruction_end:
        w = Instruction(prefixed_word)
        shift = -2
      elif index > instruction_end:
        w = Word(prefixed_word)
        shift = -3
      else:
        continue
      
      mem_pos = memory_start + index + shift
      self._state.memory.write(mem_pos, w)
      
    self._state.memory_start = memory_start
    self._state.code_entrypoint = memory_start + code_entrypoint
    self._state.instructions_begin = memory_start + instruction_begin - 1
    self._state.instructions_end = memory_start + instruction_end - 3
    self._state.pc.value = memory_start + code_entrypoint
  
  
  
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
    
    