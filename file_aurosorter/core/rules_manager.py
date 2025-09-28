import os
import json


class RulesManager:
    def __init__(self, file_path="data/rules.json"):
        self.file_path = file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=4)

    def load_rules(self) -> dict:
        """Загрузить правила из JSON"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def save_rules(self, rules: dict):
        """Сохранить правила в JSON"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(rules, f, ensure_ascii=False, indent=4)

    def get_rules(self) -> dict:
        """Вернуть все правила (папка -> список расширений)"""
        return self.load_rules()

    def add_rule(self, folder: str, extensions: list[str]):
        """Добавить новое правило"""
        rules = self.load_rules()
        rules[folder] = extensions
        self.save_rules(rules)

    def update_rule(self, folder: str, extensions: list[str]):
        """Обновить правило (перезаписать список расширений)"""
        rules = self.load_rules()
        rules[folder] = extensions
        self.save_rules(rules)

    def delete_rule(self, folder: str):
        """Удалить правило по папке"""
        rules = self.load_rules()
        if folder in rules:
            del rules[folder]
            self.save_rules(rules)
