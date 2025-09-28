import os
import shutil
from core.rules_manager import RulesManager

rules_manager = RulesManager()

def sort_file(file_path: str) -> str:
    """
    принимает путь к файлу, определяет категорию по расширению 
    и перемещает в соответствующую папку.
    """
    if not os.path.isfile(file_path):
        return "Oшибка: указан не файл"
    
    ext = os.path.splitext(file_path)[1].lower()
    rules = rules_manager.load_rules()

    target_dir = None
    for folder, extensions in rules.items():
        if ext in extensions:
            target_dir = folder
            break

    if not target_dir:
        return f"NO_RULE::{ext}"
    
    os.makedirs(target_dir, exist_ok=True)

    try:
        shutil.move(file_path, os.path.join(target_dir, os.path.basename(file_path)))
        return f"OK:: Файл{os.path.basename(file_path)} перенесён в {target_dir}"
    except PermissionError:
        return f"EROR: нет доступа к {file_path}"
    except Exception as e:
        return f"EROR: Ошибка при переносе {e}"