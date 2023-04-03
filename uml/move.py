import os
from pathlib import Path

path = Path(__file__).parent
out_path = path / 'out'
out_path.mkdir(exist_ok=True, parents=True)

FORMAT = '.eps'
# classes_path = out_path / f'classes{FORMAT}'
# packages_path = out_path / f'package{FORMAT}'

# files = list(path.glob('*.puml'))

# for f in files:
#   cmd = f'plantuml -t{FORMAT[1:]} -o out {str(f.relative_to(path))}'
#   print(cmd)
#   os.system(cmd)
  
#   dest_path = out_path / f'{f.stem}{FORMAT}'
#   if classes_path.exists():
#     os.system(f'mv {str(classes_path.resolve())} {str(dest_path.resolve())}')
#   elif packages_path.exists():
#     os.system(f'mv {str(packages_path.resolve())} {str(dest_path.resolve())}')


out_path = path.parent / 'out' / 'uml'
for folder in out_path.glob('*'):
  fname = 'classes' if (out_path / folder.name / f'classes{FORMAT}').exists() else 'packages'
  cmd = f'mv {out_path / folder.name / f"{fname}{FORMAT}"} {str(path / "out" / f"{folder.name}{FORMAT}")}'
  # print(cmd)
  os.system(cmd)
os.system(f'rm -rf {out_path.parent}')