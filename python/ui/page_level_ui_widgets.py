import csv
from typing import Dict

from PySide6 import QtGui, QtCore
from PySide6.QtCore import QRect

from python.core.core_classes import Obj
from python.core.core_functions import *
from python.ui.additional_widgets import ObjModelViewer, WorkerThread
from python.ui.basic_level_ui_widgets import BasicToolMainWindow, AnimationPlayer, BasicYieldCsvPage, ModelPlayer
from python.ui.notice_dialog_widgets import ErrorDialog, NoticeDialog
from python.util.tools import Tools
from python.util.values import basic_bin_bytes
from python.util.xml_reader import XmlReader


class ToolMainWindow(BasicToolMainWindow):
    def __init__(self):
        self.pushButton_1 = self.pushButton_2 = self.pushButton_3 = self.pushButton_4 = None
        BasicToolMainWindow.__init__(self, self)
        self.page1 = ModelEditor()
        self.page2 = CsvYieldTool()
        self.page3 = AnimationEditor()
        self.init_build()

    def init_build(self):
        self.setWindowIcon(QtGui.QIcon(u':/icons/icon'))
        self.setWindowFlag(QtCore.Qt.WindowType.WindowMaximizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowMinimizeButtonHint, False)
        self.pushButton_1.clicked.connect(self.page1.show)
        self.pushButton_2.clicked.connect(self.page2.show)
        self.pushButton_3.clicked.connect(self.page3.show)


class ModelEditor(ModelPlayer):
    def __init__(self):
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
        self.input_directory = self.file_chose("WaveFront(*.obj);;SF2Model(*.xml)")
        if self.input_directory:
            try:
                if self.input_directory.endswith(".obj"):
                    with open(self.input_directory, "r", encoding="utf-8") as read_file:
                        self.obj_data = self.ori_obj_data = self.pre_obj_data = read_file.read()
                elif self.input_directory.endswith(".xml"):
                    with open(self.input_directory, "r", encoding="utf-8") as read_file:
                        xml_data = read_file.read()
                        obj_text = XmlReader.generate_obj_string(xml_data, capsule_segments=16, capsule_rings=12)
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
        if self.input_directory:
            try:
                config = self.get_config()
                obj = Tools.edit_obj_data(Obj.build_obj(self.pre_obj_data), config)
                xml_doc = Tools.model_obj_to_xml(obj, config)
                with open(directory, 'w', encoding="utf-8") as xml_out:
                    xml_out.write(xml_doc)
                NoticeDialog(self)
            except Exception as e:
                ErrorDialog(self, e)
        else:
            NoticeDialog(self, "You Haven't Chose A File!")

    def output_obj(self, directory: str = './model/output.obj'):
        if self.input_directory:
            try:
                config = self.get_config()
                obj = Tools.edit_obj_data(Obj.build_obj(self.pre_obj_data), config)
                with open(directory, 'w', encoding="utf-8") as obj_out:
                    obj_out.write(obj.to_text())
                NoticeDialog(self)
            except Exception as e:
                ErrorDialog(self, e)
        else:
            NoticeDialog(self, "You Haven't Chose A File!")

    def setting_show(self, state):
        if not state:
            for widget in self.advanced_setting:
                widget.hide()
                self.gridLayoutWidget.setGeometry(QRect(10, 10, 230, 180))
        else:
            for widget in self.advanced_setting:
                widget.show()
                self.gridLayoutWidget.setGeometry(QRect(10, 10, 230, 320))

    def setting_able(self, state):
        for widget in self.advanced_setting[2:]:
            if hasattr(widget, "setDisabled"):
                widget.setDisabled(not bool(state))


class CsvYieldTool(BasicYieldCsvPage):
    def __init__(self):
        self.worker = None
        super().__init__(main_window=self)
        self.input_directory: str = ""
        self.csv_data: str = ""
        self.total_files = self.finished_files = self.error_files = 0
        self.local_timer = QtCore.QTimer()
        self.init_build()

    def init_build(self) -> None:
        self.pushButton.clicked.connect(self.get_data)
        self.buttonBox.accepted.connect(self.output)
        self.buttonBox.rejected.connect(self.close)
        self.local_timer.timeout.connect(self.update_progress)

    def get_data(self) -> None:
        self.input_directory = self.dir_chose()
        if self.input_directory:
            try:
                self.textBrowser.setText(self.input_directory)
                self.total_files = find_regular_files(['.obj'], self.input_directory)
            except Exception as e:
                ErrorDialog(self, e)

    def output(self) -> None:
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
        new_value = int(round(self.finished_files + self.error_files / self.total_files, 2))
        self.progressBar.setValue(new_value)
        self.progressBar.update()

    def on_finished(self):
        self.local_timer.stop()
        self.progressBar.setValue(100)
        self.finished_files = self.total_files - self.error_files
        NoticeDialog(self, f'[Notice]: Transform Successfully!\n'
                           f'Total: {self.total_files}\n'
                           f'Successful: {self.finished_files}\n'
                           f'Failed: {self.error_files}')

    def get_config(self) -> Dict[str, List[float] | str | bool | int]:
        config = {
            'x': [float(self.doubleSpinBox.text()), float(self.doubleSpinBox_2.text())],
            'y': [float(self.doubleSpinBox_3.text()), float(self.doubleSpinBox_4.text())],
            'z': [float(self.doubleSpinBox_5.text()), float(self.doubleSpinBox_6.text())],
            'rotate_method': self.comboBox.currentText(),
            'is_zoom': True if self.comboBox_2.currentText() == 'True' else False,
        }
        return config

    def write_csv_animation(self, file_name: str = './csv/output.csv') -> None:
        try:
            tar = os.listdir(self.input_directory)
            with open(file_name, 'w', newline='', encoding="utf-8") as f_decode:
                _writer = csv.writer(f_decode)
                for obj_name in tar:
                    if obj_name.endswith('.obj'):
                        obj_p = Tools.edit_obj_data(Obj(os.path.join(self.input_directory, obj_name)),
                                                    self.get_config())
                        _writer.writerow(str(_i) for _i in obj_p.pre_formate_to_bin()[1])
        except Exception as e:
            ErrorDialog(self, e)


class AnimationEditor(AnimationPlayer):
    def __init__(self):
        super().__init__()
        self.input_directory: str = ""
        self.binary_stream: bytes = basic_bin_bytes
        self.init_build()

    def init_build(self) -> None:
        self.action_open.triggered.connect(self.get_data)
        self.action_csv.triggered.connect(lambda: self.output_to_csv())
        self.action_bin.triggered.connect(lambda: self.output_to_binary())

    def get_data(self) -> None:
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
        if self.input_directory:
            try:
                with open(directory, "w") as csv_out:
                    csv_out.write(Tools.animation_deserialize(self.move_bin))
                NoticeDialog(self)
            except Exception as e:
                ErrorDialog(self, e)
        else:
            NoticeDialog(self, "You Haven't Chose A File!")

    def output_to_binary(self, directory: str = "./animation/encode_bin.bin") -> None:
        if self.input_directory:
            try:
                with open(directory, 'wb') as bin_out:
                    bin_out.write(self.content)
                NoticeDialog(self)
            except Exception as e:
                ErrorDialog(self, e)
        else:
            NoticeDialog(self, "You Haven't Chose A File!")
