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
    # 使用 .ico 图标，确保 Windows 任务栏图标正确
    '--icon=ui/icon/icon.ico',
    # 打包 QSS 样式表，保证一文件模式下也能加载
    '--add-data=ui/qss_sheet/style.qss;ui/qss_sheet',
    '--clean',
    '--exclude-module=PyQt6',
]

PyInstaller.__main__.run(args)
