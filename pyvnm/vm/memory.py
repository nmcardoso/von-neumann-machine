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
      
      
  def get_first_word_address(self):
    return next(i for i, word in enumerate(self._data) if not word.is_empty())
  
  
  def get_last_word_address(self):
    x = next(i for i, word in enumerate(self._data[::-1]) if not word.is_empty())
    return len(self._data) - x
      
  
  def _check_valid_position(self, position: int):
    if position < 0 or position >= self._size:
      raise ValueError(f'Acessando uma posicao invalida da memoria: {position}')