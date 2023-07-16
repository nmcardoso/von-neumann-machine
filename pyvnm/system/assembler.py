import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Literal, Tuple

from ..vm.cpu import InstructionSet
from ..vm.memory import Byte, Word

LINE_PATTERN = r'^[ \t\f]*@.*$|(\w+)?[ \t\f]+(\w+)[ \t\f]*(\w+)?.*$'
"""Padrão separa a linha em três grupos: rótulo, mnemônico e operando"""
LINE_PATTERN = r'^[ \t\f]*@.*$|^(?:(\w+)?[ \t\f]*)?(?:(\w+)[ \t\f]*)?(\w+)?.*$'
"""Padrão separa a linha em três grupos: rótulo, mnemônico e operando"""
OPERAND_PATTERN = r'^(?:0[xb])?\d+$|^0c\w$'
"""Padrão que detecta um operando no formato 0xA, 0b0110 ou 0cD"""


@dataclass
class LineTokens:
  """
  Entidade que representa uma linha de código separada em tokens
  """
  label: str = None
  """Valor do campo rótulo (primeiro campo)"""
  mnemonic: str = None
  """Valor do campo mnemônico (segundo campo)"""
  operand: str = None
  """Valor do campo operando (terceiro campo)"""
  index: int = None
  """Índice da linha, posição da linha relativa ao início do programa"""
  mem_addr: int = None
  """Endereço da linha na memória"""
  
  
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
    """
    Executa montagem absoluta do código-fonte. A saída deste método é um
    programa-objeto absoluto

    Returns
    -------
    str
      Programa objeto absoluto
    """
    labels, instructions = self._tokenize() # primeiro passo
    self._decode_operands(lbl_tokens=labels, inst_tokens=instructions) # segundo passo
    
    origin = Word(instructions[0].mem_addr)
    
    # geração do programa objeto
    program_object = ''
    n_bytes = 0
    
    for instruction in instructions:
      mnemonic = instruction.mnemonic
      operand = instruction.operand
      label = instruction.label
      
      if operand is not None:
        if mnemonic == AssemblerInstructions.DATA:
          w = Word(operand)
          program_object += (
            ' ' + w.first_byte.to(self._output_base) + 
            ' ' + w.second_byte.to(self._output_base)
          )
          n_bytes += 2
        elif mnemonic == AssemblerInstructions.AREA:
          program_object += ' 00' * operand
          n_bytes += operand
        else:
          opcode = InstructionSet.get_opcode(mnemonic)
          inst = Word.from_instruction(opcode, operand)
          program_object += (
            ' ' + inst.first_byte.to(self._output_base) + 
            ' ' + inst.second_byte.to(self._output_base)
          )
          n_bytes += 2
      else:
        if mnemonic is None and label is not None: # ignora linhas em branco
          program_object += ' 00 00'
          n_bytes += 2
          
    n_bytes += 4 # end inicial (2), # of bytes (1), checksum (1)
    
    # inclusão da posição inicial e do número de bytes
    n_bytes = Byte(n_bytes)
    program_object = (
      origin.first_byte.to(self._output_base) + ' ' + 
      origin.second_byte.to(self._output_base) + ' ' + 
      n_bytes.to(self._output_base) +
      program_object
    )
    
    # inclusão do checksum
    cs = self._compute_checksum(program_object)
    program_object += ' ' + cs.to(self._output_base)
    
    if self._output_path:
      self._output_path.write_text(program_object)

    return program_object
  
  
  def _compute_checksum(self, program: str) -> Byte:
    """
    Calcula o checksum de um programa-objeto no formato de uma string

    Parameters
    ----------
    program : str
      Programa objeto no formato string com cada instrução separada por um
      espaço

    Returns
    -------
    Byte
      Valor no checksum
    """
    s = 0
    for byte in program.split(' '):
      s += Byte('0x' + byte).uint
    return Byte(-Byte(s).int)
    
    
  def _tokenize(self) -> Tuple[List[LineTokens], List[LineTokens]]:
    """
    Transforma o código-fonte recebido em uma lista de tokens

    Returns
    -------
    List[LineTokens], List[LineTokens]
      Tupla no formato (labels, instrucions), onde instructions é uma lista
      contendo todas as linhas do programa tokenizadas e labels é um subconjunto
      de instructions onde ``Linetokens.label`` é diferente de ``None``.
      A única vantagem da lista ``labels`` é poder iterar sob uma lista menor.
    """
    labels = []
    instructions = []
    
    orig_token = self._tokenize_line(
      line=self._program_lines[0], 
      line_index=0, 
      memory_offset=0
    )
    memory_offset = Word.convert_to_int(orig_token.operand)
    
    line_index = 0
    for line in self._program_lines[1:]: # discarta ORG
      tokens = self._tokenize_line(
        line=line, 
        line_index=line_index, 
        memory_offset=memory_offset
      )
      
      if tokens.label is None and tokens.mnemonic is None: 
        continue # ignora linhas em branco
      
      if tokens.label:
        labels.append(tokens)
        
      instructions.append(tokens)
      line_index += 2
    
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
      )
    
    return LineTokens(
      label=m.group(1),
      mnemonic=m.group(2),
      operand=m.group(3),
      index=line_index,
      mem_addr=memory_offset + line_index,
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

  prog = Path(__file__).parent.parent.parent / 'programs' / 'test_arit.asm'
  # prog = Path(__file__).parent / 'dumper.asm'
  prog = prog.read_text()
  a = Assembler(prog, output_base='x')
  obj = a.assemble()
  print(obj)