class Word:
  size = 16
  
  def __init__(self, value: str | int | None = None):
    self.value = value
    
    
  def __repr__(self):
    return f'<Word {self.value}>'
  
  
  @property
  def value(self) -> int | None:
    return self._value
  
  
  @value.setter
  def value(self, new_value: str | int | None):
    if new_value is None:
      self._value = None
    else:
      self._value = Word.bin_to_int(
        Word.int_to_bin(
          Word.convert_to_int(new_value)
        )
      )
  
  
  @property
  def binary(self) -> str | None:
    if self.value is None:
      return None
    return Word.int_to_bin(self._value)
  
  
  @staticmethod
  def bin_to_int(value: str) -> int:
    return int(value, 2)
  
  
  @staticmethod
  def int_to_bin(value: int, extend: bool = True, word_size: int = None) -> str:
    if extend:
      extend_size = Word.size if word_size is None else word_size
      return format(value, f'0>{extend_size}b')[-extend_size:]
    return format(value, 'b')
  
  
  @staticmethod
  def convert_to_int(value: str | int) -> int:
    if isinstance(value, int):
      return value
    
    if value[:2] == '0b':
      return int(value, 2)
    elif value[:2] == '0x':
      return int(value, 16)
    else:
      return int(value)



class ControlWord(Word):
  MEMORY_START = 0x0
  INSTRUCTIONS_BEGIN = 0x1
  INSTRUCTIONS_END = 0x2
  CODE_ENTRYPOINT = 0x3
  
  def __init__(self, value: str | int | None, kind: int):
    super().__init__(value)
    self._type = kind
    
    
  def __repr__(self):
    return f'<ControlWord {self.value}>'
  
  
  @property
  def value(self) -> int | None:
    return self._value
  
  
  @value.setter
  def value(self, new_value: str | int | None):
    self._value = new_value    



class Instruction(Word):
  def __init__(self, value: str | int | None):
    super().__init__(value)
    word_bits = self.binary
    self._opcode = Word.bin_to_int(word_bits[:4])
    self._operand = Word.bin_to_int(word_bits[4:])
    
    
  def __repr__(self):
    return f'<Instruction {InstructionSet.get_name(self.opcode)}>'
    
  
  @property
  def opcode(self) -> int:
    return self._opcode
  
  
  @property
  def operand(self) -> int:
    return self._operand
  
  
  
class InstructionSet:
  JP = 0x0
  RS = 0x0
  JZ = 0x1
  JN = 0x2
  HJ = 0x3
  AD = 0x4
  SB = 0x5
  ML = 0x6
  DV = 0x7
  LD = 0x8
  ST = 0x9
  SC = 0xA
  GD = 0xB
  PD = 0xC
  OS = 0xD
  
  @classmethod
  def get_opcode(cls, symbol: str) -> int:
    return cls.__dict__.get(symbol, None)
  
  
  @classmethod
  def get_name(cls, opcode: int) -> str:
    for name, code in cls.__dict__.items():
      if code == opcode:
        return name
    return None