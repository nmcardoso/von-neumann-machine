from abc import abstractmethod
from typing import Dict

from .isa import Word


class Device:
  def read(self) -> Word:
    pass


  def write(self, data: Word):
    pass
  
  
  
class Screen(Device):
  def write(self, data: Word):
    print(data.value)



class Keyboard(Device):
  def read(self) -> Word:
    data = input('>> Digite um numero: ')
    return Word(data)

  
  
class Devices:
  def __init__(self):
    self._devices: Dict[int, Device] = {}
    
  
  def add(self, code: int, device: Device):
    self._devices[code] = device
    
    
  def remove(self, code: int):
    del self._devices[code]
    
    
  def get(self, code: int) -> Device | None:
    return self._devices.get(code, None)