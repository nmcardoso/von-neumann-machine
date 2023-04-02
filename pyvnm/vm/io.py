import re
from pathlib import Path
from typing import List

from .isa import Instruction, InstructionSet, Word
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
  def __init__(self, initial_state: MachineState, bytecode: str | Path, input_base: str = 'x'):
    self._state = initial_state
    self._bytecode = bytecode.read_text() if isinstance(bytecode, Path) else bytecode
    self._input_base = input_base
    self._words = self._bytecode.split(' ')
    
    
  def _get_instructions_range(self):
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
  def __init__(self, state: MachineState, output_path: Path = None, output_base: str = 'x'):
    self._state = state
    self._output_path = output_path
    self._output_base = output_base
  
  
  def dump(self) -> str:
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
    
    