import tempfile

import numpy as np
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget, QFrame
import pyqtgraph as pg
import pyqtgraph.opengl as gl

from python.core.core_classes import Obj
from python.core.core_functions import *
from python.ui.notice_dialog_widgets import ErrorDialog


class ObjModelViewer(QWidget):
    """3D OBJ model preview widget implemented with pyqtgraph.opengl."""

    def __init__(self, parent=None):
        super().__init__(parent)
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        frame = QFrame(self)
        frame.setObjectName("modelViewerFrame")
        frame.setStyleSheet(
            "#modelViewerFrame {"
            "  background-color: rgb(245,246,248);"
            "  border: 1px solid #4b5563;"
            "  border-radius: 8px;"
            "}"
        )

        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(4, 4, 4, 4)

        self.view = gl.GLViewWidget(frame)
        self.view.setBackgroundColor((245, 246, 248))
        self.view.opts['distance'] = 10
        frame_layout.addWidget(self.view)

        outer_layout.addWidget(frame)
        self.setLayout(outer_layout)

        self.mesh_item = None

    def add_mesh(self, content: str) -> None:
        """Parse OBJ text content and display it as a mesh in the 3D view."""
        try:
            obj = Obj.build_obj(content)
            if obj is None or not obj.data['v '] or not obj.data['f ']:
                return

            vertices = np.array(obj.data['v '], dtype=float)

            faces = []
            for face in obj.data['f ']:
                idx = []
                for token in face:
                    part = token.split('/')[0]
                    idx.append(int(part) - 1)
                if len(idx) == 3:
                    faces.append(idx)

            if not faces:
                return

            faces = np.array(faces, dtype=int)

            if self.mesh_item is not None:
                self.view.removeItem(self.mesh_item)

            self.mesh_item = gl.GLMeshItem(
                vertexes=vertices,
                faces=faces,
                smooth=False,
                drawEdges=True,
                edgeColor=(0, 0, 0, 1),
                color=(0.7, 0.7, 0.9, 1),
            )
            self.view.addItem(self.mesh_item)

            center = vertices.mean(axis=0)
            self.view.opts['center'] = pg.Vector(*center)
        except Exception as e:
            ErrorDialog(self, e)

    def closeEvent(self, event):
        """Remove mesh item from the GL view before closing the widget."""
        try:
            if self.mesh_item is not None:
                self.view.removeItem(self.mesh_item)
                self.mesh_item = None
            super().closeEvent(event)
        except Exception as e:
            ErrorDialog(self, e)


class WorkerThread(QThread):
    finished = Signal()

    def __init__(self, source_dir, target_dir, target_fun):
        super().__init__()
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.target_fun = target_fun

    def run(self):
        """Execute the provided target function in a worker thread."""
        self.target_fun()
