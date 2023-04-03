from typing import List

from .isa import Word


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
    self._data = [Word(None) for _ in range(size)]
    
  
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
    Ler o conteúdo de um endereço específica da memória

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
    return self._data[address]
  
  
  def write(self, position: int, data: Word | List[Word]):
    """
    Escrever conteúdo em um endereço específica da memória

    Parameters
    ----------
    address : int
      Endereço a ser escrito
    data: Word | List[Word]
      Palavra ou lista de palavras a serem escritas na memória
    """
    self._check_valid_position(position)
    
    if isinstance(data, list):
      for i, d in enumerate(data, start=position):
        self._data[i] = d
    else:
      self._data[position] = data
      
      
  def get_first_word_address(self) -> int:
    """
    Método de utilidade que retorna a posição na memória da primeira palavra
    não nula

    Returns
    -------
    int
      Endereço da memória da primeira palavra não nula
    """
    return next(i for i, word in enumerate(self._data) if not word.is_empty())
  
  
  def get_last_word_address(self) -> int:
    """
    Método de utilidade que retorna a posição na memória da última palavra
    não nula

    Returns
    -------
    int
      Endereço da memória da última palavra não nula
    """
    x = next(i for i, word in enumerate(self._data[::-1]) if not word.is_empty())
    return len(self._data) - x
      
  
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