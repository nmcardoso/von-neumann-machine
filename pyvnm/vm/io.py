import re
from abc import abstractmethod
from pathlib import Path
from typing import List

from .isa import ControlWord, Instruction, InstructionSet, Word
from .state import MachineState


class Assembler:
  def __init__(self, program: str, output_base: str = 'x'):
    self._program = program
    self._output_base = output_base
  
  
  def assemble(self) -> str:
    program_lines = self._program.split('\n')
    is_instruction = False
    
    bytecode = self._parse_control_instruction(program_lines[0])
    for line in program_lines[1:-1]:
      line = line.strip()
      parts = re.split(r'\s+', line)
      
      if is_instruction:
        if len(parts) == 2:
          instr_int = self._parse_instruction(parts[0], parts[1])
          bytecode += ' ' + format(instr_int, self._output_base)
        elif len(parts) == 1:
          if parts[0] == ']':
            bytecode += ' ]'
            is_instruction = False
        else:
          bytecode += ' 0'
      else:
        if parts[0] == '[':
          bytecode += ' ['
          is_instruction = True
        else:
          bytecode += ' ' + self._parse_data(parts[0])
    bytecode += ' ' + self._parse_control_instruction(program_lines[-1])
    return bytecode
  
    
  def _parse_instruction(self, opcode: str, operand: str) -> int:
    opcode = InstructionSet.get_opcode(opcode)
    operand = Word.convert_to_int(operand)
  
    opcode_bits = Word.int_to_bin(opcode, extend=True, word_size=4)
    operand_bits = Word.int_to_bin(operand, extend=True, word_size=12)
    
    word_bits = opcode_bits + operand_bits
    return Word.bin_to_int(word_bits)
    
    
  def _parse_control_instruction(self, instruction: str) -> int:
    instr_int = Word.convert_to_int(instruction)
    return format(instr_int, self._output_base)
  
  
  def _parse_data(self, data: str) -> int:
    data_int = Word.convert_to_int(data)
    return format(data_int, self._output_base)
    


class Loader:
  def __init__(self, initial_state: MachineState, bytecode: str, input_base: str = 'x'):
    self._state = initial_state
    self._bytecode = bytecode
    self._input_base = input_base
    
    
  def load(self):
    words = self._bytecode.split(' ')
    memory_start = Word.convert_to_int(f'0{self._input_base}{words[0]}')
    code_entrypoint = Word.convert_to_int(f'0{self._input_base}{words[-1]}')
    is_instruction = False
    
    self._state.memory.write(
      memory_start, 
      ControlWord(memory_start, ControlWord.MEMORY_START)
    )
    
    for pos, word in enumerate(words[1:-1], start=memory_start + 1):
      prefixed_word = f'0{self._input_base}{word}'
      
      if is_instruction:
        if word != ']':
          w = Instruction(prefixed_word)
        else:
          w = ControlWord(']', kind=ControlWord.INSTRUCTIONS_BEGIN)
          is_instruction = False
      else:
        if word != '[':
          w = Word(prefixed_word)
        else:
          w = ControlWord('[', kind=ControlWord.INSTRUCTIONS_END)
          is_instruction = True
      
      self._state.memory.write(pos, w)
          
    self._state.memory.write(
      pos + 1, 
      ControlWord(code_entrypoint, ControlWord.CODE_ENTRYPOINT)
    )
      
    self._state.pc.value = memory_start + code_entrypoint
    # print(self._state.memory._data)
  
  
  
class Dumper:
  def __init__(self):
    pass
  
  
  def dump(self):
    pass