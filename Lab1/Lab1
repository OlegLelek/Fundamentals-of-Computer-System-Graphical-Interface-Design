import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class LabWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа №1 (PyQt5)")
        self.setFixedSize(360, 400)

        # Надпись
        self.label = QLabel("Нажмите кнопку, чтобы увидеть изображение", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        # Кнопка
        self.button = QPushButton("Показать изображение", self)
        self.button.clicked.connect(self.on_button_click)

        # готовим изображение
        self.pixmap = QPixmap("picture.png")
        self.image_shown = False

        # Расположение виджетов вертикально
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.label)
        layout.addSpacing(20)
        layout.addWidget(self.button)
        layout.addStretch()
        self.setLayout(layout)

    def on_button_click(self):
        if not self.image_shown:
            scaled = self.pixmap.scaled(280, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(scaled)
            self.label.setMinimumSize(280, 180)
            self.image_shown = True
            self.button.setText("Показать текст")
        else:
            self.label.clear()
            self.label.setText("Нажмите кнопку, чтобы увидеть изображение")
            self.image_shown = False
            self.button.setText("Показать изображение")


def main():
    app = QApplication(sys.argv)
    window = LabWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
