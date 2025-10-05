import os
import shutil
from core.rules_manager import RulesManager

rules_manager = RulesManager()

def sort_by_extension(filename: str, rules: list[dict]) -> str | None:
    """Подбор папки по расширению"""
    ext = os.path.splitext(filename)[1].lower()
    for rule in rules:
        if rule["type"] == "Расширение" and ext in rule["patterns"]:
            return rule["folder"]
    return None

def sort_by_keyword(filename: str, rules: list[dict]) -> str | None:
    """Подбор папки по ключевым словам"""
    for rule in rules:
        folder = rule["folder"]
        for pattern in rule["patterns"]:
            if pattern.lower() in filename.lower():
                return folder
    return None


def move_file(file_path: str, target_dir: str) -> str:
    """Перемещаем файл в папку с обработкой ошибок"""
    os.makedirs(target_dir, exist_ok=True)
    filename = os.path.basename(file_path)

    try:
        shutil.move(file_path, os.path.join(target_dir, filename))
        return f"OK:: Файл {filename} перенесён в {target_dir}"
    except PermissionError:
        return f"ERROR: нет доступа к {file_path}"
    except Exception as e:
        return f"ERROR: Ошибка при переносе {e}"
    
def sort_file(file_path: str) -> str:
    """ Определяет правило (по расширению или 
    ключевому слову) и переносит файл в нужную папку."""
    
    if not os.path.isfile(file_path):
        return "ERROR: указан не файл"
    
    filename = os.path.basename(file_path)
    ext = os.path.splitext(file_path)[1].lower()
    rules = rules_manager.load_rules()

    target_dir = sort_by_keyword(filename, rules)
    if not target_dir:
        target_dir = sort_by_extension(filename, rules)

    if not target_dir:
        return f"NO_RULE::{ext}"
    
    return move_file(file_path, target_dir)
