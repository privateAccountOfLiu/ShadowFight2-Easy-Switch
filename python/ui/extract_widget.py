import tempfile

import pyvista as pv
import vtk
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (QVBoxLayout, QWidget,
                             QHBoxLayout, QPushButton, QSlider, QLabel, QMainWindow, QMenu, QMenuBar, QCheckBox)
from pyvistaqt import QtInteractor

from python.core.core_functions import *
from python.ui.notice_dialog_widget import ErrorDialog


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
                self.plotter = QtInteractor(parent=self.parent(), auto_update=True)
                self.layout().addWidget(self.plotter)
            self.mesh_show()
            self.plotter.render()
        except Exception as e:
            ErrorDialog(self, e)


class AnimationPlayer(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.content = basic_bin_bytes
        self.sphere_radius = 0
        self.data_bounds = None
        self.num_nodes = 0
        self.num_frames = 0
        self.frames_data = []
        self.move_bin = MoveBin.build_binary(self.content)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.control_layout = QHBoxLayout()
        self.layout = QVBoxLayout(self.central_widget)
        self.plotter = QtInteractor(parent=self.parent(), auto_update=True)
        self.renderer = vtk.vtkRenderer()
        self.plotter.GetRenderWindow().AddRenderer(self.renderer)
        self.timer = QTimer()
        self.play_button = QPushButton("Play")
        self.prev_button = QPushButton("Last")
        self.next_button = QPushButton("Next")
        self.reset_camera_button = QPushButton("Reset Camera")
        self.frame_slider = QSlider(Qt.Orientation.Horizontal)
        self.action_open = QAction(self)
        self.action_csv = QAction(self)
        self.action_bin = QAction(self)
        self.menubar = QMenuBar(self)
        self.menuFile = QMenu(self.menubar)
        self.menuSave_as = QMenu(self.menuFile)
        self.menuSetting = QMenu(self.menubar)
        self.menuHelp = QMenu(self.menubar)
        self.trajectory_checkbox = QCheckBox("Show Orbit")
        self.current_frame = 0

        self.frame_label = QLabel("Frame 0/0")

        self.is_playing = False
        self.show_trajectories = False
        self.scale_factor = 1.0

        self.trajectory_actors = []
        self.line_actors = []
        self.sphere_sources = []
        self.sphere_actors = []

        self.connections = [
            (13, 15), (12, 14), (14, 30), (29, 30), (29, 32), (30, 32), (14, 16), (14, 32), (14, 29), (15, 31),
            (31, 33), (33, 34), (15, 34), (15, 17), (15, 33), (11, 13), (10, 12), (0, 53), (52, 53), (51, 52),
            (0, 51), (51, 53), (0, 52), (0, 43), (1, 43), (1, 2), (1, 3), (1, 44), (1, 45), (28, 48),
            (45, 48), (44, 48), (44, 45), (1, 48), (2, 4), (4, 6), (3, 5), (10, 11), (18, 50), (11, 50), (10, 50),
            (18, 27), (10, 27), (11, 27), (27, 50), (46, 47), (28, 46), (28, 47), (27, 28), (27, 48), (47, 48),
            (46, 48), (43, 53), (5, 7), (49, 54), (20, 22), (19, 20), (20, 21), (23, 24), (24, 25), (24, 26)
        ]
        self.setup_ui()
        self.load_bin_file(self.content)
        self.setup_animation()
        self.plotter.Initialize()
        self.plotter.Start()

    def load_bin_file(self, content: bytes):
        try:
            self.content = content
            self.move_bin = MoveBin.build_binary(content)
            self.frames_data = [frame.points for frame in self.move_bin.bin_data]
            self.num_frames = self.move_bin.frames_num
            self.num_nodes = self.move_bin.bin_data[0].length if self.num_frames > 0 else 0
            self.data_bounds = self.calculate_data_bounds()
            self.sphere_radius = self.calculate_sphere_radius()
            self.update_ui_after_loading()
            self.setup_vtk_after_loading()
            self.current_frame = 0
            self.update_frame_display()
        except Exception as e:
            ErrorDialog(self, e)

    def calculate_data_bounds(self):
        if not self.frames_data:
            return None

        all_points = [point for frame in self.frames_data for point in frame]
        min_x = min(point[0] for point in all_points)
        max_x = max(point[0] for point in all_points)
        min_y = min(point[1] for point in all_points)
        max_y = max(point[1] for point in all_points)
        min_z = min(point[2] for point in all_points)
        max_z = max(point[2] for point in all_points)

        bounds = {
            'min': (min_x, min_y, min_z),
            'max': (max_x, max_y, max_z),
            'range': (max_x - min_x, max_y - min_y, max_z - min_z),
            'center': ((min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2)
        }

        print(f"DataRange: X[{min_x:.2f}, {max_x:.2f}], Y[{min_y:.2f}, {max_y:.2f}], Z[{min_z:.2f}, {max_z:.2f}]")
        return bounds

    def update_ui_after_loading(self):
        self.frame_slider.setRange(0, self.num_frames - 1)
        self.frame_label.setText(f"Frame {self.current_frame + 1}/{self.num_frames}")
        self.setWindowTitle(f"BinaryPlayer - {self.num_frames} frames, {self.num_nodes} nodes")

    def setup_vtk_after_loading(self):
        self.clear_scene()
        self.renderer.SetBackground(1, 1, 1)
        valid_connections = [(start, end) for start, end in self.connections
                             if start < self.num_nodes and end < self.num_nodes]

        for i in range(self.num_nodes):
            sphere_source = vtk.vtkSphereSource()
            sphere_source.SetRadius(self.sphere_radius)
            sphere_source.SetPhiResolution(8)
            sphere_source.SetThetaResolution(8)

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(sphere_source.GetOutputPort())

            actor = vtk.vtkActor()
            actor.SetMapper(mapper)

            hue = i / max(1, self.num_nodes - 1)
            actor.GetProperty().SetColor(*self.hsv_to_rgb(hue, 0.8, 1.0))

            self.renderer.AddActor(actor)
            self.sphere_actors.append(actor)
            self.sphere_sources.append(sphere_source)

        for start_idx, end_idx in valid_connections:
            line_source = vtk.vtkLineSource()

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(line_source.GetOutputPort())

            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(0, 0,
                                         0)
            actor.GetProperty().SetLineWidth(2)

            self.renderer.AddActor(actor)
            self.line_actors.append((actor, line_source, start_idx, end_idx))
        self.setup_trajectories()
        self.setup_camera()

    def clear_scene(self):
        if self.is_playing:
            self.timer.stop()
            self.is_playing = False
            self.play_button.setText("Play")
        for actor in self.sphere_actors:
            self.renderer.RemoveActor(actor)
        self.sphere_actors = []
        self.sphere_sources = []
        for actor_data in self.line_actors:
            actor, _, _, _ = actor_data
            self.renderer.RemoveActor(actor)
        self.line_actors = []
        for actor in self.trajectory_actors:
            self.renderer.RemoveActor(actor)
        self.trajectory_actors = []

    def setup_ui(self):
        self.setWindowTitle("BinaryPlayer")
        self.resize(800, 600)

        self.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.action_open)
        self.menuFile.addAction(self.menuSave_as.menuAction())
        self.menuSave_as.addAction(self.action_csv)
        self.menuSave_as.addAction(self.action_bin)
        self.menuFile.setIcon(QIcon(get_dir('./res/ui/icon/file.svg')))
        self.menuSetting.setIcon(QIcon(get_dir('./res/ui/icon/setting.svg')))
        self.menuHelp.setIcon(QIcon(get_dir('./res/ui/icon/exclamation-circle.svg')))
        self.action_open.setText("Open")
        self.action_csv.setText("csv")
        self.action_bin.setText("bin/bytes")
        self.menuFile.setTitle("File")
        self.menuSave_as.setTitle("Export")
        self.menuSetting.setTitle("Setting")
        self.menuHelp.setTitle("Help")

        self.layout.addWidget(self.plotter, 1)
        self.control_layout.setSpacing(5)

        self.play_button.clicked.connect(self.toggle_play)
        self.control_layout.addWidget(self.play_button)
        self.prev_button.clicked.connect(self.previous_frame)
        self.control_layout.addWidget(self.prev_button)
        self.next_button.clicked.connect(self.next_frame)
        self.control_layout.addWidget(self.next_button)
        self.reset_camera_button.clicked.connect(self.reset_camera)
        self.control_layout.addWidget(self.reset_camera_button)
        self.trajectory_checkbox.stateChanged.connect(self.toggle_trajectories)
        self.control_layout.addWidget(self.trajectory_checkbox)

        frame_label = QLabel("Frame:")
        self.control_layout.addWidget(frame_label)
        self.frame_slider.setRange(0, 0)
        self.frame_slider.valueChanged.connect(self.slider_changed)
        self.control_layout.addWidget(self.frame_slider)
        self.control_layout.addWidget(self.frame_label)
        self.layout.addLayout(self.control_layout)
        self.renderer.SetBackground(1, 1, 1)

    def setup_vtk(self):
        self.renderer.SetBackground(1, 1, 1)
        self.plotter.GetRenderWindow().AddRenderer(self.renderer)
        for i in range(self.num_nodes):
            sphere_source = vtk.vtkSphereSource()
            sphere_source.SetRadius(self.sphere_radius)
            sphere_source.SetPhiResolution(8)
            sphere_source.SetThetaResolution(8)
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(sphere_source.GetOutputPort())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            hue = i / max(1, self.num_nodes - 1)
            actor.GetProperty().SetColor(*self.hsv_to_rgb(hue, 0.8, 1.0))
            self.renderer.AddActor(actor)
            self.sphere_actors.append(actor)
            self.sphere_sources.append(sphere_source)
        self.setup_skeleton_lines()
        axes = vtk.vtkAxesActor()
        axes_length = max(self.data_bounds['range']) * 0.5 if self.data_bounds else 1.0
        axes.SetTotalLength(axes_length, axes_length, axes_length)
        self.renderer.AddActor(axes)
        self.setup_camera()
        self.setup_trajectories()

    def calculate_sphere_radius(self):
        if not self.data_bounds:
            return 0.1

        max_range = max(self.data_bounds['range'])
        radius = max_range * 0.005
        return max(0.01, radius)

    def setup_skeleton_lines(self):
        for start_idx, end_idx in self.connections:
            line_source = vtk.vtkLineSource()

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(line_source.GetOutputPort())

            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(0, 0,
                                         0)
            actor.GetProperty().SetLineWidth(2)

            self.renderer.AddActor(actor)
            self.line_actors.append((actor, line_source, start_idx, end_idx))

    def setup_trajectories(self):
        for node_idx in range(self.num_nodes):
            points = vtk.vtkPoints()
            for frame_idx in range(self.num_frames):
                x, y, z = self.frames_data[frame_idx][node_idx]
                points.InsertNextPoint(x, y, z)
            poly_line = vtk.vtkPolyLine()
            poly_line.GetPointIds().SetNumberOfIds(self.num_frames)
            for i in range(self.num_frames):
                poly_line.GetPointIds().SetId(i, i)
            cells = vtk.vtkCellArray()
            cells.InsertNextCell(poly_line)
            poly_data = vtk.vtkPolyData()
            poly_data.SetPoints(points)
            poly_data.SetLines(cells)
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputData(poly_data)
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(*self.hsv_to_rgb(node_idx / max(1, self.num_nodes - 1), 0.8, 0.6))
            actor.GetProperty().SetLineWidth(1)
            actor.SetVisibility(False)
            self.renderer.AddActor(actor)
            self.trajectory_actors.append(actor)

    def setup_camera(self):
        if not self.data_bounds:
            return

        center = self.data_bounds['center']
        max_range = max(self.data_bounds['range'])

        camera = self.renderer.GetActiveCamera()
        camera.SetFocalPoint(center[0], center[1], center[2])
        camera.SetPosition(
            center[0],
            center[1],
            center[2] + max_range * 1.5
        )
        camera.SetViewUp(0, 1, 0)
        self.renderer.ResetCameraClippingRange()

    def reset_camera(self):
        """Reset the camera to the initial setup position"""
        self.setup_camera()
        self.plotter.GetRenderWindow().Render()

    def setup_animation(self):
        self.timer.timeout.connect(self.next_frame)
        self.timer.setInterval(50)  # 20 FPS
        self.update_frame_display()

    def update_frame_display(self):
        if self.current_frame >= len(self.frames_data):
            return
        frame_points = self.frames_data[self.current_frame]

        for node_idx, (x, y, z) in enumerate(frame_points):
            if node_idx < len(self.sphere_actors):
                scaled_x = x * self.scale_factor
                scaled_y = y * self.scale_factor
                scaled_z = z * self.scale_factor
                self.sphere_actors[node_idx].SetPosition(scaled_x, scaled_y, scaled_z)

        for actor, line_source, start_idx, end_idx in self.line_actors:
            if start_idx < len(frame_points) and end_idx < len(frame_points):
                start_point = frame_points[start_idx]
                end_point = frame_points[end_idx]

                scaled_start_x = start_point[0] * self.scale_factor
                scaled_start_y = start_point[1] * self.scale_factor
                scaled_start_z = start_point[2] * self.scale_factor

                scaled_end_x = end_point[0] * self.scale_factor
                scaled_end_y = end_point[1] * self.scale_factor
                scaled_end_z = end_point[2] * self.scale_factor

                line_source.SetPoint1(scaled_start_x, scaled_start_y, scaled_start_z)
                line_source.SetPoint2(scaled_end_x, scaled_end_y, scaled_end_z)

        self.frame_slider.setValue(self.current_frame)
        self.frame_label.setText(f"Frame {self.current_frame + 1}/{self.num_frames}")

        self.plotter.GetRenderWindow().Render()

    def toggle_play(self):
        if self.is_playing:
            self.timer.stop()
            self.play_button.setText("Play")
        else:
            self.timer.start()
            self.play_button.setText("Stop")
        self.is_playing = not self.is_playing

    def next_frame(self):
        self.current_frame = (self.current_frame + 1) % self.num_frames
        self.update_frame_display()

    def previous_frame(self):
        self.current_frame = (self.current_frame - 1) % self.num_frames
        self.update_frame_display()

    def slider_changed(self, value):
        if value != self.current_frame:
            self.current_frame = value
            self.update_frame_display()

    def toggle_trajectories(self, state):
        self.show_trajectories = (state == Qt.CheckState.Checked.value)
        for actor in self.trajectory_actors:
            actor.SetVisibility(self.show_trajectories)
        self.plotter.GetRenderWindow().Render()

    @staticmethod
    def hsv_to_rgb(h, s, v):
        if s == 0.0:
            return v, v, v
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        color = [(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)]
        return color[i % 6]

    def closeEvent(self, event):
        try:
            if hasattr(self, 'plotter') and self.plotter:
                if self.is_playing:
                    self.timer.stop()
                    self.play_button.setText("Play")
                self.plotter.close()
                self.plotter.deleteLater()
                self.plotter = None
            super().closeEvent(event)
        except Exception as e:
            ErrorDialog(self, e)

    def showEvent(self, event):
        try:
            super().showEvent(event)
            if not hasattr(self, 'plotter') or self.plotter is None:
                self.plotter = QtInteractor(parent=self.parent(), auto_update=True)
                self.renderer = vtk.vtkRenderer()
                self.plotter.GetRenderWindow().AddRenderer(self.renderer)
                self.load_bin_file(self.content)
                self.layout.insertWidget(0, self.plotter)
            self.plotter.Initialize()
            self.plotter.Start()
            self.plotter.render()
        except Exception as e:
            ErrorDialog(self, e)

    def hideEvent(self, event):
        try:
            if hasattr(self, 'plotter') and self.plotter:
                if self.is_playing:
                    self.timer.stop()
                    self.play_button.setText("Play")
                self.plotter.hide()
            super().hideEvent(event)
        except Exception as e:
            ErrorDialog(self, e)


class WorkerThread(QThread):
    finished = pyqtSignal()

    def __init__(self, source_dir, target_dir, target_fun):
        super().__init__()
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.target_fun = target_fun

    # noinspection PyUnresolvedReferences
    def run(self):
        self.target_fun()
        self.finished.emit()
