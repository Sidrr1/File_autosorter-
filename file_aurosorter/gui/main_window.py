from PyQt5.QtWidgets import QMainWindow, QTabWidget
from .sort_tab import SortTab
from .settings_tab import SettingsTab
from core.file_sorter import sort_file

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Autosorter")
        self.setGeometry(200, 200, 800, 500)

        tabs = QTabWidget()
        tabs.addTab(SortTab(), "Сортировка")
        tabs.addTab(SettingsTab(), "Настройки")

        self.setCentralWidget(tabs)