class Lock:
  def __init__(self):
    self._locked = False
    
    
  def aquire(self):
    self._locked = True
    
  
  def release(self):
    self._locked = False
    
  
  def is_locked(self):
    return self._locked