"""
To create a standalone executable for broh5
"""
import os
import subprocess
from pathlib import Path
import nicegui

cmd = [
    'python',
    '-m', 'PyInstaller',
    './broh5/main.py',
    '--name', 'broh5',
    '--onefile',
    '--hidden-import=matplotlib.backends.backend_svg',
    '--add-data', f'{Path(nicegui.__file__).parent}{os.pathsep}nicegui'
]
subprocess.call(cmd)