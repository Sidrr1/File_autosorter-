import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QHBoxLayout, QPushButton,
    QHeaderView, QFileDialog, QInputDialog, QMessageBox, QTableWidgetItem
)
from core.rules_manager import RulesManager


class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.rules_manager = RulesManager()

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Расширения", "Папка назначения"])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Добавить правило")
        btn_del = QPushButton("Удалить правило")

        btn_add.clicked.connect(self.add_rule)
        btn_del.clicked.connect(self.delete_rule)

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_del)

        layout.addWidget(self.table)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.refresh_table()

    def refresh_table(self):
        """Обновить таблицу из RulesManager"""
        self.table.setRowCount(0)
        rules = self.rules_manager.load_rules()
        for folder, extensions in rules.items():
            self.add_rule_to_table(extensions, folder)

    def add_rule_to_table(self, extensions, folder):
        """Добавление строки в таблицу"""
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(", ".join(extensions)))
        self.table.setItem(row, 1, QTableWidgetItem(folder))

    def add_rule(self):
        """Добавление нового правила"""
        exts_str, ok = QInputDialog.getText(
            self, "Новое правило",
            """Введите расширения (например: .txt):
Так же можно и несколько(.txt, .docx, .jpeg)
            """
        )
        if not ok or not exts_str.strip():
            return

        extensions = [("." + ext.strip().lower().lstrip(".")) for ext in exts_str.split(",") if ext.strip()]
        if not extensions:
            QMessageBox.warning(self, "Ошибка", "Нужно указать хотя бы одно расширение!")
            return

        folder = QFileDialog.getExistingDirectory(self, "Выберите папку назначения")
        if not folder:
            return

        rules = self.rules_manager.load_rules()
        rules[folder] = extensions
        self.rules_manager.save_rules(rules)

        self.refresh_table()

    def delete_rule(self):
        """Удаление выбранного правила"""
        row = self.table.currentRow()
        if row >= 0:
            folder = self.table.item(row, 1).text()
            rules = self.rules_manager.load_rules()
            if folder in rules:
                del rules[folder]
                self.rules_manager.save_rules(rules)
            self.refresh_table()
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите правило для удаления")
