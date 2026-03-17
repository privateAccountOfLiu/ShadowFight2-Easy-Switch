import math
import tempfile

import numpy as np
from PySide6.QtCore import QPoint, QRect, Qt, QTimer, QThread, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from PySide6.QtWidgets import QVBoxLayout, QWidget, QFrame
import pyqtgraph as pg
import pyqtgraph.opengl as gl

from python.core.core_classes import Obj
from python.core.core_functions import *
from python.ui.notice_dialog_widgets import ErrorDialog


class AxisHUDWidget(QWidget):
    """Overlay widget that draws a dynamic X/Y/Z axis indicator in the bottom-left of a GL view."""

    SIZE = 72
    MARGIN = 8
    AXIS_LEN = 22

    def __init__(self, gl_view, parent=None, axis_mapping=None):
        """axis_mapping 用于指定逻辑坐标轴在 GL 世界坐标中的方向。

        例如，对于默认三维视图可以使用:
            X -> (1, 0, 0), Y -> (0, 1, 0), Z -> (0, 0, 1)

        对于经过坐标变换的视图（如 AnimationPlayer），可以传入自定义映射，
        使 HUD 中的 X/Y/Z 与逻辑含义保持一致。
        """
        super().__init__(parent)
        self._gl_view = gl_view
        if axis_mapping is None:
            self._axis_mapping = {
                "X": np.array([1.0, 0.0, 0.0]),
                "Y": np.array([0.0, 1.0, 0.0]),
                "Z": np.array([0.0, 0.0, 1.0]),
            }
        else:
            self._axis_mapping = {
                name: np.array(vec, dtype=float) for name, vec in axis_mapping.items()
            }

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setFixedSize(self.SIZE, self.SIZE)
        self._gl_view.installEventFilter(self)
        self._update_geometry()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_tick)
        self._timer.start(120)

    def _update_geometry(self):
        if self._gl_view and self._gl_view.height() >= self.SIZE:
            self.setGeometry(
                self.MARGIN,
                self._gl_view.height() - self.SIZE - self.MARGIN,
                self.SIZE,
                self.SIZE,
            )

    def eventFilter(self, obj, event):
        if obj == self._gl_view and event.type() == event.Type.Resize:
            self._update_geometry()
        return super().eventFilter(obj, event)

    def _on_tick(self):
        if self.isVisible():
            self.update()

    def _project_axes(self):
        try:
            opts = getattr(self._gl_view, "opts", None)
            if opts is None:
                return None
            az_deg = opts.get("azimuth", 0)
            el_deg = opts.get("elevation", 0)
        except Exception:
            return None
        az = math.radians(az_deg)
        el = math.radians(el_deg)
        cx, sx = math.cos(az), math.sin(az)
        ce, se = math.cos(el), math.sin(el)
        view_dir = np.array([-ce * cx, -ce * sx, -se], dtype=float)
        view_dir /= max(np.linalg.norm(view_dir), 1e-6)
        up_world = np.array([0.0, 1.0, 0.0])
        right = np.cross(up_world, view_dir)
        rn = np.linalg.norm(right)
        if rn < 1e-6:
            right = np.array([1.0, 0.0, 0.0])
        else:
            right /= rn
        up_screen = np.cross(view_dir, right)
        up_screen /= max(np.linalg.norm(up_screen), 1e-6)

        def proj(axis):
            dx = np.dot(axis, right)
            dy = -np.dot(axis, up_screen)
            return (dx, dy)
        return {name: proj(axis) for name, axis in self._axis_mapping.items()}

    def paintEvent(self, event):
        super().paintEvent(event)
        proj = self._project_axes()
        if proj is None:
            return
        center_x = self.SIZE // 2
        center_y = self.SIZE // 2
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
        font = QFont()
        font.setPointSize(7)
        painter.setFont(font)
        colors = [
            ("X", proj["X"], QColor(200, 60, 60)),
            ("Y", proj["Y"], QColor(60, 160, 60)),
            ("Z", proj["Z"], QColor(60, 80, 200)),
        ]
        for label, (dx, dy), color in colors:
            length = math.hypot(dx, dy)
            if length < 1e-4:
                continue
            scale = self.AXIS_LEN / max(length, 1e-4)
            ex = center_x + dx * scale
            ey = center_y - dy * scale
            painter.setPen(QPen(color, 2))
            painter.drawLine(center_x, center_y, int(ex), int(ey))
            tx = center_x + dx * (scale + 6)
            ty = center_y - dy * (scale + 6)
            painter.setPen(color)
            painter.drawText(int(tx) - 4, int(ty) + 4, label)
        painter.end()


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
        self.view.setObjectName("modelGLView")
        self.view.setBackgroundColor((245, 246, 248))
        self.view.opts['distance'] = 10
        frame_layout.addWidget(self.view)

        self._axis_hud = AxisHUDWidget(self.view, self.view)
        self._axis_hud.show()

        # 初始给一个占位网格，后续在加载模型时根据模型尺寸动态调整
        self.grid_item = gl.GLGridItem(glOptions="opaque")
        self.grid_item.setColor((0, 0, 0, 255))
        self.view.addItem(self.grid_item)

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

            # 根据模型尺寸动态调整网格尺寸与格子大小，视觉上接近“无限网格”
            mins = vertices.min(axis=0)
            maxs = vertices.max(axis=0)
            center = (mins + maxs) / 2.0
            extent = max(maxs - mins)
            if extent <= 0:
                extent = 1.0

            # 网格整体尺寸取模型尺寸的 4 倍，相对物体稍微缩减一些
            grid_size = extent * 4.0
            # 只需要 12x12 个格子即可，格子大小由整体尺寸自动决定
            cell_size = max(grid_size / 12.0, 0.05)
            if grid_size > 0:
                self.grid_item.setSize(grid_size, grid_size)
                self.grid_item.setSpacing(cell_size, cell_size)
                # 让网格在 X/Y 方向跟随模型中心，但 Z 方向恒定为 0
                self.grid_item.resetTransform()
                self.grid_item.translate(center[0], center[1], 0.0)

            self.view.opts['center'] = pg.Vector(*center)
        except Exception as e:
            ErrorDialog(self, e)

    def closeEvent(self, event):
        """Remove mesh item and grid from the GL view before closing the widget."""
        try:
            if self.mesh_item is not None:
                self.view.removeItem(self.mesh_item)
                self.mesh_item = None
            if getattr(self, "grid_item", None) is not None:
                self.view.removeItem(self.grid_item)
                self.grid_item = None
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
