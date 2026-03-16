"""Helper script to build the application with PyInstaller."""

import PyInstaller.__main__

args = [
    "main.py",
    "--onefile",
    "--windowed",
    "--name=ShadowFight2EasySwitch",
    "--icon=ui/icon/icon.ico",
    "--add-data=ui/qss_sheet/style.qss;ui/qss_sheet",
    "--add-data=config/settings.json;config",
    "--clean",
    "--exclude-module=PyQt6",
]

PyInstaller.__main__.run(args)
