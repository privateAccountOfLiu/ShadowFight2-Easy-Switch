from __future__ import annotations

from typing import List

from PySide6 import QtCore, QtWidgets, QtGui

from python.ui.page_level_ui_widgets import ToolMainWindow


class StartupWindow(QtWidgets.QWidget):
    """Startup window that shows a loading animation before the main tool window."""

    def __init__(self) -> None:
        """Initialize the frameless startup window and its internal state."""
        super().__init__(None, QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setStyleSheet("background-color: rgb(245,246,248);")

        self._progress = 0
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._on_tick)

        self._build_ui()

    def _build_ui(self) -> None:
        """Build all widgets and layouts for the startup window."""
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        container = QtWidgets.QFrame(self)
        container.setObjectName("startupContainer")
        container.setStyleSheet(
            "#startupContainer {"
            "  background-color: rgb(245,246,248);"
            "  border-radius: 16px;"
            "}"
        )

        vbox = QtWidgets.QVBoxLayout(container)
        vbox.setContentsMargins(24, 24, 24, 24)
        vbox.setSpacing(16)

        icon_label = QtWidgets.QLabel(container)
        icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        icon = QtGui.QIcon(":/icons/icon")
        pix = icon.pixmap(64, 64)
        icon_label.setPixmap(pix)

        title_label = QtWidgets.QLabel("Shadow Fight 2 Easy Switch", container)
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        font = title_label.font()
        font.setPointSize(14)
        font.setBold(True)
        title_label.setFont(font)

        self._progress_bar = QtWidgets.QProgressBar(container)
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(0)
        self._progress_bar.setTextVisible(False)
        self._progress_bar.setFixedHeight(6)

        self._status_label = QtWidgets.QLabel("Loading...", container)
        self._status_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        vbox.addWidget(icon_label)
        vbox.addWidget(title_label)
        vbox.addWidget(self._progress_bar)
        vbox.addWidget(self._status_label)

        layout.addWidget(container)

        self.resize(420, 220)
        self._center_on_screen()

    def _center_on_screen(self) -> None:
        """Center the startup window on the primary screen."""
        screen = QtWidgets.QApplication.primaryScreen()
        if not screen:
            return
        geo = screen.availableGeometry()
        self.move(
            geo.center().x() - self.width() // 2,
            geo.center().y() - self.height() // 2,
        )

    def start(self) -> None:
        """Start the loading animation and show the startup window."""
        self._progress = 0
        self._progress_bar.setValue(0)
        self._status_label.setText("Loading...")
        self.show()
        self._timer.start(25)

    @QtCore.Slot()
    def _on_tick(self) -> None:
        """Advance the progress bar each tick and open main window when complete."""
        self._progress += 2
        if self._progress > 100:
            self._progress = 100
        self._progress_bar.setValue(self._progress)

        if self._progress >= 100:
            self._timer.stop()
            self._open_main()

    def _open_main(self) -> None:
        """Create and show the main window, then close the startup window."""
        app = QtWidgets.QApplication.instance()
        if app is None:
            return

        self._main_window = ToolMainWindow()
        self._main_window.show()
        app.setActiveWindow(self._main_window)
        self.close()

