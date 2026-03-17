"""
Application entry point that configures Qt, applies styles and shows the startup window.
"""

import sys

import python.res.resources_rc
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QApplication

from python.core.core_functions import get_dir, make_dir
from python.ui.startup_page import StartupWindow


if __name__ == '__main__':
    QApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_CompressHighFrequencyEvents, True)
    QApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_ShareOpenGLContexts, True)
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QtWidgets.QApplication(sys.argv)
    make_dir()
    try:
        with open(get_dir("./ui/qss_sheet/style.qss"), "r", encoding="utf-8") as qss_file:
            app.setStyleSheet(qss_file.read())
    except Exception:
        app.setStyle('windowsvista')
    app.setWindowIcon(QtGui.QIcon(u':/icons/icon'))

    # show startup loading page before entering the main tool window
    startup = StartupWindow()
    startup.start()

    sys.exit(app.exec())
