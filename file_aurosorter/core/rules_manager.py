import os
import json


class RulesManager:
    def __init__(self, file_path="data/rules.json"):
        self.file_path = file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def load_rules(self) -> list[dict]:
        """Загрузить правила из JSON"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                rules = json.load(f)
                if isinstance(rules, list):
                    return rules
                return [] 
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_rules(self, rules: list[dict]):
        """Сохранить правила в JSON"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(rules, f, ensure_ascii=False, indent=4)

    def add_rule(self, folder: str, rule_type: str, patterns: list[str]):
        """Добавляем новое правило или расширяем существующее"""
        rules = self.load_rules()

        for r in rules:
            if r["type"] == rule_type and r["folder"] == folder:
                existing = set(r["patterns"])
                r["patterns"] = list(existing.union(patterns))
                self.save_rules(rules)
                return

        rules.append({
            "type": rule_type,
            "patterns": patterns,
            "folder": folder
        })
        self.save_rules(rules)

    def update_rule(self, index: int, folder: str, rule_type: str, patterns: list[str]):
        """Обновить правило по индексу"""
        rules = self.load_rules()
        if 0 <= index < len(rules):
            rules[index] = {
                "type": rule_type,
                "patterns": patterns,
                "folder": folder
            }
            self.save_rules(rules)

    def delete_rule(self, index: int):
        """Удалить правило по индексу"""
        rules = self.load_rules()
        if 0 <= index < len(rules):
            rules.pop(index)
            self.save_rules(rules)
