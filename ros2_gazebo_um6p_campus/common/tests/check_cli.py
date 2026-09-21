#!/usr/bin/env python3
"""Invalid commands must explain the error, never silently start or exit."""
import subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[2]
for args in ([],['3'],['1','guibash','scripts/demo_control.sh','start'],['2','bad']):
    p=subprocess.run(['bash',str(root/'scripts/launch_demo.sh'),*args],capture_output=True,text=True,timeout=5)
    assert p.returncode==2 and 'Terminal A:' in p.stderr and 'Terminal B:' in p.stderr
print('PASS: four invalid launch commands return actionable two-terminal instructions')
