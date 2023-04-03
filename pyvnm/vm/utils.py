class Lock:
  """
  Representação de um cadeado para implementação da lógica de bloqueio
  de um determinado recurso
  
  Attribute
  ---------
  _locked: bool
    Representa o estado travado/destravado
  """
  def __init__(self):
    self._locked = False
    
    
  def aquire(self):
    """
    Trava o cadeado
    """
    self._locked = True
    
  
  def release(self):
    """
    Destrava o cadeado
    """
    self._locked = False
    
  
  def is_locked(self) -> bool:
    """
    Verifica se o cadeado está travado

    Returns
    -------
    bool
      ``True`` se o cadeado estiver travado, ``False`` caso contrário.
    """
    return self._locked