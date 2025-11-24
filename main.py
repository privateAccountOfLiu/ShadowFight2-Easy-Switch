import sys

from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtWidgets import QApplication

from python.core.core_functions import make_dir, get_dir
from python.ui.basic_ui_widget import ToolMainWindow

if __name__ == '__main__':
    QApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_CompressHighFrequencyEvents, True)
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QtWidgets.QApplication(sys.argv)
    make_dir()
    app.setStyle('windowsvista')
    app.setWindowIcon(QtGui.QIcon(get_dir('./res/ui/icon/icon.png')))
    main = ToolMainWindow()
    main.show()
    sys.exit(app.exec())
