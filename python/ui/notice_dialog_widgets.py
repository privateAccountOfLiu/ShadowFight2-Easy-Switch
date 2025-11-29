from PySide6 import QtWidgets

from python.core.core_functions import get_error_msg, write_to_log


class ErrorDialog(QtWidgets.QMessageBox):
    def __init__(self, parent, e):
        super().__init__(parent)
        self.error_msg = get_error_msg(e)
        write_to_log(self.error_msg)
        self.critical(parent, "Error!", f'[Something Wrong!]: {self.error_msg}', self.StandardButton.Ok)


class NoticeDialog(QtWidgets.QMessageBox):
    def __init__(self, parent, msg=f'[Notice]: Transform Successfully!'):
        super().__init__(parent)
        self.msg = msg
        QtWidgets.QMessageBox().information(self, 'Notice', self.msg, QtWidgets.QMessageBox.StandardButton.Ok)
