import re
from collections import namedtuple
from dataclasses import dataclass
from pathlib import Path
from typing import List, Literal, NamedTuple, Tuple

from ..vm.isa import Instruction, InstructionSet, Word

LINE_PATTERN = r'^[ \t\f]*@.*$|(\w+)?[ \t\f]+(\w+)[ \t\f]*(\w+)?.*$'
LINE_PATTERN = r'^[ \t\f]*@.*$|^(?:(\w+)?[ \t\f]*)?(?:(\w+)[ \t\f]*)?(\w+)?.*$'
OPERAND_PATTERN = r'^(?:0[xb])?\d+$'


@dataclass
class LineTokens:
  label: str = None
  mnemonic: str = None
  operand: str = None
  index: int = None
  mem_addr: int = None
  empty: bool = None
  
  
class AssemblerInstructions:
  ORG = 'ORG'
  END = 'END'
  DATA = 'DATA'
  AREA = 'AREA'


class Assembler:
  def __init__(
    self, 
    program: str | Path, 
    output_path: str | Path = None, 
    output_base: Literal['x', 'b'] = 'x'
  ):
    self._program = program if isinstance(program, str) else program.read_text()
    self._output_path = Path(output_path) if output_path else None
    self._output_base = output_base
    
    self._line_regex = re.compile(LINE_PATTERN, flags=re.M)
    self._operand_regex = re.compile(OPERAND_PATTERN, flags=re.I)
    self._program_lines = self._program.splitlines()
  
    
  def assemble(self) -> str:
    labels, instructions = self._tokenize() # primeiro passo
    self._decode_operands(lbl_tokens=labels, inst_tokens=instructions) # segundo passo
    
    origin = instructions[0].mem_addr
    instr_end = False
    
    # geração do programa objeto
    program_object = format(origin, self._output_base) + ' ['
    for instruction in instructions:
      mnemonic = instruction.mnemonic
      operand = instruction.operand
      
      if operand is not None:
        if mnemonic == AssemblerInstructions.DATA:
          if not instr_end:
            instr_end = True
            program_object += ' ]'
          program_object += ' ' + format(operand, self._output_base)
        elif mnemonic == AssemblerInstructions.AREA:
          if not instr_end:
            instr_end = True
            program_object += ' ]'
          program_object += ' 0' * operand
        else:
          opcode = InstructionSet.get_opcode(mnemonic)
          inst_value = Instruction.build(opcode, operand).value
          program_object += ' ' + format(inst_value, self._output_base)
      else:
        if mnemonic is None:
          program_object += ' 0'
        elif mnemonic == AssemblerInstructions.END:
          if instr_end:
            program_object += ' 0'
          else:
            program_object += ' ] 0'
        
    print(*instructions, sep='\n')
        
    return program_object
    
    
  def _tokenize(self) -> Tuple[List[LineTokens], List[LineTokens]]:
    labels = []
    instructions = []
    
    orig_token = self._tokenize_line(
      line=self._program_lines[0], 
      line_index=0, 
      memory_offset=0
    )
    memory_offset = Word.convert_to_int(orig_token.operand)
    
    for i, line in enumerate(self._program_lines[1:]):
      tokens = self._tokenize_line(
        line=line, 
        line_index=i, 
        memory_offset=memory_offset
      )
      instructions.append(tokens)
      if tokens.label:
        labels.append(tokens)
    
    return (labels, instructions)
  
  
  def _tokenize_line(
    self, 
    line: str, 
    line_index: int, 
    memory_offset: int
  ) -> LineTokens:
    m = self._line_regex.match(line)
    
    if not m or not m.group(0).strip():
      return LineTokens(
        index=line_index, 
        mem_addr=memory_offset + line_index, 
        empty=True
      )
    
    return LineTokens(
      label=m.group(1),
      mnemonic=m.group(2),
      operand=m.group(3),
      index=line_index,
      mem_addr=memory_offset + line_index,
      empty=False
    )
  
  
  def _decode_operands(
    self, 
    lbl_tokens: List[LineTokens],
    inst_tokens: List[LineTokens],
  ):
    lbl_list = [l.label for l in lbl_tokens]
    
    for inst in inst_tokens:
      operand = inst.operand
      
      if not operand:
        inst.operand = None
        continue
      
      if self._operand_regex.search(operand):
        inst.operand = Word.convert_to_int(operand)
        continue
      
      try:
        idx = lbl_list.index(operand)
        inst.operand = lbl_tokens[idx].mem_addr
        continue
      except:
        pass
      
      inst.operand = None

  
  def _check_labels(self):
    pass
  
  
  def _check_mnemonics(self):
    pass
  
  
  def _check_operands(self):
    pass
      
      
      
      
if __name__ == '__main__':
  from pathlib import Path
  prog = Path(__file__).parent.parent.parent / 'programs' / 'test_02.asm'
  prog = prog.read_text()
  a = Assembler(prog, output_base='x')
  obj = a.assemble()
  print()
  print(obj)