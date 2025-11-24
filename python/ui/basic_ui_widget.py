from typing import Dict

from PyQt6 import QtWidgets, QtGui, uic, QtCore

from python.core.core_functions import *
from python.ui.extract_widget import ObjModelViewer, WorkerThread, AnimationPlayer
from python.ui.notice_dialog_widget import ErrorDialog, NoticeDialog
from python.util.tools import Tools


class Page(QtWidgets.QDialog):
    def __init__(self, ui_path: str):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon(get_dir('./res/ui/icon/icon.png')))
        if ui_path:
            self.ui_path = get_dir(ui_path)
            uic.loadUi(self.ui_path, self)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowMaximizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowMinimizeButtonHint, False)

    def init_build(self) -> None:
        pass

    def output(self) -> None:
        pass

    def get_data(self) -> None:
        pass

    def file_chose(self, regulation: str = "*") -> str:
        directory, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Chose Files", "", regulation,
            options=QtWidgets.QFileDialog.Option.DontUseNativeDialog
        )
        return directory

    def dir_chose(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Chose Directory", "",
            QtWidgets.QFileDialog.Option.DontUseNativeDialog
        )
        return directory


class ToolMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.pushButton_1 = self.pushButton_2 = self.pushButton_3 = self.pushButton_4 = None
        ui_path = get_dir('./res/ui/pages/main_page.ui')
        uic.loadUi(ui_path, self)
        self.page1 = PageObjToXml()
        self.page2 = PageObjsToCsv()
        self.page3 = AnimationEditor()
        self.init_build()

    def init_build(self):
        self.setWindowIcon(QtGui.QIcon(get_dir('./res/ui/icon/icon.png')))
        self.setWindowFlag(QtCore.Qt.WindowType.WindowMaximizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowMinimizeButtonHint, False)
        self.pushButton_1.clicked.connect(self.page1.show)
        self.pushButton_2.clicked.connect(self.page2.show)
        self.pushButton_3.clicked.connect(self.page3.show)


class PageObjToXml(Page):
    def __init__(self):
        self.spinBox = None
        self.comboBox = None
        self.comboBox_2 = None
        self.comboBox_4 = None
        self.doubleSpinBox_2 = None
        self.doubleSpinBox_6 = None
        self.doubleSpinBox_5 = None
        self.doubleSpinBox_4 = None
        self.doubleSpinBox_3 = None
        self.doubleSpinBox = None
        self.buttonBox = None
        self.pushButton = None
        self.textBrowser = None

        super().__init__('./res/ui/pages/obj_to_xml_page.ui')
        self.input_directory: str = ""
        self.obj_data: str = ""
        self.vtk_viewer = ObjModelViewer(parent=self)
        self.init_build()

    def init_build(self) -> None:
        self.vtk_viewer.setGeometry(380, 70, 240, 260)
        self.vtk_viewer.show()
        self.pushButton.clicked.connect(self.get_data)
        self.buttonBox.accepted.connect(self.output)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.apply_config)

    def get_data(self) -> None:
        self.input_directory = self.file_chose("WaveFront(*.obj)")
        if self.input_directory:
            try:
                self.textBrowser.setText(self.input_directory)
                with open(self.input_directory, "r") as read_file:
                    self.obj_data = read_file.read()
                self.vtk_viewer.add_mesh(self.obj_data)
            except Exception as e:
                ErrorDialog(self, e)

    def apply_config(self):
        if self.input_directory:
            try:
                self.obj_data = edit_obj_data(self.get_config(), self.input_directory).to_text()
                self.vtk_viewer.add_mesh(self.obj_data)
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

    def output(self):
        if self.input_directory:
            try:
                config = self.get_config()
                obj = edit_obj_data(config, self.input_directory)
                write_xml(config, obj)
                NoticeDialog(self)
                self.close()
            except Exception as e:
                ErrorDialog(self, e)
        else:
            self.close()


class PageObjsToCsv(Page):
    def __init__(self):
        self.comboBox_2 = None
        self.comboBox = None
        self.doubleSpinBox_6 = None
        self.doubleSpinBox_5 = None
        self.doubleSpinBox_4 = None
        self.doubleSpinBox_3 = None
        self.doubleSpinBox_2 = None
        self.doubleSpinBox = None
        self.pushButton = None
        self.textBrowser = None
        self.buttonBox = None
        self.progressBar = None
        self.worker = None

        super().__init__('./res/ui/pages/objs_to_csv_page.ui')
        self.input_directory: str = ""
        self.csv_data: str = ""
        self.total_files = self.finished_files = self.error_files = 0
        self.local_timer = QtCore.QTimer()
        self.init_build()

    def init_build(self) -> None:
        self.pushButton.clicked.connect(self.get_data)
        self.buttonBox.accepted.connect(self.output)
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
                self.progressBar.setValue(0)
                self.worker = WorkerThread(self.input_directory, "./objs_to_bin",
                                           lambda: write_csv_bin(self.get_config(), self.input_directory)
                                           )
                self.finished_files += 1
            except Exception as e:
                ErrorDialog(self, e)
                self.error_files += 1
        self.worker.finished.connect(self.on_finished)
        self.worker.start()
        self.local_timer.start(50)

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


class AnimationEditor(AnimationPlayer, Page):
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

    def output_to_csv(self, directory: str = "./bin/decode_bin.csv") -> None:
        try:
            with open(directory, "w") as csv_out:
                csv_out.write(Tools.animation_deserialize(self.move_bin))
            NoticeDialog(self)
        except Exception as e:
            ErrorDialog(self, e)

    def output_to_binary(self, directory: str = "./bin/encode_bin.bin"):
        try:
            with open(directory, 'wb') as bin_out:
                bin_out.write(self.content)
            NoticeDialog(self)
        except Exception as e:
            ErrorDialog(self, e)
