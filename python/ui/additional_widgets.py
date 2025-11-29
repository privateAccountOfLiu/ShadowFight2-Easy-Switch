import tempfile

import pyvista as pv
import vtk
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (QVBoxLayout, QWidget)
from pyvistaqt import QtInteractor

from python.core.core_functions import *
from python.ui.notice_dialog_widgets import ErrorDialog


class ObjModelViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.plotter = QtInteractor(parent=parent, auto_update=True)
        self.mesh = pv.Box()
        self.reader = vtk.vtkOBJReader()
        layout.addWidget(self.plotter)
        self.setLayout(layout)
        self.mesh_show()

    def add_mesh(self, content):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.obj', delete=False) as temp:
            temp.write(content)
        self.mesh = pv.read(temp.name)
        self.mesh_show()
        os.unlink(temp.name)

    def mesh_show(self):
        self.plotter.clear()
        try:
            self.plotter.add_mesh(self.mesh, show_edges=True, texture=False)
            self.plotter.add_axes()
            self.plotter.show_grid()
            self.plotter.view_isometric()
        except Exception as e:
            ErrorDialog(self, e)

    def hideEvent(self, event):
        try:
            if hasattr(self, 'plotter') and self.plotter:
                self.plotter.close()
                self.layout().removeWidget(self.plotter)
                self.plotter.deleteLater()
                self.plotter = None
            super().hideEvent(event)
        except Exception as e:
            ErrorDialog(self, e)

    def closeEvent(self, event):
        try:
            if hasattr(self, 'plotter') and self.plotter:
                self.plotter.close()
                self.layout().removeWidget(self.plotter)
                self.plotter.deleteLater()
                self.plotter = None
            super().closeEvent(event)
        except Exception as e:
            ErrorDialog(self, e)

    def showEvent(self, event):
        try:
            super().showEvent(event)
            if not hasattr(self, 'plotter') or self.plotter is None:
                self.plotter = QtInteractor(auto_update=True)
                self.layout().addWidget(self.plotter)
            self.mesh_show()
            self.plotter.render()
        except Exception as e:
            ErrorDialog(self, e)


class WorkerThread(QThread):
    finished = Signal()

    def __init__(self, source_dir, target_dir, target_fun):
        super().__init__()
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.target_fun = target_fun

    # noinspection PyUnresolvedReferences
    def run(self):
        self.target_fun()
        # self.finished.emit()
