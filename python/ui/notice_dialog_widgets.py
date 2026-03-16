from PySide6 import QtWidgets, QtCore, QtGui

from python.core.core_functions import get_error_msg, write_to_log
from python.util import i18n


class ErrorDialog(QtWidgets.QMessageBox):
    """Message box that shows an error with a translated title and full traceback text."""

    def __init__(self, parent, e):
        super().__init__(parent)
        self.error_msg = get_error_msg(e)
        write_to_log(self.error_msg)
        self.critical(
            parent,
            i18n.tr("dialog.error.title"),
            f'[Something Wrong!]: {self.error_msg}',
            self.StandardButton.Ok,
        )


class NoticeDialog(QtWidgets.QMessageBox):
    """Simple information dialog with a translated title and optional custom message."""

    def __init__(self, parent, msg: str | None = None):
        super().__init__(parent)
        self.msg = msg or i18n.tr("dialog.notice.default")
        QtWidgets.QMessageBox().information(
            self,
            i18n.tr("dialog.notice.title"),
            self.msg,
            QtWidgets.QMessageBox.StandardButton.Ok,
        )


class HelpDialog(QtWidgets.QDialog):
    """Shared help/about dialog for ModelPlayer and AnimationPlayer with translations."""

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(i18n.tr("about.title"))
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setMinimumSize(420, 260)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        icon_label = QtWidgets.QLabel(self)
        icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        icon = QtGui.QIcon(":/icons/icon")
        pix = icon.pixmap(72, 72)
        icon_label.setPixmap(pix)

        info_layout = QtWidgets.QFormLayout()
        info_layout.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        info_layout.setHorizontalSpacing(12)
        info_layout.setVerticalSpacing(8)
        info_layout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

        author_label = QtWidgets.QLabel("PrivateLiu", self)
        version_label = QtWidgets.QLabel("2.3.0", self)

        link_label = QtWidgets.QLabel(self)
        link_label.setText(
            '<a href="https://github.com/privateAccountOfLiu/ShadowFight2-Easy-Switch">'
            f'{i18n.tr("about.github.link")}'
            "</a>"
        )
        link_label.setTextFormat(QtCore.Qt.TextFormat.RichText)
        link_label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)
        link_label.setOpenExternalLinks(True)

        info_layout.addRow(i18n.tr("about.author.label"), author_label)
        info_layout.addRow(i18n.tr("about.version.label"), version_label)
        info_layout.addRow(i18n.tr("about.github.label"), link_label)

        license_label = QtWidgets.QLabel(self)
        license_label.setWordWrap(True)
        license_label.setText(i18n.tr("about.license.text"))

        close_button = QtWidgets.QPushButton(i18n.tr("about.close"), self)
        close_button.clicked.connect(self.accept)

        layout.addWidget(icon_label)
        layout.addLayout(info_layout)
        layout.addWidget(license_label)
        layout.addStretch(1)
        layout.addWidget(close_button, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

