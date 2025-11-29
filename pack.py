"""
Pack To Release
按需使用
"""
import PyInstaller.__main__

args = [
    'main.py',
    '--onefile',
    '--windowed',
    '--name=ShadowFight2EasySwitch',
    '--hidden-import=vtkmodules',
    '--icon=ui/icon/icon.png',
    '--clean',
    '--exclude-module=PyQt6'
]

PyInstaller.__main__.run(args)
