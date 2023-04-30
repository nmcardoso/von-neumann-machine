class OS:
  SIG_TERM = 15
  SIG_TRAP = 5
  LOADER_CHECKSUM_MISSMATCH = 400
  flags = set()

  
  @classmethod
  def codes(cls):
    return list(cls.__dict__.values())