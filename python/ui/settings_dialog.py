from __future__ import annotations

from typing import Literal

from PySide6 import QtWidgets, QtCore

from python.util.settings import AppSettings
from python.util import i18n


LanguageCode = Literal["en", "zh-CN"]


class SettingsDialog(QtWidgets.QDialog):
    """Application settings dialog shared by ModelPlayer and AnimationPlayer."""

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        """Initialize the settings dialog and load current AppSettings values."""
        super().__init__(parent)
        self._settings = AppSettings.instance()

        self.setWindowTitle(i18n.tr("settings.title"))
        self.setModal(True)
        self.setMinimumSize(440, 220)

        self._build_ui()
        self._load_values()

    def _build_ui(self) -> None:
        """Create all form controls and wire up button signals."""
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        form = QtWidgets.QFormLayout()
        form.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        form.setHorizontalSpacing(10)
        form.setVerticalSpacing(8)

        self.edit_model_dir = QtWidgets.QLineEdit(self)
        self.btn_model_browse = QtWidgets.QPushButton("...", self)
        self.btn_model_browse.setFixedWidth(32)
        model_layout = QtWidgets.QHBoxLayout()
        model_layout.addWidget(self.edit_model_dir)
        model_layout.addWidget(self.btn_model_browse)

        self.edit_animation_dir = QtWidgets.QLineEdit(self)
        self.btn_animation_browse = QtWidgets.QPushButton("...", self)
        self.btn_animation_browse.setFixedWidth(32)
        animation_layout = QtWidgets.QHBoxLayout()
        animation_layout.addWidget(self.edit_animation_dir)
        animation_layout.addWidget(self.btn_animation_browse)

        self.combo_language = QtWidgets.QComboBox(self)
        self.combo_language.addItem(i18n.tr("settings.language.en"), "en")
        self.combo_language.addItem(i18n.tr("settings.language.zh"), "zh-CN")

        form.addRow(i18n.tr("settings.export.model"), model_layout)
        form.addRow(i18n.tr("settings.export.animation"), animation_layout)
        form.addRow(i18n.tr("settings.language"), self.combo_language)

        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel,
            QtCore.Qt.Orientation.Horizontal,
            self,
        )

        layout.addLayout(form)
        layout.addWidget(button_box)

        self.btn_model_browse.clicked.connect(self._on_browse_model)
        self.btn_animation_browse.clicked.connect(self._on_browse_animation)
        button_box.accepted.connect(self._on_accept)
        button_box.rejected.connect(self.reject)

    def _load_values(self) -> None:
        """Load current values from AppSettings into widgets."""
        self.edit_model_dir.setText(self._settings.export_dir_model)
        self.edit_animation_dir.setText(self._settings.export_dir_animation)

        current_lang = self._settings.language
        index = self.combo_language.findData(current_lang)
        if index < 0:
            index = 0
        self.combo_language.setCurrentIndex(index)

    def _on_browse_model(self) -> None:
        """Open a directory dialog and set the chosen model export directory."""
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, i18n.tr("settings.export.model"))
        if directory:
            self.edit_model_dir.setText(directory)

    def _on_browse_animation(self) -> None:
        """Open a directory dialog and set the chosen animation export directory."""
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, i18n.tr("settings.export.animation"))
        if directory:
            self.edit_animation_dir.setText(directory)

    def _on_accept(self) -> None:
        """Persist settings and inform user about language reload behavior."""
        self._settings.export_dir_model = self.edit_model_dir.text() or "./model"
        self._settings.export_dir_animation = self.edit_animation_dir.text() or "./animation"
        lang_data = self.combo_language.currentData()
        if lang_data in ("en", "zh-CN"):
            self._settings.language = lang_data
        self._settings.save()

        QtWidgets.QMessageBox.information(
            self,
            i18n.tr("settings.title"),
            i18n.tr("settings.restart.info"),
            QtWidgets.QMessageBox.StandardButton.Ok,
        )

        self.accept()

