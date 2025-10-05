from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QFileDialog, QTabWidget, QWidget, QDialogButtonBox
)
from PyQt5.QtCore import Qt


class AddRuleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setMinimumWidth(400)

        self.folder = None
        self.rule_type = "extension"
        self.patterns = []

        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.ext_tab = QWidget()
        self.key_tab = QWidget()
        self._init_extension_tab()
        self._init_keyword_tab()
        self.tabs.addTab(self.ext_tab, "Расширения")
        self.tabs.addTab(self.key_tab, "Ключевые слова")
        layout.addWidget(self.tabs)

        folder_layout = QHBoxLayout()
        self.folder_edit = QLineEdit()
        self.folder_edit.setReadOnly(False)
        self.folder_edit.setPlaceholderText("Папка не выбрана")

        btn_folder = QPushButton("Обзор...")
        btn_folder.clicked.connect(self.choose_folder)

        folder_layout.addWidget(self.folder_edit)
        folder_layout.addWidget(btn_folder)
        layout.addLayout(folder_layout)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def _init_extension_tab(self):
        """Вкладка для ввода расширений"""
        layout = QVBoxLayout()
        self.ext_input = QLineEdit()
        self.ext_input.setPlaceholderText("Например: jpg, png, pdf")
        layout.addWidget(QLabel("Введите расширения через запятую:"))
        layout.addWidget(self.ext_input)
        self.ext_tab.setLayout(layout)

    def _init_keyword_tab(self):
        """Вкладка для ввода ключевых слов"""
        layout = QVBoxLayout()
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Например: отчет, фото, музыка")
        layout.addWidget(QLabel("Введите ключевые слова через запятую:"))
        layout.addWidget(self.key_input)
        self.key_tab.setLayout(layout)

    def choose_folder(self):
        """Выбор папки назначения"""
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder:
            self.folder = folder
            self.folder_edit.setText(folder) 

    def validate(self):
        """Проверка заполненности"""
        current_tab = self.tabs.currentIndex()
        if current_tab == 0:
            text = self.ext_input.text().strip()
            if text:
                self.rule_type = "extension"
                self.patterns = [x.strip().lower() for x in text.split(",") if x.strip()]
        else:
            text = self.key_input.text().strip()
            if text:
                self.rule_type = "keyword"
                self.patterns = [x.strip().lower() for x in text.split(",") if x.strip()]

        return bool(self.folder and self.patterns)

    def get_result(self):
        """Возращение результата вSettingsTab"""
        if not self.validate():
            return None
        return {
            "type": self.rule_type,
            "patterns": self.patterns,
            "folder": self.folder
        }
