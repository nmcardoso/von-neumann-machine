from pathlib import Path
from typing import Dict

from .memory import Byte, Word


class Device:
  """
  Interface que representa um hardware periférico de entrada e saída de dados
  """
  def read(self) -> Word:
    """
    Lê dados do dispositivo
    
    Returns
    -------
    Word
      Palavra recebida pelo periférico
    """
    pass


  def write(self, data: Word):
    """
    Escreve dados no dispositivo
    
    Parameters
    ----------
    data: Word
      Palavra a ser escrita no dispositivo
    """
    pass
  
  
  
class Screen(Device):
  def write(self, data: Word):
    print('>> Saída:', data.int)
    
    
    
class CharScreen(Device):
  def __init__(self):
    self._buffer = ''
   
    
  def write(self, data: Word):
    if data.value == 4:
      print('>>', self._buffer)
      self._buffer = ''
    else:
      self._buffer += chr(data.value)



class Keyboard(Device):
  def read(self) -> Word:
    data = input('>> Digite um numero: ')
    return Word(data)



class HardDisk(Device):
  """
  Representa um disco rígido. Permite operações de entrada e saída a partir
  de manipulação de arquivos no programa assembly pelas instruções PD e GD.

  Parameters
  ----------
  input_data: str, optional
    Dado de entrada a ser lido, geralmente o programa a ser executado.
  output_path: str | Path, optional
    Caminho da saída de dados.
  """
  def __init__(self, input_data: str = None, output_path: str | Path = None):
    self.output_path = Path(output_path) if output_path else None
    self.input_data = None if not input_data else input_data.split(' ')
    self.output_data = ''
    self._cursor = 0
    
    
  def read(self) -> Byte:
    if self._cursor < len(self.input_data):
      b = Byte('0x' + self.input_data[self._cursor])
      self._cursor += 1
      return b
    
    
  def write(self, data: Word):
    self.output_data += data.second_byte.hex + ' '
    
    
  def save(self):
    self.output_path.write_text(self.output_data.rstrip())
    



class DeviceBus:
  """
  Abstração de um bus de dispositivos. É possível acessar qualquer um dos
  dispositivos registrados a partir desta classe
  
  Attributes
  ----------
  devices: Dict[int, Device]
    Dicionário usado para mapear todos os disposivos de entrada/saída
  """
  def __init__(self):
    self._devices: Dict[int, Device] = {}
    
  
  def add(self, code: int, device: Device):
    """
    Adiciona um novo dispositivo no bus

    Parameters
    ----------
    code : int
      Código do dispositivo (máx 16bits)
    device : Device
      Dispositivo a ser adicionado
    """
    self._devices[code] = device
    
    
  def remove(self, code: int):
    """
    Remove um dispositivo do bus

    Parameters
    ----------
    code : int
      Código do dispositivo a ser removido
    """
    del self._devices[code]
    
    
  def get(self, code: int) -> Device | None:
    """
    Obtém um disposivo a partir de seu código

    Parameters
    ----------
    code : int
      Código do dispositvo a ser retornado

    Returns
    -------
    Device | None
      O dispositivo requisitado, se o código constar no mapa de disposivo,
      ``None`` caso contrário
    """
    return self._devices.get(code, None)