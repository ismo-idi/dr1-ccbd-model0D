#!/usr/bin/env python3
"""Import complete maintained source files into LaTeX without copying their contents."""
from pathlib import Path
r=Path(__file__).resolve().parents[1]
files=[]
for folder in ['common/src','common/scripts','common/tests','demo/demo_1_no_obstacle/src','demo/demo_1_no_obstacle/tests','demo/demo_2_static_sphere/src','demo/demo_2_static_sphere/tests']:
    files += [p for p in (r/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
files += [r/'scripts'/n for n in ['build.sh','setup.sh','setup_demo.sh','launch_demo.sh','demo_control.sh','verify_demo.sh','verify_unit.sh','reproduce_clean.sh','build_tutorials.sh','build_kinematic_tutorial.sh','kinematic_listings.py']]
files += [r/'references/demo-packages.txt']
text='\\section{Complete first-party source listings}\n'
text+='These listings import the delivered files directly. Generated mesh coordinates are represented by the complete generator and separately hashed assets.\\par\n'
for i,p in enumerate(sorted(set(files)),1):
    rel=p.relative_to(r).as_posix()
    text+='\\subsection*{File '+str(i)+'}\n\\noindent{\\small\\path{'+rel+'}}\\par\n'
    text+='\\lstinputlisting{../../../'+rel+'}\n'
(r/'tutorial/source/kinematic_demos/listings.tex').write_text(text)
print('Imported',len(set(files)),'source files for kinematic_demos')
