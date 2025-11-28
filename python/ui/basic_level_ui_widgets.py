import vtk
from PyQt6.QtCore import (QCoreApplication, QMetaObject, QRect,
                          Qt, QTimer, QSize)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (QGridLayout, QLabel, QPushButton, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QSlider,
                             QMenuBar, QMenu, QCheckBox, QDoubleSpinBox, QComboBox, QProgressBar, QTextBrowser,
                             QDialogButtonBox, QStatusBar, QSpinBox)
from pyvistaqt import QtInteractor

from python.core.core_classes import MoveBin
from python.ui.notice_dialog_widgets import ErrorDialog
from python.util.values import basic_bin_bytes


class BasicToolMainWindow:
    def __init__(self, main_window):
        self.label = None
        self.pushButton_1 = None
        self.pushButton_2 = None
        self.pushButton_3 = None
        self.gridLayout = None
        self.gridLayoutWidget = None
        self.centralwidget = None
        self.setup_ui(main_window)

    def setup_ui(self, main_window):
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
        main_window.setWindowTitle(QCoreApplication.translate("MainWindow", u"Shadow Fight 2 Easy Switch", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Animation Editor", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow",
                                                             u"Frames(.obj(multiple)) to (Format Data).csv",
                                                             None))
        self.pushButton_1.setText(QCoreApplication.translate("MainWindow",
                                                             u"Model Editor",
                                                             None))
        self.label.setText(QCoreApplication.translate("MainWindow",
                                                      u"<html><head/><body><p>"
                                                      u"<span style=\" font-size:24pt; font-weight:700;\">"
                                                      u"Shadow Fight 2 Easy Switch"
                                                      u"</span></p></body></html>",
                                                      None))


class ModelPlayer:
    def __init__(self, main_window):
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

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menuExport.addAction(self.action_xml)
        self.menuExport.addAction(self.action_obj)

        self.re_translate_ui(main_window)

        QMetaObject.connectSlotsByName(main_window)
    # setupUi

    def re_translate_ui(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("MainWindow", u"ModelPlayer", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.action_xml.setText(QCoreApplication.translate("MainWindow", u"xml", None))
        self.action_obj.setText(QCoreApplication.translate("MainWindow", u"(WaveFront)obj", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("MainWindow", u"False", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("MainWindow", u"True", None))

        self.label_3.setText(QCoreApplication.translate("MainWindow", u"range(x):", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"is zoom:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"range(z):", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"begin_id", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"xyz", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"xzy", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"yxz", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"yzx", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"zxy", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"zyx", None))

        self.comboBox_4.setItemText(0, QCoreApplication.translate("MainWindow", u"weapon", None))
        self.comboBox_4.setItemText(1, QCoreApplication.translate("MainWindow", u"helm", None))
        self.comboBox_4.setItemText(2, QCoreApplication.translate("MainWindow", u"ranged", None))
        self.comboBox_4.setItemText(3, QCoreApplication.translate("MainWindow", u"armor_a", None))
        self.comboBox_4.setItemText(4, QCoreApplication.translate("MainWindow", u"armor_b", None))
        self.comboBox_4.setItemText(5, QCoreApplication.translate("MainWindow", u"armor_c", None))

        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Advanced Setting", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"range(y):", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"type:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"rotate:", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuExport.setTitle(QCoreApplication.translate("MainWindow", u"Export", None))
        self.menuSetting.setTitle(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))


class BasicYieldCsvPage:
    def __init__(self, main_window):
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
        main_window.setWindowTitle(QCoreApplication.translate("MainWindow", u"ToCsv", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"is zoom:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"range(z):", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"rotate:", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Select Dir", None))
        self.label_title.setText(QCoreApplication.translate("MainWindow",
                                                            u"<html><head/><body><p>"
                                                            u"<span style=\" font-size:12pt; font-weight:700;\">"
                                                            u"Bin: .objs to .csv"
                                                            u"</span></p>"
                                                            u"<p>output and input are in './objs_to_bin'</p>"
                                                            u"</body></html>",
                                                            None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"xyz", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"xzy", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"yxz", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"yzx", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"zxy", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"zyx", None))

        self.comboBox_2.setItemText(0, QCoreApplication.translate("MainWindow", u"False", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("MainWindow", u"True", None))

        self.label_2.setText(QCoreApplication.translate("MainWindow", u"range(y):", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"range(x):", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Progress:", None))


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
        self.menuFile.setIcon(QIcon(u':/icons/file'))
        self.menuSetting.setIcon(QIcon(u':/icons/setting'))
        self.menuHelp.setIcon(QIcon(u':/icons/help'))
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
