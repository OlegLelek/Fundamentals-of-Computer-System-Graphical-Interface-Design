import os
import sys
from datetime import datetime

from PyQt5.QtCore import QObject, QTimer, pyqtSlot
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine


class Interface(QObject):
    def __init__(self):
        super().__init__()
        self.canvas = None

        self.save_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "snapshots"
        )
        os.makedirs(self.save_dir, exist_ok=True)

        self.timer = QTimer(self)
        self.timer.setInterval(10_000)
        self.timer.timeout.connect(self.save_canvas)
        self.timer.start()

    @pyqtSlot(QObject)
    def set_canvas(self, canvas):
        self.canvas = canvas
        print("Canvas подключён к backend")

    @pyqtSlot()
    def save_canvas(self):
        if self.canvas is None:
            print("Canvas ещё не подключён")
            return

        filename = datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
        filepath = os.path.join(self.save_dir, filename)

        if self.canvas.save(filepath):
            print(f"Рисунок сохранён: {filepath}")
        else:
            print(f"Не удалось сохранить рисунок: {filepath}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    interface = Interface()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("backend", interface)

    qml_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "mainWindow.qml"
    )
    engine.load(qml_file)

    if not engine.rootObjects():
        print("Ошибка: не удалось загрузить QML-файл")
        sys.exit(-1)

    root = engine.rootObjects()[0]
    canvas = root.findChild(QObject, "canvas")
    if canvas is None:
        print("Ошибка: объект Canvas не найден")
        sys.exit(-1)

    interface.set_canvas(canvas)
    sys.exit(app.exec_())
