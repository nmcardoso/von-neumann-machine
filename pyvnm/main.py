from pathlib import Path

from vm.vnm import VonNeumannMachine


def main():
  vnm = VonNeumannMachine(memory_size=128)
  test_file = Path(__file__).parent.parent / 'test' / 'test_01.s'
  vnm.execute_program(test_file)
  



if __name__ == '__main__':
  main()