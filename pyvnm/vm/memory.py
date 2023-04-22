from typing import List

import numpy as np

from .isa import Byte, Word


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
    self._data = np.empty(shape=(self._size, 8))
    self._data.fill(np.nan)
    
  
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
    byte = self._data[address : address + 2].flatten()
    if len(np.argwhere(np.isnan(byte))) != 0:
      return Word(None)
    byte_str = ''.join(byte.tolist())
    return Word('0b' + byte_str)
    # return self._data[address]
  
  
  def write(self, position: int, data: Word):
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
    bits = np.array(list(data.bin)).reshape(shape=(2, 8))
    self._data[position : position+2, : ] = bits
      
      
  def write_byte(self, position: int, data: Byte):
    self._data[position, : ] = list(data.bin)
      
  
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