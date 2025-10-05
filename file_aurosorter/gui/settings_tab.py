import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QHBoxLayout, QPushButton,
    QHeaderView, QMessageBox, QTableWidgetItem
)
from core.rules_manager import RulesManager
from gui.add_rule_dialog import AddRuleDialog


class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.rules_manager = RulesManager()

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Тип", "Шаблоны", "Папка назначения"])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)

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
        for rule in rules:
            self.add_rule_to_table(rule)

    def add_rule_to_table(self, rule: dict):
        """Добавление строки в таблицу"""
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(rule.get("type", "")))
        self.table.setItem(row, 1, QTableWidgetItem(", ".join(rule.get("patterns", []))))
        self.table.setItem(row, 2, QTableWidgetItem(rule.get("folder", "")))

    def add_rule(self):
        """Добавление нового правила через кастомный диалог"""
        dialog = AddRuleDialog(self)
        if dialog.exec_():
            result = dialog.get_result()
            if result:
                self.rules_manager.add_rule(
                    result["folder"],
                    result["type"],
                    result["patterns"]
                )
                self.refresh_table()

    def delete_rule(self):
        """Удаление выбранного правила"""
        row = self.table.currentRow()
        if row >= 0:
            # Удаляем правило по индексу
            self.rules_manager.delete_rule(row)
            self.refresh_table()
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите правило для удаления")
