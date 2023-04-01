import re
from abc import abstractclassmethod
from pathlib import Path
from typing import List

from .isa import Instruction, InstructionSet, Word
from .state import MachineState


class Assembler:
  pass


class Loader:
  def __init__(self, initial_state: MachineState, input_path: Path):
    self._state = initial_state
    self._input_path = input_path
    
    
  @abstractclassmethod
  def _parse(self, word: str) -> Instruction:
    pass
  
  
  def load(self):
    data = self._input_path.read_text().split('\n')
    memory_start = Word.convert_to_int(data[0])
    code_entrypoint = Word.convert_to_int(data[-1])
    
    for pos, word in enumerate(data[1:-1], start=memory_start):
      instruction = self._parse(word)
      self._state.memory.write(pos, instruction)
      
    self._state.pc.value = memory_start + code_entrypoint - 1
    # print(self._state.memory._data)
      
      
      
class BinaryLoader(Loader):
  def _parse(self, word: str) -> Instruction:
    word_bits = Word.int_to_bin(Word.convert_to_int(word))
    opcode = Word.bin_to_int(word_bits[:4])
    operand = Word.bin_to_int(word_bits[4:])
    return Instruction(opcode, operand)
  
  
  
class SymbolicLoader(Loader):
  def _parse(self, word: str) -> Instruction:
    instr_parts = re.split(r'\s+', word)
    opcode = InstructionSet.get_opcode(instr_parts[0])
    operand = Word.convert_to_int(instr_parts[1])
    opcode_bits = Word.int_to_bin(opcode, extend=True, word_size=4)
    operand_bits = Word.int_to_bin(operand, extend=True, word_size=12)
    word_bits = opcode_bits + operand_bits
    word_int = Word.bin_to_int(word_bits)
    return Instruction(word_int)
  



class Dumper:
  def __init__(self):
    pass
  
  
  def dump(self):
    pass