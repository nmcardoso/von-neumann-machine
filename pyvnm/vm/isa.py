import numpy as np


class Word:
  """
  Representação de uma palavra na memória e nos registradores.

  Attributes
  ----------
  size: int
    Tamanho da palavra em bits
    
  Parameters
  ----------
  value: str
    Valor a ser armazenado na palavra
  """
  size = 16
  
  def __init__(self, value: str | int | None = None):
    self.value = value
    
    
  def __repr__(self) -> str:
    if self.value is None:
      return '<Empty>'
    return f'<Word {self.value}>'
  
  
  def is_empty(self) -> bool:
    """
    Varifica se a palavra nunca foi inicializada pelo carregador

    Returns
    -------
    bool
      ``True`` se a palavra é vazia (= None),  ``False`` caso contrário
    """
    return self.value is None
  
  
  @property
  def value(self) -> int | None:
    """
    Retorna o valor armazenado na palavra na representação inteira

    Returns
    -------
    int | None
      O valor inteiro da palavra ou ``None``, caso ela nunca tenha sido
      inicializada
    """
    return self._value
  
  
  @value.setter
  def value(self, new_value: str | int | None):
    """
    Altera a propriedade valor para atualzar seu valor. Efetua conversões
    de tipos de dados e overflow, de forma que o valor a ser armazenado
    seja os n bits menos significativos, onde n é o tamanho da palavra.

    Parameters
    ----------
    new_value : str | int | None
      Valor a ser armazenado
    """
    if new_value is None:
      self._value = None
      self.bin = None
      self.uint = None
      self.int = None
      self.hex = None
    else:
      int_value = Word.convert_to_int(new_value)
      if int_value >= 0:
        uint_value = int_value
      else: 
        uint_value = int_value & ((1 << Word.size) - 1)
      
      # converte a palavra pra binário e trunca p/ 16 bits menos significativos
      bin_value = np.binary_repr(uint_value, width=Word.size)[-Word.size:]
      uint_value = int(bin_value, 2)
      sint_value = uint_value if uint_value < 2 ** Word.size / 2 else uint_value - 2 ** Word.size 
      hex_value = np.base_repr(uint_value, base=16)
      
      self.bin = bin_value
      self.uint = uint_value
      self.int = sint_value
      self.hex = hex_value
      self._value = uint_value
      
  
  @property
  def opcode(self):
    """
    Retorna o código da operação da respectiva instrução

    Returns
    -------
    int
      Representação inteira do código da operação
    """
    return int(self.bin[:4], 2)
  
  
  @property
  def operand(self):
    """
    Retorna o operando da respectiva instrução

    Returns
    -------
    int
      Representação inteira do operando
    """
    return int(self.bin[4:], 2)
  
  
  @staticmethod
  def convert_to_int(value: str | int) -> int:
    """
    Converte uma string para um objeto do tipo inteiro. A base é infeira
    de acordo com a seguinte convensão:
    
    - Números representados na base binária devem começar com os caracteres 
    ``0b``, por exemplo: ``0b10101010``; 
    - Números representados na base hexadecimal devem começar com os
    caracteres  ``0x``, por exemplo: ``0xfa``;
    - Números sem prefixo serão considerados decimais.

    Parameters
    ----------
    value : str | int
      Número a ser representado como inteiro

    Returns
    -------
    int
      Valor inteiro do número indicado após a conversão de base
    """
    if isinstance(value, int):
      return value
    
    if value[:2].lower() == '0b':
      return int(value, 2)
    elif value[:2].lower() == '0x':
      return int(value, 16)
    elif value[:2].lower() == '0c':
      return ord(value[2])
    else:
      return int(value)



class Byte(Word):
  size = 8
  
  
  
class InstructionSet:
  JP = 0x0
  """Instrução JP (Jump uncondicional)"""
  RS = 0x0
  """Instrução RS (Return from subroutine)"""
  JZ = 0x1
  """Instrução JZ (Jump if acc = 0)"""
  JN = 0x2
  """Instrução JN (Jump if acc < 0)"""
  HJ = 0x3
  """Instrução HJ (Jump after halt)"""
  AD = 0x4
  """Instrução AD (Adição)"""
  SB = 0x5
  """Instrução SB (Subtração)"""
  ML = 0x6
  """Instrução ML (Multiplicação)"""
  DV = 0x7
  """Instrução DV (Divisão)"""
  LD = 0x8
  """Instrução LD (Load)"""
  ST = 0x9
  """Instrução ST (Store)"""
  SC = 0xA
  """Instrução SC (Subroutine Call)"""
  GD = 0xB
  """Instrução GD (Get Data)"""
  PD = 0xC
  """Instrução PD (Put Data)"""
  OS = 0xD
  """Instrução OS (Chamada no sistema operacional)"""
  
  
  @classmethod
  def get_opcode(cls, symbol: str) -> int:
    """
    Obtém o código da operação (opcode) a partir de seu símbolo

    Parameters
    ----------
    symbol : str
      Símbolo do opcode buscado

    Returns
    -------
    int
      Valor do opcode
    """
    return cls.__dict__.get(symbol, None)
  
  
  @classmethod
  def get_mnemonic(cls, opcode: int) -> str:
    """
    Obtém o mnemônico da instrução a partir de seu opcode

    Parameters
    ----------
    opcode : int
      O código da operação

    Returns
    -------
    str
      O mnemônico correspondente
    """
    for name, code in cls.__dict__.items():
      if code == opcode:
        return name
    return None