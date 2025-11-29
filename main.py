import sys

import python.res.resources_rc
import vtkmodules.util.data_model
import vtkmodules.util.execution_model
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QApplication

from python.core.core_functions import make_dir
from python.ui.page_level_ui_widgets import ToolMainWindow


if __name__ == '__main__':
    QApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_CompressHighFrequencyEvents, True)
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QtWidgets.QApplication(sys.argv)
    make_dir()
    app.setStyle('windowsvista')
    app.setWindowIcon(QtGui.QIcon(u':/icons/icon'))
    main = ToolMainWindow()
    main.show()
    sys.exit(app.exec())
