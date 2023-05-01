Executar o programa
===================

Na pasta von-neumann-machine, executar o comando:


```sh
cd pyvnm
python3 main.py -m 1024 -c --debug --sysdebug --dump ../programs/test_02.dump.hex -e ../programs/test_02.hex
```


Executar o assembly
===================

Na pasta von-neumann-machine, executar o comando:


```sh
python3 -m pyvnm.system.assembler
```