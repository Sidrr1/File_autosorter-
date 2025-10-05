from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
from core.file_sorter import sort_file


class SortTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.drop_area = QLabel("Перетащите файлы сюда")
        self.drop_area.setStyleSheet("border: 2px dashed #aaa; font-size: 16px;")
        self.drop_area.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True) 

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(100)   

        layout.addWidget(self.drop_area, stretch=3)
        layout.addWidget(QLabel("ЛОГ:"))
        layout.addWidget(self.log, stretch=1)
        self.setLayout(layout)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        for url in urls:
            file_path = url.toLocalFile()
            if file_path:
                result = sort_file(file_path)
                
                if result.startswith("NO_RULE::"):
                    ext = result.split("::")[1]
                    QMessageBox.warning(
                        self,
                        "Нет правил для сортировки", 
                        f"Для расширения {ext} не задана папка.\n\n"
                        "Откройте вкладку «Настройки» и добавьте правило,\n"
                        "чтобы такие файлы сортировались автоматически."
                    )
                    self.log.append(f"Нет правил для {ext}")
                else:
                    self.log.append(result)


    