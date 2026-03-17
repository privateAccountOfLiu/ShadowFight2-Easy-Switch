from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            Qt, QTimer, QSize)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (QGridLayout, QLabel, QPushButton, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout,
                               QSlider, QMenuBar, QMenu, QCheckBox, QDoubleSpinBox, QComboBox, QProgressBar,
                               QTextBrowser, QDialogButtonBox, QStatusBar, QSpinBox, QFileDialog, QFrame)
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl

from python.core.core_classes import MoveBin
from python.ui.additional_widgets import AxisHUDWidget
from python.ui.notice_dialog_widgets import ErrorDialog, HelpDialog
from python.ui.settings_dialog import SettingsDialog
from python.util import i18n
from python.util.values import basic_bin_bytes


class Page(QMainWindow):
    """Base window class that provides common file dialogs and shared actions."""

    def __init__(self, *args, **kwargs):
        """Initialize the page window with icon and fixed window flags."""
        super().__init__(*args, **kwargs)
        self.setWindowIcon(QIcon(u":/icons/icon"))
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)
        self.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, False)

    def init_build(self) -> None:
        """Hook for subclasses to initialize their specific UI components."""
        pass

    def output(self) -> None:
        """Hook for subclasses to implement export or output behavior."""
        pass

    def get_data(self) -> None:
        """Hook for subclasses to implement input or data-loading behavior."""
        pass

    def show_help_dialog(self) -> None:
        """Open the shared help/about dialog."""
        dialog = HelpDialog(self)
        dialog.exec()

    def show_settings_dialog(self) -> None:
        """Open the shared application settings dialog."""
        dialog = SettingsDialog(self)
        dialog.exec()

    def file_chose(self, regulation: str = "*") -> str:
        """Show a file open dialog and return the selected file path."""
        directory, _ = QFileDialog.getOpenFileName(
            self,
            "Chose Files",
            "",
            regulation,
            options=QFileDialog.Option.DontUseNativeDialog,
        )
        return directory

    def dir_chose(self) -> str:
        """Show a directory chooser dialog and return the selected directory path."""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Chose Directory",
            "",
            QFileDialog.Option.DontUseNativeDialog,
        )
        return directory


class BasicToolMainWindow(QMainWindow):
    """Landing window that lets the user choose between the main tool pages."""

    def __init__(self, main_window, parent=None):
        """Create the main landing window and configure its UI layout."""
        super().__init__(parent=parent)
        self.label = None
        self.pushButton_1 = None
        self.pushButton_2 = None
        self.pushButton_3 = None
        self.gridLayout = None
        self.gridLayoutWidget = None
        self.centralwidget = None
        self.setup_ui(main_window)

    def setup_ui(self, main_window):
        """Build the landing window layout and hook up the three entry buttons."""
        if not main_window.objectName():
            main_window.setObjectName(u"MainWindow")
        main_window.resize(550, 400)
        self.centralwidget = QWidget(main_window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(40, 150, 471, 211))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_3 = QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 2, 0, 1, 2)

        self.pushButton_2 = QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 0, 1, 2)

        self.pushButton_1 = QPushButton(self.gridLayoutWidget)
        self.pushButton_1.setObjectName(u"pushButton_1")
        self.gridLayout.addWidget(self.pushButton_1, 0, 0, 1, 2)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 550, 150))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_window.setCentralWidget(self.centralwidget)

        self.re_translate_ui(main_window)
        QMetaObject.connectSlotsByName(main_window)

    def re_translate_ui(self, main_window):
        """Apply translated texts for the main title and entry buttons."""
        main_window.setWindowTitle(i18n.tr("app.title"))
        self.pushButton_3.setText(i18n.tr("main.button.animation"))
        self.pushButton_2.setText(i18n.tr("main.button.csv"))
        self.pushButton_1.setText(i18n.tr("main.button.model"))
        self.label.setText(
            "<html><head/><body><p>"
            "<span style=\" font-size:24pt; font-weight:700;\">"
            "Shadow Fight 2 Easy Switch"
            "</span></p></body></html>"
        )


class ModelPlayer(Page):
    """Main window for previewing, configuring and exporting 3D model files."""

    def __init__(self, main_window, parent=None):
        """Initialize all UI fields and build the model player layout."""
        super().__init__(parent)
        self.statusBar_A = None
        self.menuHelp = None
        self.menuSetting = None
        self.menuExport = None
        self.menuFile = None
        self.menubar = None
        self.pushButton = None
        self.doubleSpinBox_3 = None
        self.label_6 = None
        self.doubleSpinBox_6 = None
        self.doubleSpinBox_4 = None
        self.label_9 = None
        self.spinBox = None
        self.label_4 = None
        self.doubleSpinBox = None
        self.doubleSpinBox_2 = None
        self.checkBox = None
        self.comboBox_4 = None
        self.comboBox = None
        self.label_8 = None
        self.label_5 = None
        self.doubleSpinBox_5 = None
        self.label_7 = None
        self.label_3 = None
        self.comboBox_2 = None
        self.comboBox_2 = None
        self.gridLayout = None
        self.gridLayout = None
        self.gridLayoutWidget = None
        self.gridLayoutWidget = None
        self.centralwidget = None
        self.action_obj = None
        self.action_xml = None
        self.actionOpen = None
        self.statue_label = QLabel(f"Nodes: 0, Edges: 0, Triangles: 0, X Scope: [], Y Scope: [], Z Scope: []")
        self.setup_ui(main_window)

    def setup_ui(self, main_window):
        """Create all widgets, menus and status bar for the model player."""
        if not main_window.objectName():
            main_window.setObjectName(u"MainWindow")
        main_window.resize(800, 600)
        main_window.setUnifiedTitleAndToolBarOnMac(False)
        self.actionOpen = QAction(main_window)
        self.actionOpen.setObjectName(u"actionOpen")
        self.action_xml = QAction(main_window)
        self.action_xml.setObjectName(u"action_xml")
        self.action_obj = QAction(main_window)
        self.action_obj.setObjectName(u"action_obj")
        self.centralwidget = QWidget(main_window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 230, 320))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.comboBox_2 = QComboBox(self.gridLayoutWidget)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.gridLayout.addWidget(self.comboBox_2, 6, 1, 1, 2)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.doubleSpinBox_5 = QDoubleSpinBox(self.gridLayoutWidget)
        self.doubleSpinBox_5.setObjectName(u"doubleSpinBox_5")
        self.doubleSpinBox_5.setMinimum(-100.000000000000000)
        self.doubleSpinBox_5.setMaximum(100.000000000000000)
        self.doubleSpinBox_5.setSingleStep(0.200000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_5, 4, 1, 1, 1)

        self.pushButton = QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 8, 0, 1, 3)

        self.label_5 = QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.label_8 = QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_8, 7, 0, 1, 1)

        self.comboBox = QComboBox(self.gridLayoutWidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 6, 1, 1, 2)

        self.comboBox_4 = QComboBox(self.gridLayoutWidget)
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.setObjectName(u"comboBox_4")

        self.gridLayout.addWidget(self.comboBox_4, 5, 1, 1, 2)

        self.checkBox = QCheckBox(self.gridLayoutWidget)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout.addWidget(self.checkBox, 0, 0, 1, 3)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.gridLayoutWidget)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        self.doubleSpinBox_2.setMinimum(-1000.000000000000000)
        self.doubleSpinBox_2.setMaximum(1000.000000000000000)
        self.doubleSpinBox_2.setSingleStep(0.500000000000000)
        self.doubleSpinBox_2.setValue(-150.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_2, 2, 2, 1, 1)

        self.doubleSpinBox = QDoubleSpinBox(self.gridLayoutWidget)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setMinimum(-1000.000000000000000)
        self.doubleSpinBox.setMaximum(1000.000000000000000)
        self.doubleSpinBox.setSingleStep(0.500000000000000)
        self.doubleSpinBox.setValue(-150.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox, 2, 1, 1, 1)

        self.comboBox_2 = QComboBox(self.gridLayoutWidget)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.gridLayout.addWidget(self.comboBox_2, 1, 1, 1, 2)

        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.spinBox = QSpinBox(self.gridLayoutWidget)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1000000)

        self.gridLayout.addWidget(self.spinBox, 7, 1, 1, 2)

        self.label_9 = QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_9, 5, 0, 1, 1)

        self.label_7 = QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 1)

        self.doubleSpinBox_4 = QDoubleSpinBox(self.gridLayoutWidget)
        self.doubleSpinBox_4.setObjectName(u"doubleSpinBox_4")
        self.doubleSpinBox_4.setMinimum(-100.000000000000000)
        self.doubleSpinBox_4.setMaximum(1000.000000000000000)
        self.doubleSpinBox_4.setValue(280.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_4, 3, 2, 1, 1)

        self.doubleSpinBox_6 = QDoubleSpinBox(self.gridLayoutWidget)
        self.doubleSpinBox_6.setObjectName(u"doubleSpinBox_6")
        self.doubleSpinBox_6.setMinimum(-100.000000000000000)
        self.doubleSpinBox_6.setMaximum(100.000000000000000)
        self.doubleSpinBox_6.setSingleStep(0.200000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_6, 4, 2, 1, 1)

        self.label_6 = QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_6, 6, 0, 1, 1)

        self.doubleSpinBox_3 = QDoubleSpinBox(self.gridLayoutWidget)
        self.doubleSpinBox_3.setObjectName(u"doubleSpinBox_3")
        self.doubleSpinBox_3.setMinimum(-100.000000000000000)
        self.doubleSpinBox_3.setMaximum(1000.000000000000000)
        self.doubleSpinBox_3.setSingleStep(1.000000000000000)
        self.doubleSpinBox_3.setValue(-12.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_3, 3, 1, 1, 1)

        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(main_window)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        icon = QIcon()
        icon.addFile(u":/icons/file", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menuFile.setIcon(icon)
        self.menuExport = QMenu(self.menuFile)
        self.menuExport.setObjectName(u"menuExport")
        self.menuSetting = QMenu(self.menubar)
        self.menuSetting.setObjectName(u"menuSetting")
        icon1 = QIcon()
        icon1.addFile(u":/icons/setting", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menuSetting.setIcon(icon1)
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        icon2 = QIcon()
        icon2.addFile(u":/icons/help", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menuHelp.setIcon(icon2)
        main_window.setMenuBar(self.menubar)
        self.statusBar_A = QStatusBar(main_window)
        self.statusBar_A.setObjectName(u"statusBar")
        self.statusBar_A.addWidget(self.statue_label)
        main_window.setStatusBar(self.statusBar_A)

        self.actionHelpAbout = QAction(main_window)
        self.actionHelpAbout.setObjectName(u"actionHelpAbout")
        self.actionSettings = QAction(main_window)
        self.actionSettings.setObjectName(u"actionSettings")

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menuExport.addAction(self.action_xml)
        self.menuExport.addAction(self.action_obj)
        self.menuSetting.addAction(self.actionSettings)
        self.menuHelp.addAction(self.actionHelpAbout)

        self.re_translate_ui(main_window)

        QMetaObject.connectSlotsByName(main_window)

        self.actionHelpAbout.triggered.connect(self.show_help_dialog)
        self.actionSettings.triggered.connect(self.show_settings_dialog)

    def re_translate_ui(self, main_window):
        """Apply texts for actions, labels and menus, including i18n-aware labels."""
        main_window.setWindowTitle("ModelPlayer")
        self.actionOpen.setText("Open")
        self.action_xml.setText("xml")
        self.action_obj.setText("(WaveFront)obj")
        self.comboBox_2.setItemText(0, "False")
        self.comboBox_2.setItemText(1, "True")

        self.label_3.setText(i18n.tr("label.range_x"))
        self.label_7.setText(i18n.tr("label.is_zoom"))
        self.label_5.setText(i18n.tr("label.range_z"))
        self.label_8.setText(i18n.tr("label.begin_id"))
        self.comboBox.setItemText(0, "xyz")
        self.comboBox.setItemText(1, "xzy")
        self.comboBox.setItemText(2, "yxz")
        self.comboBox.setItemText(3, "yzx")
        self.comboBox.setItemText(4, "zxy")
        self.comboBox.setItemText(5, "zyx")

        self.comboBox_4.setItemText(0, "weapon")
        self.comboBox_4.setItemText(1, "helm")
        self.comboBox_4.setItemText(2, "ranged")
        self.comboBox_4.setItemText(3, "armor_a")
        self.comboBox_4.setItemText(4, "armor_b")
        self.comboBox_4.setItemText(5, "armor_c")

        self.checkBox.setText(i18n.tr("label.advanced_setting"))
        self.label_4.setText(i18n.tr("label.range_y"))
        self.label_9.setText(i18n.tr("label.type"))
        self.label_6.setText(i18n.tr("label.rotate"))
        self.pushButton.setText(i18n.tr("button.apply"))

        # 菜单与设置项使用多语言资源
        self.menuFile.setTitle(i18n.tr("menu.file"))
        self.menuExport.setTitle(i18n.tr("menu.export"))
        self.menuSetting.setTitle(i18n.tr("menu.setting"))
        self.menuHelp.setTitle(i18n.tr("menu.help"))

        self.actionHelpAbout.setText(i18n.tr("menu.help.about"))
        self.actionSettings.setText(i18n.tr("menu.setting.settings"))



class BasicYieldCsvPage(Page):
    """Base page that provides common controls for CSV batch conversion tools."""

    def __init__(self, main_window, parent=None):
        """Initialize the CSV page layout and connect designer-generated widgets."""
        super().__init__(parent)
        self.buttonBox = None
        self.label_6 = None
        self.label = None
        self.doubleSpinBox_2 = None
        self.label_2 = None
        self.progressBar = None
        self.textBrowser = None
        self.doubleSpinBox_5 = None
        self.comboBox_2 = None
        self.doubleSpinBox_4 = None
        self.doubleSpinBox_6 = None
        self.doubleSpinBox = None
        self.label_title = None
        self.pushButton = None
        self.comboBox = None
        self.doubleSpinBox_3 = None
        self.label_4 = None
        self.label_3 = None
        self.label_5 = None
        self.gridLayout = None
        self.gridLayoutWidget = None
        self.centralwidget = None
        self.setup_ui(main_window)

    def setup_ui(self, main_window):
        """Build the CSV configuration panel, progress bar and button box."""
        if not main_window.objectName():
            main_window.setObjectName(u"MainWindow")
        main_window.resize(400, 400)
        self.centralwidget = QWidget(main_window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(20, 10, 360, 330))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)

        self.doubleSpinBox_3 = QDoubleSpinBox(self.gridLayoutWidget)
        self.doubleSpinBox_3.setObjectName(u"doubleSpinBox_3")
        self.doubleSpinBox_3.setMinimum(-5000.000000000000000)
        self.doubleSpinBox_3.setMaximum(5000.000000000000000)
        self.doubleSpinBox_3.setSingleStep(1.000000000000000)
        self.doubleSpinBox_3.setValue(0.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_3, 3, 1, 1, 1)

        self.pushButton = QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)

        self.label_title = QLabel(self.gridLayoutWidget)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_title, 0, 0, 1, 3)

        self.doubleSpinBox = QDoubleSpinBox(self.gridLayoutWidget)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setMinimum(-5000.000000000000000)
        self.doubleSpinBox.setMaximum(5000.000000000000000)
        self.doubleSpinBox.setSingleStep(1.000000000000000)
        self.doubleSpinBox.setValue(0.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox, 2, 1, 1, 1)

        self.comboBox = QComboBox(self.gridLayoutWidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 5, 1, 1, 2)

        self.doubleSpinBox_6 = QDoubleSpinBox(self.gridLayoutWidget)
        self.doubleSpinBox_6.setObjectName(u"doubleSpinBox_6")
        self.doubleSpinBox_6.setMinimum(-5000.000000000000000)
        self.doubleSpinBox_6.setMaximum(5000.000000000000000)
        self.doubleSpinBox_6.setSingleStep(1.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_6, 4, 2, 1, 1)

        self.doubleSpinBox_4 = QDoubleSpinBox(self.gridLayoutWidget)
        self.doubleSpinBox_4.setObjectName(u"doubleSpinBox_4")
        self.doubleSpinBox_4.setMinimum(-5000.000000000000000)
        self.doubleSpinBox_4.setMaximum(5000.000000000000000)
        self.doubleSpinBox_4.setValue(0.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_4, 3, 2, 1, 1)

        self.comboBox_2 = QComboBox(self.gridLayoutWidget)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.gridLayout.addWidget(self.comboBox_2, 6, 1, 1, 2)

        self.doubleSpinBox_5 = QDoubleSpinBox(self.gridLayoutWidget)
        self.doubleSpinBox_5.setObjectName(u"doubleSpinBox_5")
        self.doubleSpinBox_5.setMinimum(-5000.000000000000000)
        self.doubleSpinBox_5.setMaximum(5000.000000000000000)
        self.doubleSpinBox_5.setSingleStep(1.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_5, 4, 1, 1, 1)

        self.progressBar = QProgressBar(self.gridLayoutWidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.gridLayout.addWidget(self.progressBar, 8, 0, 1, 3)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.gridLayoutWidget)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        self.doubleSpinBox_2.setMinimum(-5000.000000000000000)
        self.doubleSpinBox_2.setMaximum(5000.000000000000000)
        self.doubleSpinBox_2.setSingleStep(1.000000000000000)
        self.doubleSpinBox_2.setValue(0.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_2, 2, 2, 1, 1)

        self.textBrowser = QTextBrowser(self.gridLayoutWidget)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout.addWidget(self.textBrowser, 1, 1, 1, 2)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.label_6 = QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_6, 7, 0, 1, 3)

        self.buttonBox = QDialogButtonBox(self.centralwidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(0, 350, 400, 35))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)
        main_window.setCentralWidget(self.centralwidget)

        self.re_translate_ui(main_window)

        QMetaObject.connectSlotsByName(main_window)
    # setupUi

    def re_translate_ui(self, main_window):
        main_window.setWindowTitle(i18n.tr("csv.window.title"))
        self.label_5.setText(i18n.tr("label.is_zoom"))
        self.label_3.setText(i18n.tr("label.range_z"))
        self.label_4.setText(i18n.tr("label.rotate"))
        self.pushButton.setText(i18n.tr("csv.button.select_dir"))
        self.label_title.setText(i18n.tr("csv.label.title"))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"xyz", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"xzy", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"yxz", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"yzx", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"zxy", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"zyx", None))

        self.comboBox_2.setItemText(0, QCoreApplication.translate("MainWindow", u"False", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("MainWindow", u"True", None))

        self.label_2.setText(i18n.tr("label.range_y"))
        self.label.setText(i18n.tr("label.range_x"))
        self.label_6.setText(i18n.tr("csv.label.progress"))


# noinspection PyUnresolvedReferences
class AnimationPlayer(Page):
    """3D animation player that visualizes skeletal motion from binary or CSV data."""

    def __init__(self, parent=None):
        """Initialize animation state, 3D view widgets and playback controls."""
        super().__init__(parent)
        self.content = basic_bin_bytes
        self.sphere_radius = 0
        self.data_bounds = None
        self.num_nodes = 0
        self.num_frames = 0
        self.frames_data = []
        # 视图平移偏移量：仅在 X/Z 方向居中，Y 保持与源动画一致
        self.view_offset = np.zeros(3, dtype=float)
        self.move_bin = MoveBin.build_binary(self.content)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.control_layout = QHBoxLayout()
        self.layout = QVBoxLayout(self.central_widget)

        self.view_frame = QFrame(self.central_widget)
        self.view_frame.setObjectName("animationViewerFrame")
        self.view_frame.setStyleSheet(
            "#animationViewerFrame {"
            "  background-color: rgb(245,246,248);"
            "  border: 1px solid #4b5563;"
            "  border-radius: 8px;"
            "}"
        )
        self.view_frame_layout = QVBoxLayout(self.view_frame)
        self.view_frame_layout.setContentsMargins(4, 4, 4, 4)

        self.view = gl.GLViewWidget(self.view_frame)
        self.view.setObjectName("animationGLView")
        self.view.setBackgroundColor((245, 246, 248))
        self.view.opts['distance'] = 10
        self.view_frame_layout.addWidget(self.view)

        # HUD 坐标轴需要与二进制动画中逻辑坐标系保持一致。
        # 动画数据在 _transform_point 中做了 (x, y, z) -> (z, x, y) 的变换，
        # 即 GL 坐标系中：X'⇐原 Z，Y'⇐原 X，Z'⇐原 Y。
        # 下面的映射让 HUD 上的 X/Y/Z 标签对应“原始数据”的坐标轴方向。
        # HUD 中 X/Y 轴与当前视觉效果对齐：
        # - 让 X 轴对应你感知中的“左右”方向
        # - 让 Y 轴对应你感知中的“上下”方向
        axis_mapping = {
            "X": (0.0, 0.0, 1.0),
            "Y": (0.0, -1.0, 0.0),
            "Z": (1.0, 0.0, 0.0),
        }
        self._axis_hud = AxisHUDWidget(self.view, self.view, axis_mapping=axis_mapping)
        self._axis_hud.show()
        self.timer = QTimer()
        self.play_button = QPushButton()
        self.prev_button = QPushButton()
        self.next_button = QPushButton()
        self.reset_camera_button = QPushButton()
        self.frame_slider = QSlider(Qt.Orientation.Horizontal)
        self.action_open = QAction(self)
        self.action_csv = QAction(self)
        self.action_bin = QAction(self)
        self.menubar = QMenuBar(self)
        self.menuFile = QMenu(self.menubar)
        self.menuSave_as = QMenu(self.menuFile)
        self.menuSetting = QMenu(self.menubar)
        self.menuHelp = QMenu(self.menubar)
        self.trajectory_checkbox = QCheckBox()
        self.current_frame = 0

        self.frame_label = QLabel("Frame 0/0")

        self.is_playing = False
        self.show_trajectories = False
        self.scale_factor = 1.0

        self.scatter_item = None
        self.line_items = []
        self.trajectory_items = []
        self._gl_pending = False

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

    def load_bin_file(self, content: bytes):
        """Load raw binary animation content and prepare transformed frame data."""
        try:
            self.content = content
            self.move_bin = MoveBin.build_binary(content)
            raw_frames = [frame.points for frame in self.move_bin.bin_data]
            self.num_frames = self.move_bin.frames_num
            self.num_nodes = self.move_bin.bin_data[0].length if self.num_frames > 0 else 0

            self.frames_data = [
                [self._transform_point(p) for p in frame]
                for frame in raw_frames
            ]

            self.data_bounds = self.calculate_data_bounds()
            # 计算视图平移偏移：只在 X/Z 方向居中，Y 轴保持原始高度（Y=0 即为动画的地面）
            if self.data_bounds:
                cx, cy, cz = self.data_bounds['center']
                self.view_offset = np.array([cx, 0.0, cz], dtype=float)
            else:
                self.view_offset = np.zeros(3, dtype=float)
            self.sphere_radius = self.calculate_sphere_radius()
            self.update_ui_after_loading()
            self.current_frame = 0
            if self.isVisible():
                self.setup_gl_after_loading()
                self.update_frame_display()
            else:
                self._gl_pending = True
        except Exception as e:
            ErrorDialog(self, e)

    @staticmethod
    def _transform_point(point):
        """Transform original (x, y, z) coordinates into visualization coordinates."""
        x, y, z = point
        return [z, x, y]

    def calculate_data_bounds(self):
        """Compute global min/max ranges and center for all animation frames."""
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
        """Update frame slider range and window title according to loaded data."""
        self.frame_slider.setRange(0, self.num_frames - 1)
        self.frame_label.setText(f"Frame {self.current_frame + 1}/{self.num_frames}")
        self.setWindowTitle(f"BinaryPlayer - {self.num_frames} frames, {self.num_nodes} nodes")

    def setup_gl_after_loading(self):
        """Create scatter, skeleton lines, grid and trajectories after data is loaded."""
        self.clear_scene()
        if not self.frames_data:
            return

        max_range = max(self.data_bounds['range']) if self.data_bounds else 1.0
        point_size = 10.0

        colors = []
        for node_idx in range(self.num_nodes):
            r, g, b = self.hsv_to_rgb(node_idx / max(1, self.num_nodes - 1), 0.8, 1.0)
            colors.append((r, g, b, 1.0))
        colors = np.array(colors, dtype=float)

        if self.frames_data and self.frames_data[0]:
            init_pos = np.array(self.frames_data[0], dtype=np.float32) - self.view_offset.astype(np.float32)
        else:
            init_pos = np.zeros((self.num_nodes, 3), dtype=np.float32)

        self.scatter_item = gl.GLScatterPlotItem(
            pos=init_pos,
            size=point_size,
            color=colors.astype(np.float32),
            pxMode=True  # 像素模式，保证点大小恒定、可见
        )
        self.scatter_item.setGLOptions('opaque')
        self.view.addItem(self.scatter_item)

        # 初始化骨骼线段
        valid_connections = [
            (start, end) for start, end in self.connections
            if start < self.num_nodes and end < self.num_nodes
        ]
        self.line_items = []
        for _ in valid_connections:
            line = gl.GLLinePlotItem(
                pos=np.zeros((2, 3), dtype=float),
                color=(0, 0, 0, 1),
                width=2,
                antialias=True
            )
            self.view.addItem(line)
            self.line_items.append(line)

        self.setup_trajectories()

        # 根据动画数据范围动态创建“近似无限”的网格
        self.grid_item = gl.GLGridItem(glOptions="opaque")
        self.grid_item.setColor((0, 0, 0, 255))

        if self.data_bounds:
            rng_x, rng_y, rng_z = self.data_bounds['range']
            max_range = max(rng_x, rng_y, rng_z)
        else:
            max_range = 1.0

        if max_range <= 0:
            max_range = 1.0

        # 网格尺寸设置为范围的多倍，保证视觉上“看不到边界”，同时相对物体略微缩减
        grid_size = max_range * 4.0
        # 只需要 12x12 个格子即可，格子大小由整体尺寸自动决定
        cell_size = max(grid_size / 12.0, 0.05)

        self.grid_item.setSize(grid_size, grid_size)
        self.grid_item.setSpacing(cell_size, cell_size)

        # 网格原点固定在 (0, 0, 0)，Y=0 即为动画坐标系的 Y=0
        self.grid_item.translate(0.0, 0.0, 0.0)
        self.view.addItem(self.grid_item)

        self.setup_camera()

    def clear_scene(self):
        """Remove all plotted items from the 3D view and stop playback if running."""
        if self.is_playing:
            self.timer.stop()
            self.is_playing = False
            self.play_button.setText("Play")
        if self.scatter_item is not None:
            self.view.removeItem(self.scatter_item)
            self.scatter_item = None
        for item in self.line_items:
            self.view.removeItem(item)
        self.line_items = []
        for item in self.trajectory_items:
            self.view.removeItem(item)
        self.trajectory_items = []
        if getattr(self, "grid_item", None) is not None:
            self.view.removeItem(self.grid_item)
            self.grid_item = None

    def setup_ui(self):
        """Construct menus, toolbar actions and playback controls for the animation player."""
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
        self.menuFile.setIcon(QIcon(u':/icons/file'))
        self.menuSetting.setIcon(QIcon(u':/icons/setting'))
        self.menuHelp.setIcon(QIcon(u':/icons/help'))
        self.action_open.setText("Open")
        self.action_csv.setText("csv")
        self.action_bin.setText("bin/bytes")

        # 菜单与设置项使用多语言资源
        self.menuFile.setTitle(i18n.tr("menu.file"))
        self.menuSave_as.setTitle(i18n.tr("menu.export"))
        self.menuSetting.setTitle(i18n.tr("menu.setting"))
        self.menuHelp.setTitle(i18n.tr("menu.help"))

        # add shared About action under Help menu
        self.actionHelpAbout = QAction(self)
        self.actionHelpAbout.setObjectName("actionHelpAbout")
        self.actionHelpAbout.setText("About")
        self.menuHelp.addAction(self.actionHelpAbout)
        self.actionHelpAbout.triggered.connect(self.show_help_dialog)

        # add shared Settings action
        self.actionSettings = QAction(self)
        self.actionSettings.setObjectName("actionSettings")
        self.actionSettings.setText("Settings...")
        self.menuSetting.addAction(self.actionSettings)
        self.actionSettings.triggered.connect(self.show_settings_dialog)

        self.layout.addWidget(self.view_frame, 1)
        self.control_layout.setSpacing(5)

        self.play_button.setText(i18n.tr("anim.button.play"))
        self.prev_button.setText(i18n.tr("anim.button.prev"))
        self.next_button.setText(i18n.tr("anim.button.next"))
        self.reset_camera_button.setText(i18n.tr("anim.button.reset_camera"))
        self.trajectory_checkbox.setText(i18n.tr("anim.checkbox.show_orbit"))

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

        frame_label = QLabel(i18n.tr("anim.label.frame_prefix"))
        self.control_layout.addWidget(frame_label)
        self.frame_slider.setRange(0, 0)
        self.frame_slider.valueChanged.connect(self.slider_changed)
        self.control_layout.addWidget(self.frame_slider)
        self.control_layout.addWidget(self.frame_label)
        self.layout.addLayout(self.control_layout)
        self.view.setBackgroundColor('w')

    def calculate_sphere_radius(self):
        """Estimate a suitable sphere radius based on overall data extents."""
        if not self.data_bounds:
            return 0.1

        max_range = max(self.data_bounds['range'])
        radius = max_range * 0.005
        return max(0.01, radius)

    def setup_trajectories(self):
        """Precompute and add trajectory line items for each node in the animation."""
        self.trajectory_items = []
        if not self.frames_data:
            return
        for node_idx in range(self.num_nodes):
            raw_points = np.array(
                [self.frames_data[frame_idx][node_idx] for frame_idx in range(self.num_frames)],
                dtype=float
            )
            points = raw_points - self.view_offset
            color = self.hsv_to_rgb(node_idx / max(1, self.num_nodes - 1), 0.8, 0.6) + (1.0,)
            line = gl.GLLinePlotItem(pos=points, color=color, width=1, antialias=True)
            line.setVisible(False)
            self.view.addItem(line)
            self.trajectory_items.append(line)

    def setup_camera(self):
        """Configure the camera position so the animated character fits nicely in view."""
        if not self.data_bounds:
            return
        center = (0.0, 0.0, 0.0)
        max_range = max(self.data_bounds['range'])
        base_distance = max_range * 2.0 if max_range > 0 else 10
        distance = base_distance * 0.7
        self.view.opts['center'] = pg.Vector(*center)
        self.view.setCameraPosition(
            distance=distance,
            elevation=0, 
            azimuth=0   
        )

    def reset_camera(self):
        """Reset the camera to its default position and refresh the view."""
        self.setup_camera()
        self.view.update()

    def setup_animation(self):
        """Connect timer updates to frame stepping and initialize playback state."""
        self.timer.timeout.connect(self.next_frame)
        self.timer.setInterval(50)  # 20 FPS
        self.update_frame_display()

    def update_frame_display(self):
        """Update scatter, skeleton lines and UI to reflect the current frame index."""
        if self.current_frame >= len(self.frames_data):
            return
        frame_points = self.frames_data[self.current_frame]

        if self.scatter_item is not None:
            scaled = (np.array(frame_points, dtype=np.float32) - self.view_offset.astype(np.float32)) * np.float32(self.scale_factor)
            self.scatter_item.setData(pos=scaled)

        if self.line_items:
            valid_connections = [
                (start, end) for start, end in self.connections
                if start < len(frame_points) and end < len(frame_points)
            ]
            for line_item, (start_idx, end_idx) in zip(self.line_items, valid_connections):
                start_point = (np.array(frame_points[start_idx], dtype=float) - self.view_offset) * self.scale_factor
                end_point = (np.array(frame_points[end_idx], dtype=float) - self.view_offset) * self.scale_factor
                pos = np.vstack([start_point, end_point])
                line_item.setData(pos=pos)

        self.frame_slider.setValue(self.current_frame)
        self.frame_label.setText(f"Frame {self.current_frame + 1}/{self.num_frames}")

        self.view.update()

    def toggle_play(self):
        """Toggle between playing and paused states for the animation."""
        if self.is_playing:
            self.timer.stop()
            self.play_button.setText(i18n.tr("anim.button.play"))
        else:
            self.timer.start()
            self.play_button.setText(i18n.tr("anim.button.stop"))
        self.is_playing = not self.is_playing

    def next_frame(self):
        """Advance the animation to the next frame and update the display."""
        self.current_frame = (self.current_frame + 1) % self.num_frames
        self.update_frame_display()

    def previous_frame(self):
        """Move the animation to the previous frame and update the display."""
        self.current_frame = (self.current_frame - 1) % self.num_frames
        self.update_frame_display()

    def slider_changed(self, value):
        """Jump to a frame when the slider is moved to a different position."""
        if value != self.current_frame:
            self.current_frame = value
            self.update_frame_display()

    def toggle_trajectories(self, state):
        """Show or hide trajectory lines based on the checkbox state."""
        self.show_trajectories = (state == Qt.CheckState.Checked.value)
        for item in self.trajectory_items:
            item.setVisible(self.show_trajectories)
        self.view.update()

    @staticmethod
    def hsv_to_rgb(h, s, v):
        """Convert HSV color values to an RGB tuple."""
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
        """Stop playback and delegate to the base close event handler."""
        try:
            if self.is_playing:
                self.timer.stop()
                self.play_button.setText("Play")
            super().closeEvent(event)
        except Exception as e:
            ErrorDialog(self, e)

    def showEvent(self, event):
        """Build 3D scene on first show to avoid GL context conflict with other windows; refresh view."""
        try:
            super().showEvent(event)
            if getattr(self, "_gl_pending", False) and self.frames_data:
                self._gl_pending = False
                self.setup_gl_after_loading()
                self.update_frame_display()
            self.view.update()
        except Exception as e:
            ErrorDialog(self, e)

    def hideEvent(self, event):
        """Stop playback when the window is hidden and delegate to the base handler."""
        try:
            if self.is_playing:
                self.timer.stop()
                self.play_button.setText("Play")
            super().hideEvent(event)
        except Exception as e:
            ErrorDialog(self, e)
