from typing import Dict

from .isa import Word


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
    print('>>', data.value)



class Keyboard(Device):
  def read(self) -> Word:
    data = input('>> Digite um numero: ')
    return Word(data)

  
  
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