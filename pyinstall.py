# pyinstall.py

import PyInstaller.__main__

PyInstaller.__main__.run([
    './Beginner/signalgui1.py',
    '--windowed',
    '--noconsole',
    '--icon=icon.png',
])
