#!/usr/bin/env python3
"""Import complete maintained source files into LaTeX without copying their contents."""
from pathlib import Path
r=Path(__file__).resolve().parents[1]
files=[]
for folder in ['campus_environment/src','campus_environment/scripts','campus_environment/tests','.vscode']:
    files += [p for p in (r/folder).rglob('*') if p.is_file() and (p.suffix in ('.py','.sh','.xml','.sdf','.config','.yaml','.json') or p.name=='CMakeLists.txt') and '__pycache__' not in p.parts]
files += [r/'scripts'/n for n in ['build.sh','check_environment.sh','setup.sh','setup_demo.sh','setup_native.sh','launch_environment.sh','launch_paused.sh','verify.sh','reproduce_clean.sh','build_tutorial.sh','build_tutorials.sh','tutorial_listings.py']]
files += [r/'references'/n for n in ['native-packages.txt','demo-packages.txt','documentation-packages.txt','observed-direct-package-pins.txt']]
text='\\section{Complete first-party source listings}\n'
text+='These listings import the delivered files directly. Generated mesh coordinates are represented by the complete generator and separately hashed assets.\\par\n'
for i,p in enumerate(sorted(set(files)),1):
    rel=p.relative_to(r).as_posix()
    text+='\\subsection*{File '+str(i)+'}\n\\noindent{\\small\\path{'+rel+'}}\\par\n'
    text+='\\lstinputlisting{../../../'+rel+'}\n'
(r/'tutorial/source/campus_environment/listings.tex').write_text(text)
print('Imported',len(set(files)),'source files for campus_environment')
