from setuptools import find_packages, setup

setup(
  name='pyvnm',
  version='0.1',
  description='Simulador da Máquina de Von Neymann',
  packages=find_packages(),
  install_requires=[
    'wheel',
  ],
  extras_require={
    'docs': [
      'Jinja2>=3.1',
      'sphinxcontrib-napoleon',
      'sphinx',
      'furo',
      'ipykernel',
      'sphinx_copybutton',
    ]
  }
)