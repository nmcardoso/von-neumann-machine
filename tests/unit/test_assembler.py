import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'pyvnm'))

from pyvnm.vm.io import Assembler

PROGRAMS_PATH = Path(__file__).parent.parent / 'programs'



class TestAssember(unittest.TestCase):
  def setUp(self) -> None:
    programs = list(PROGRAMS_PATH.glob('*.s'))
    programs_path = [p.parent / (p.stem + '.s') for p in programs]
    hexbytecodes_path = [p.parent / (p.stem + '.hexbytecode') for p in programs]
    binbytecodes_path = [p.parent / (p.stem + '.binbytecode') for p in programs]
    self.programs = [p.read_text() for p in programs_path]
    self.hexbytecodes = [p.read_text().strip() for p in hexbytecodes_path]
    self.binbytecodes = [p.read_text().strip() for p in binbytecodes_path]

  
  def test_hex_assemble(self):
    for program, expected_bytecode in zip(self.programs, self.hexbytecodes):
      a = Assembler(program=program)
      bytecode = a.assemble()
      self.assertEqual(bytecode, expected_bytecode)
      
  
  def test_bin_assemble(self):
    for program, expected_bytecode in zip(self.programs, self.binbytecodes):
      a = Assembler(program=program, output_base='b')
      bytecode = a.assemble()
      self.assertEqual(bytecode, expected_bytecode)
    
    
    
if __name__ == '__main__':
  unittest.main()