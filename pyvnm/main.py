import argparse
from pathlib import Path

from vm.vnm import VonNeumannMachine


def cli():
  p = argparse.ArgumentParser(prog='Simulador da Maquina de Von Neumann')
  # p.add_argument('-e', )


def main():
  vnm = VonNeumannMachine(memory_size=128)
  test_file = Path(__file__).parent.parent / 'programs' / 'test_02.hex'
  vnm.execute_program(test_file)
  



if __name__ == '__main__':
  main()