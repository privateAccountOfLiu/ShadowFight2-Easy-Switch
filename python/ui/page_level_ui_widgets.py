import csv
from typing import Dict

from PySide6 import QtGui, QtCore
from PySide6.QtCore import QRect

from python.core.core_classes import Obj
from python.core.core_functions import *
from python.ui.additional_widgets import ObjModelViewer, WorkerThread
from python.ui.basic_level_ui_widgets import BasicToolMainWindow, AnimationPlayer, BasicYieldCsvPage, ModelPlayer
from python.ui.notice_dialog_widgets import ErrorDialog, NoticeDialog
from python.ui.settings_dialog import SettingsDialog
from python.util import i18n
from python.util.settings import AppSettings
from python.util.tools import Tools
from python.util.values import basic_bin_bytes
from python.util.xml_reader import XmlReader


class ToolMainWindow(BasicToolMainWindow):
    def __init__(self):
        """Initialize the main tool window and create all sub-pages."""
        self.pushButton_1 = self.pushButton_2 = self.pushButton_3 = self.pushButton_4 = None
        BasicToolMainWindow.__init__(self, self)
        self.page1 = ModelEditor()
        self.page2 = CsvYieldTool()
        self.page3 = AnimationEditor()
        self.init_build()

    def init_build(self):
        """Bind main window buttons to open corresponding tool pages."""
        self.setWindowIcon(QtGui.QIcon(u':/icons/icon'))
        self.setWindowFlag(QtCore.Qt.WindowType.WindowMaximizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowMinimizeButtonHint, False)
        self.pushButton_1.clicked.connect(self.page1.show)
        self.pushButton_2.clicked.connect(self.page2.show)
        self.pushButton_3.clicked.connect(self.page3.show)


class ModelEditor(ModelPlayer):
    def __init__(self):
        """Initialize the model editor page, including preview widget and state fields."""
        super().__init__(main_window=self)
        self.input_directory: str = ""
        self.obj_data: str = ""
        self.pre_obj_data: str = ""
        self.ori_obj_data: str = ""
        self.vtk_viewer = ObjModelViewer(parent=self)
        self.advanced_setting = [self.label_7, self.comboBox_2,
                                 self.label_3, self.doubleSpinBox, self.doubleSpinBox_2,
                                 self.label_4, self.doubleSpinBox_3, self.doubleSpinBox_4,
                                 self.label_5, self.doubleSpinBox_5, self.doubleSpinBox_6]
        self.init_build()

    def init_build(self) -> None:
        """Configure advanced widgets, preview widget geometry and signal bindings."""
        self.vtk_viewer.setGeometry(255, 40, 530, 530)
        self.vtk_viewer.show()
        self.checkBox.setChecked(True)
        for widget in self.advanced_setting[2:]:
            if hasattr(widget, "setDisabled"):
                widget.setDisabled(True)
        self.pushButton.clicked.connect(self.apply_config)
        self.actionOpen.triggered.connect(self.get_data)
        self.action_xml.triggered.connect(lambda: self.output_xml())
        self.action_obj.triggered.connect(lambda: self.output_obj())
        self.checkBox.stateChanged.connect(self.setting_show)
        self.comboBox_2.currentIndexChanged.connect(self.setting_able)

    def get_data(self) -> None:
        """Open an OBJ or XML model file and load its geometry into the preview and editor state."""
        self.input_directory = self.file_chose("WaveFront(*.obj);;SF2Model(*.xml)")
        if self.input_directory:
            try:
                if self.input_directory.endswith(".obj"):
                    with open(self.input_directory, "r", encoding="utf-8") as read_file:
                        self.obj_data = self.ori_obj_data = self.pre_obj_data = read_file.read()
                elif self.input_directory.endswith(".xml"):
                    with open(self.input_directory, "r", encoding="utf-8") as read_file:
                        xml_data = read_file.read()
                        obj_text = XmlReader.generate_obj_string(xml_data, capsule_segments=8, capsule_rings=4)
                        self.obj_data = self.ori_obj_data = self.pre_obj_data = obj_text
                self.vtk_viewer.add_mesh(self.obj_data)
                msg = Obj.build_obj(self.obj_data).get_msg()
                scope = msg.get('Scope', [None, None, None])
                self.statue_label.setText(f"Nodes: {msg.get('Nodes', 0)}, Edges: {msg.get('Edges')},"
                                          f" Triangles: {msg.get('Triangles')},"
                                          f" X Scope: {scope[0]}, Y Scope: {scope[1]}, Z Scope: {scope[2]}")
            except Exception as e:
                ErrorDialog(self, e)

    def apply_config(self):
        """Apply current configuration to the model data and refresh preview and status text."""
        if self.input_directory:
            try:
                temp_obj = Tools.edit_obj_data(Obj.build_obj(self.pre_obj_data), self.get_config())
                self.obj_data = temp_obj.to_text()
                self.vtk_viewer.add_mesh(self.obj_data)
                msg = temp_obj.get_msg()
                scope = msg.get('Scope', [None, None, None])
                self.statue_label.setText(f"Nodes: {msg.get('Nodes', 0)}, Edges: {msg.get('Edges')},"
                                          f" Triangles: {msg.get('Triangles')},"
                                          f" X Scope: {scope[0]}, Y Scope: {scope[1]}, Z Scope: {scope[2]}")
            except Exception as e:
                ErrorDialog(self, e)

    def get_config(self) -> Dict[str, List[float] | str | bool | int]:
        """Build a configuration dictionary from the current UI control values."""
        config = {
            'x': [float(self.doubleSpinBox.text()), float(self.doubleSpinBox_2.text())],
            'y': [float(self.doubleSpinBox_3.text()), float(self.doubleSpinBox_4.text())],
            'z': [float(self.doubleSpinBox_5.text()), float(self.doubleSpinBox_6.text())],
            'type': self.comboBox_4.currentText(),
            'rotate_method': self.comboBox.currentText(),
            'is_zoom': True if self.comboBox_2.currentText() == 'True' else False,
            'begin_id': int(self.spinBox.text()),
            'is_draw_edge': False
        }
        return config

    def output_xml(self, directory: str = './model/output.xml'):
        """Export the edited model to an XML file under the configured model export directory."""
        if self.input_directory:
            try:
                settings = AppSettings.instance()
                export_dir = settings.export_dir_model or "./model"
                os.makedirs(export_dir, exist_ok=True)
                directory = os.path.join(export_dir, os.path.basename(directory))
                config = self.get_config()
                obj = Tools.edit_obj_data(Obj.build_obj(self.pre_obj_data), config)
                xml_doc = Tools.model_obj_to_xml(obj, config)
                with open(directory, 'w', encoding="utf-8") as xml_out:
                    xml_out.write(xml_doc)
                NoticeDialog(self)
            except Exception as e:
                ErrorDialog(self, e)
        else:
            NoticeDialog(self, i18n.tr("dialog.notice.no_file"))

    def output_obj(self, directory: str = './model/output.obj'):
        """Export the edited model to an OBJ file under the configured model export directory."""
        if self.input_directory:
            try:
                settings = AppSettings.instance()
                export_dir = settings.export_dir_model or "./model"
                os.makedirs(export_dir, exist_ok=True)
                directory = os.path.join(export_dir, os.path.basename(directory))
                config = self.get_config()
                obj = Tools.edit_obj_data(Obj.build_obj(self.pre_obj_data), config)
                with open(directory, 'w', encoding="utf-8") as obj_out:
                    obj_out.write(obj.to_text())
                NoticeDialog(self)
            except Exception as e:
                ErrorDialog(self, e)
        else:
            NoticeDialog(self, i18n.tr("dialog.notice.no_file"))

    def setting_show(self, state):
        """Show or hide advanced setting widgets and resize the control panel accordingly."""
        if not state:
            for widget in self.advanced_setting:
                widget.hide()
                self.gridLayoutWidget.setGeometry(QRect(10, 10, 230, 180))
        else:
            for widget in self.advanced_setting:
                widget.show()
                self.gridLayoutWidget.setGeometry(QRect(10, 10, 230, 320))

    def setting_able(self, state):
        """Enable or disable advanced setting controls based on state selection."""
        for widget in self.advanced_setting[2:]:
            if hasattr(widget, "setDisabled"):
                widget.setDisabled(not bool(state))


class CsvYieldTool(BasicYieldCsvPage):
    def __init__(self):
        """Batch CSV export tool that converts multiple OBJ files to CSV format."""
        self.worker = None
        super().__init__(main_window=self)
        self.input_directory: str = ""
        self.csv_data: str = ""
        self.total_files = self.finished_files = self.error_files = 0
        self.local_timer = QtCore.QTimer()
        self.init_build()

    def init_build(self) -> None:
        """Wire UI signals for directory selection, output actions and progress updates."""
        self.pushButton.clicked.connect(self.get_data)
        self.buttonBox.accepted.connect(self.output)
        self.buttonBox.rejected.connect(self.close)
        self.local_timer.timeout.connect(self.update_progress)

    def get_data(self) -> None:
        """Allow user to choose an input directory and update file count display."""
        self.input_directory = self.dir_chose()
        if self.input_directory:
            try:
                self.textBrowser.setText(self.input_directory)
                self.total_files = find_regular_files(['.obj'], self.input_directory)
            except Exception as e:
                ErrorDialog(self, e)

    def output(self) -> None:
        """Start the background worker thread to generate the output CSV file."""
        if self.input_directory:
            try:
                if self.worker:
                    self.worker.finished.disconnect()
                self.progressBar.setValue(0)
                self.worker = WorkerThread(self.input_directory, "./csv",
                                           lambda: self.write_csv_animation())
                self.worker.finished.connect(self.on_finished)
                self.worker.start()
                self.local_timer.start(50)
            except Exception as e:
                ErrorDialog(self, e)
                self.error_files += 1

    def update_progress(self):
        """Update the progress bar according to finished and failed file counts."""
        new_value = int(round(self.finished_files + self.error_files / self.total_files, 2))
        self.progressBar.setValue(new_value)
        self.progressBar.update()

    def on_finished(self):
        """Finalize progress state and show a completion notice when batch work ends."""
        self.local_timer.stop()
        self.progressBar.setValue(100)
        self.finished_files = self.total_files - self.error_files
        NoticeDialog(self, f'[Notice]: Transform Successfully!\n'
                           f'Total: {self.total_files}\n'
                           f'Successful: {self.finished_files}\n'
                           f'Failed: {self.error_files}')

    def get_config(self) -> Dict[str, List[float] | str | bool | int]:
        """Build a transformation configuration dictionary from the CSV tool controls."""
        config = {
            'x': [float(self.doubleSpinBox.text()), float(self.doubleSpinBox_2.text())],
            'y': [float(self.doubleSpinBox_3.text()), float(self.doubleSpinBox_4.text())],
            'z': [float(self.doubleSpinBox_5.text()), float(self.doubleSpinBox_6.text())],
            'rotate_method': self.comboBox.currentText(),
            'is_zoom': True if self.comboBox_2.currentText() == 'True' else False,
        }
        return config

    def write_csv_animation(self, file_name: str = './csv/output.csv') -> None:
        """Write animation data derived from OBJ files in the input directory to a CSV file."""
        try:
            tar = os.listdir(self.input_directory)
            settings = AppSettings.instance()
            export_dir = settings.export_dir_model or "./csv"
            os.makedirs(export_dir, exist_ok=True)
            target_path = os.path.join(export_dir, os.path.basename(file_name))
            with open(target_path, 'w', newline='', encoding="utf-8") as f_decode:
                _writer = csv.writer(f_decode)
                for obj_name in tar:
                    if obj_name.endswith('.obj'):
                        obj_p = Tools.edit_obj_data(Obj(os.path.join(self.input_directory, obj_name)),
                                                    self.get_config())
                        _writer.writerow([str(_i) for _i in obj_p.pre_formate_to_bin()[1]])
        except Exception as e:
            ErrorDialog(self, e)


class AnimationEditor(AnimationPlayer):
    def __init__(self):
        """Initialize the animation editor based on the shared AnimationPlayer widget."""
        super().__init__()
        self.input_directory: str = ""
        self.binary_stream: bytes = basic_bin_bytes
        self.init_build()

    def init_build(self) -> None:
        """Connect player actions to file loading and export methods."""
        self.action_open.triggered.connect(self.get_data)
        self.action_csv.triggered.connect(lambda: self.output_to_csv())
        self.action_bin.triggered.connect(lambda: self.output_to_binary())

    def get_data(self) -> None:
        """Open a binary or CSV animation file and load it into the animation player."""
        self.input_directory = self.file_chose("Binary(*.bin *bytes);;Csv(*.csv)")
        if self.input_directory:
            try:
                if self.input_directory.endswith((".bin", ".bytes")):
                    with open(self.input_directory, "rb") as read_file:
                        self.binary_stream = read_file.read()
                    self.load_bin_file(self.binary_stream)
                elif self.input_directory.endswith(".csv"):
                    self.load_bin_file(Tools.animation_serialize(self.input_directory).bin_content)
                else:
                    raise TypeError("Unsupported File!")
            except Exception as e:
                ErrorDialog(self, e)

    def output_to_csv(self, directory: str = "./animation/decode_bin.csv") -> None:
        """Export the current animation to a CSV file using the configured animation export directory."""
        if self.input_directory:
            try:
                settings = AppSettings.instance()
                export_dir = settings.export_dir_animation or "./animation"
                os.makedirs(export_dir, exist_ok=True)
                target_path = os.path.join(export_dir, os.path.basename(directory))
                with open(target_path, "w") as csv_out:
                    csv_out.write(Tools.animation_deserialize(self.move_bin))
                NoticeDialog(self)
            except Exception as e:
                ErrorDialog(self, e)
        else:
            NoticeDialog(self, i18n.tr("dialog.notice.no_file"))

    def output_to_binary(self, directory: str = "./animation/encode_bin.bin") -> None:
        """Export the current animation content to a binary file using the configured export directory."""
        if self.input_directory:
            try:
                settings = AppSettings.instance()
                export_dir = settings.export_dir_animation or "./animation"
                os.makedirs(export_dir, exist_ok=True)
                target_path = os.path.join(export_dir, os.path.basename(directory))
                with open(target_path, 'wb') as bin_out:
                    bin_out.write(self.content)
                NoticeDialog(self)
            except Exception as e:
                ErrorDialog(self, e)
        else:
            NoticeDialog(self, i18n.tr("dialog.notice.no_file"))
