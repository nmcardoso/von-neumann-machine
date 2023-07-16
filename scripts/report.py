template = lambda cmd : f"""
\subsubsection{{Comando {cmd}}}
\\label{{sec:cli-{cmd}}}
A Fig. \\ref{{fig:cli-{cmd}}} mostra o fluxograma da implementação do método \\texttt{{action\_{cmd}}} da classe \\texttt{{Terminal}}, correspondente à ação executada pelo comando {cmd}.

\\begin{{figure}}[!ht]
    \\centering
    \\includegraphics[width=0.95\\textwidth]{{figures/terminal_{cmd}}}
    \\caption{{Fluxograma da ação performada pelo comando {cmd}. Os métodos e atributos acessados são os mesmos mostrados nos diagramas de classes. Consulte as Figs. \\ref{{fig:terminal}} e \\ref{{fig:diagrama-classes}} para mais detalhes.}}
    \\label{{fig:cli-{cmd}}}
\end{{figure}}
"""

cmds = ['APA', 'ASM', 'CRF', 'DLF', 'DMP', 'END', 'EXC', 'LIN', 'LOD', 'LRL', 'MEM', 'REG', 'RUN', 'SDR', 'SET', 'SIO', 'UDR']

for cmd in cmds:
  print(template(cmd))