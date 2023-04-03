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
    
    
  def __repr__(self):
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
    else:
      self._value = Word.bin_to_int(
        Word.int_to_bin(
          Word.convert_to_int(new_value)
        )
      )
  
  
  @property
  def binary(self) -> str | None:
    """
    Converte a palavra para binário

    Returns
    -------
    str | None
      A representação binária da palavra
    """
    if self.value is None:
      return None
    return Word.int_to_bin(self._value)
  
  
  @staticmethod
  def bin_to_int(value: str) -> int:
    """
    Converte uma string contendo bits para um número inteiro

    Parameters
    ----------
    value : str
      String de bits

    Returns
    -------
    int
      Representação da string como número inteiro
    """
    return int(value, 2)
  
  
  @staticmethod
  def int_to_bin(value: int, extend: bool = True, word_size: int = None) -> str:
    """
    Converte um número inteiro para string de bits

    Parameters
    ----------
    value : int
      Valor do número inteiro a ser convertido
    extend : bool, opcional
      Indica se o valor recebido deve ser extendido com zeros à esquerda até
      o tamanho da palavra, por padrão ``True``
    word_size : int, opcional
      Tamanho da palavra, usado apenas se ``extend == True``, por padrão ``None``

    Returns
    -------
    str
      A representação binária do número inteiro inserido
    """
    if extend:
      extend_size = Word.size if word_size is None else word_size
      return format(value, f'0>{extend_size}b')[-extend_size:]
    return format(value, 'b')
  
  
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
    
    if value[:2] == '0b':
      return int(value, 2)
    elif value[:2] == '0x':
      return int(value, 16)
    else:
      return int(value) 



class Instruction(Word):
  """
  Representação de uma Instrução na memória

  Parameters
  ----------
  value : str | int | None
    Valor numérico da instrução
  """
  def __init__(self, value: str | int | None):
    super().__init__(value)
    word_bits = self.binary
    self._opcode = Word.bin_to_int(word_bits[:4])
    self._operand = Word.bin_to_int(word_bits[4:])
    
    
  def __repr__(self):
    return f'<Instruction {InstructionSet.get_name(self.opcode)} {self.operand}>'
    
  
  @property
  def opcode(self) -> int:
    """
    Retorna o código da operação da respectiva instrução

    Returns
    -------
    int
      Representação inteira do código da operação
    """
    return self._opcode
  
  
  @property
  def operand(self) -> int:
    """
    Retorna o operando da respectiva instrução

    Returns
    -------
    int
      Representação inteira do operando
    """
    return self._operand
  
  
  
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
  """Instrução ML (Jump multiplicação)"""
  DV = 0x7
  """Instrução DV (Divisão)"""
  LD = 0x8
  """Instrução LD (Load)"""
  ST = 0x9
  """Instrução ST (Store)"""
  SC = 0xA
  """Instrução JP (Subroutine Call)"""
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
  def get_name(cls, opcode: int) -> str:
    """
    Obtém o símbolo da instrução a partir de seu opcode

    Parameters
    ----------
    opcode : int
      O código da operação

    Returns
    -------
    str
      O símbolo correspondente
    """
    for name, code in cls.__dict__.items():
      if code == opcode:
        return name
    return None