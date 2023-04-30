import itertools
from typing import List, Literal

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
  
  
  def is_instruction(self) -> bool:
    return self._value is not None
  
  
  def to(self, base: Literal['x', 'hex', 'b', 'bin', 'd', 'dec', 'int', 'uint']):
    if base in ('x', 'hex'):
      return self.hex
    elif base in ('b', 'bin'):
      return self.bin
    elif base in ('d', 'dec', 'int'):
      return self.int
    elif base in ('uint'):
      return self.uint
  
  
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
        uint_value = int_value & ((1 << self.size) - 1)
      
      # converte a palavra pra binário, trunca p/ 16 bits menos significativos
      # e faz a conversão para todas as outras bases de acordo com a palavra
      # truncada em bits
      bin_value = np.binary_repr(uint_value, width=self.size)[-self.size:]
      # print('W:', uint_value, bin_value, self.size)
      uint_value = int(bin_value, 2)
      sint_value = uint_value if uint_value < 2 ** self.size / 2 else uint_value - 2 ** self.size 
      hex_value = np.base_repr(uint_value, base=16)
      hex_value = '0' * (int(self.size / 4) - len(hex_value)) + hex_value
      
      self.bin = bin_value
      self.uint = uint_value
      self.int = sint_value
      self.hex = hex_value
      self._value = uint_value
      
      
  @property
  def first_byte(self):
    return Byte('0b' + self.bin[:8])
  
  
  @property
  def second_byte(self):
    return Byte('0b' + self.bin[8:])
  
  
  @property
  def two_complement(self) -> int:
    if (self.uint & (1 << (self.size - 1))) != 0:
      return self.uint - (1 << self.size)
    return self.uint
      
  
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
  def from_instruction(opcode: int, operand: int):
    opcode_bits = format(opcode, f'0>{4}b')[-4:]
    operand_bits = format(operand, f'0>{12}b')[-12:]
    instruction_bits = '0b' + opcode_bits + operand_bits
    return Word(instruction_bits)
  
  
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
  def __init__(self, value: str | int | None = None):
    self.size = 8
    super().__init__(value)


class Memory:
  """
  Memória de dados e de programa. Armazena toda informação não-persistente
  da máquina
  
  Parameters
  ----------
  size: int
    Número de endereços da memória
    
  Attributes
  ----------
  _data: List[Word]
    Estrutura de dados usada para armazenar todo conteúdo da memória 
  """
  def __init__(self, size: int):
    self._size = size
    # self._data = [Word(None) for _ in range(size)]
    self._data = [[None]*8]*size
    
  
  @property
  def size(self) -> int:
    """
    O número de posições da memória

    Returns
    -------
    int
      O número de posições da memória
    """
    return self._size
  
  
  def read(self, address: int) -> Word:
    """
    Ler o conteúdo de um endereço específico da memória

    Parameters
    ----------
    address : int
      Endereço a ser lido

    Returns
    -------
    Word
      Conteúdo contido no endereço especificado
    """
    self._check_valid_position(address)
    byte = list(itertools.chain(*self._data[address : address+2]))
    try:
      byte.index(None)
      return Word(None)
    except:
      byte_str = ''.join(map(str, byte))
      return Word('0b' + byte_str)
    # return self._data[address]
  
  
  def write(self, address: int, data: Word):
    """
    Escrever conteúdo em um endereço específica da memória

    Parameters
    ----------
    address : int
      Endereço a ser escrito
    data: Word | List[Word]
      Palavra ou lista de palavras a serem escritas na memória
    """
    self._check_valid_position(address)
    self._data[address] = list(map(int, data.first_byte.bin))
    self._data[address+1] = list(map(int, data.second_byte.bin))
      
      
  def write_byte(self, address: int, data: Byte):
    self._data[address] = list(map(int, data.bin))
    
    
  def hexdump(self, colors):

    print('      ', sep='', end='')
    for i in range(16):
      print(colors.LIGHT_YELLOW + format(i, '0>1x') + '  ' + colors.RESET, sep='', end='')
    print()
    for i in range(self.size // 32):
      print(colors.LIGHT_YELLOW + format(i*16, '0>4x') + ':' + colors.RESET, ' ', sep='', end='')
      for j in range(0, 16, 2):
        w = self.read(i*16 + j)
        if w.value is None:
          instruction = format(0, '0>4x')
          print(instruction[:2] + ' ' + instruction[2:], ' ', sep='', end='')
        else:
          instruction = format(w.value, '0>4x')
          print(colors.LIGHT_GREEN + instruction[:2] + ' ' + instruction[2:] + colors.RESET, '', sep=' ', end='')
      print()
      
  
  def _check_valid_position(self, address: int):
    """
    Verifica se uma determinado endereço existe na memória

    Parameters
    ----------
    address : int
      Endereço pesquisado
      
    Raises
    ------
    ValueError
      Erro jogado caso haja tentativa de acesso à uma posição inválida
    """
    if address < 0 or address >= self._size:
      raise ValueError(f'Acessando uma posicao invalida da memoria: {address}')