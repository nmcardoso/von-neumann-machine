from abc import abstractmethod
from typing import List

from .isa import Word


class Memory:
  def __init__(self, size: int):
    self._size = size
    self._data = [Word(None) for _ in range(size)]
    
  
  @property
  def size(self) -> int:
    return self._size
  
  
  def read(self, position: int) -> Word:
    self._check_valid_position(position)
    
    return self._data[position]
  
  
  def write(self, position: int, data: Word | List[Word]):
    self._check_valid_position(position)
    
    if isinstance(data, list):
      for i, d in enumerate(data, start=position):
        self._data[i] = d
    else:
      self._data[position] = data
      
  
  def _check_valid_position(self, position: int):
    if position < 0 or position >= self._size:
      raise ValueError(f'Acessando uma posicao invalida da memoria: {position}')